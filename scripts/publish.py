"""Publish a queued social/posts.csv row to Instagram or YouTube.

Never prints tokens or env file contents. Run from repo root:
    python scripts/publish.py --post-id P0001
"""

from __future__ import annotations

import argparse
import csv
import json
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_CSV = ROOT / "social" / "posts.csv"
MEDIA_CSV = ROOT / "media" / "media.csv"
LIBRARY = ROOT / "media" / "library"
IG_ENV = ROOT / "config" / "instagram.env"
YT_ENV = ROOT / "config" / "youtube.env"

PHOTO_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm"}
SSL_CTX = ssl.create_default_context()


def load_env(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.is_file():
        return data
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def sanitize_error(text: str) -> str:
    text = " ".join(text.split())
    if len(text) > 240:
        text = text[:237] + "..."
    return text


def http_json(method: str, url: str, *, data: dict | None = None, headers: dict | None = None, raw: bytes | None = None) -> dict:
    body = raw
    req_headers = dict(headers or {})
    if data is not None and raw is None:
        body = urllib.parse.urlencode(data).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=120) as resp:
            payload = resp.read().decode("utf-8")
            if not payload:
                return {}
            try:
                parsed = json.loads(payload)
            except json.JSONDecodeError:
                return {"raw": "ok"}
            return parsed if isinstance(parsed, dict) else {"raw": "ok"}
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(err_body)
            msg = parsed.get("error", {}).get("message") or err_body
        except json.JSONDecodeError:
            msg = err_body
        raise RuntimeError(sanitize_error(f"HTTP {exc.code}: {msg}")) from None


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = [{k: (v if v is not None else "") for k, v in row.items()} for row in reader]
    return fieldnames, rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    tmp = path.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(path)


def note_value(notes: str, key: str) -> str | None:
    prefix = key.lower() + ":"
    for line in notes.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith(prefix):
            return stripped.split(":", 1)[1].strip()
    return None


def upsert_note(notes: str, key: str, value: str) -> str:
    prefix = key.lower() + ":"
    lines = notes.splitlines() if notes else []
    replaced = False
    out: list[str] = []
    for line in lines:
        if line.strip().lower().startswith(prefix):
            out.append(f"{key}: {value}")
            replaced = True
        else:
            out.append(line)
    if not replaced:
        if out and out[-1].strip():
            out.append(f"{key}: {value}")
        else:
            out.append(f"{key}: {value}")
    return "\n".join(out).strip()


def find_post(post_id: str) -> tuple[list[str], list[dict[str, str]], dict[str, str]]:
    fieldnames, rows = read_csv(POSTS_CSV)
    for row in rows:
        if row.get("id") == post_id:
            return fieldnames, rows, row
    raise RuntimeError(f"No post {post_id} in social/posts.csv")


def media_file(media_id: str) -> Path:
    _, rows = read_csv(MEDIA_CSV)
    for row in rows:
        if row.get("id") == media_id:
            name = row.get("filename") or ""
            path = LIBRARY / name
            if not path.is_file():
                raise RuntimeError(f"Missing library file for {media_id}: {name}")
            return path
    raise RuntimeError(f"No media {media_id} in media/media.csv")


def mark_posted(fieldnames: list[str], rows: list[dict[str, str]], post_id: str, permalink: str) -> None:
    today = date.today().isoformat()
    for row in rows:
        if row.get("id") == post_id:
            row["status"] = "posted"
            row["posted_at"] = today
            row["notes"] = upsert_note(row.get("notes") or "", "permalink", permalink)
            break
    write_csv(POSTS_CSV, fieldnames, rows)


def publish_instagram(row: dict[str, str], asset: Path, *, dry_run: bool) -> str:
    env = load_env(IG_ENV)
    user_id = env.get("INSTAGRAM_USER_ID") or ""
    token = env.get("INSTAGRAM_ACCESS_TOKEN") or ""
    version = env.get("INSTAGRAM_GRAPH_VERSION") or "v21.0"
    public_base = (env.get("INSTAGRAM_PUBLIC_MEDIA_BASE_URL") or "").rstrip("/")
    if not user_id or not token:
        raise RuntimeError("config/instagram.env needs INSTAGRAM_USER_ID and INSTAGRAM_ACCESS_TOKEN")

    caption = row.get("caption") or ""
    ext = asset.suffix.lower()
    is_video = ext in VIDEO_EXT
    is_photo = ext in PHOTO_EXT
    if not is_video and not is_photo:
        raise RuntimeError(f"Instagram does not support {ext} files")

    if dry_run:
        kind = "reel" if is_video else "photo"
        return f"dry-run instagram {kind} {asset.name} caption_chars={len(caption)}"

    graph = f"https://graph.facebook.com/{version}"
    if is_photo:
        image_url = note_value(row.get("notes") or "", "image_url")
        if not image_url:
            if not public_base:
                raise RuntimeError(
                    "Instagram photos need a public HTTPS URL. Set INSTAGRAM_PUBLIC_MEDIA_BASE_URL "
                    "or put image_url: https://... in the post notes."
                )
            image_url = f"{public_base}/{asset.name}"
        created = http_json(
            "POST",
            f"{graph}/{user_id}/media",
            data={"image_url": image_url, "caption": caption, "access_token": token},
        )
        container_id = created.get("id")
        if not container_id:
            raise RuntimeError("Instagram did not return a media container id")
    else:
        created = http_json(
            "POST",
            f"{graph}/{user_id}/media",
            data={
                "media_type": "REELS",
                "upload_type": "resumable",
                "caption": caption,
                "access_token": token,
            },
        )
        container_id = created.get("id")
        upload_uri = created.get("uri")
        if not container_id or not upload_uri:
            raise RuntimeError("Instagram did not return a resumable upload uri")
        payload = asset.read_bytes()
        http_json(
            "POST",
            upload_uri,
            raw=payload,
            headers={
                "Authorization": f"OAuth {token}",
                "offset": "0",
                "file_size": str(len(payload)),
                "Content-Type": "application/octet-stream",
            },
        )
        deadline = time.time() + 300
        while time.time() < deadline:
            status = http_json(
                "GET",
                f"{graph}/{container_id}?fields=status_code&access_token={urllib.parse.quote(token)}",
            )
            code = (status.get("status_code") or "").upper()
            if code == "FINISHED":
                break
            if code in {"ERROR", "EXPIRED"}:
                raise RuntimeError(f"Instagram container {code}")
            time.sleep(5)
        else:
            raise RuntimeError("Timed out waiting for Instagram to process the video")

    published = http_json(
        "POST",
        f"{graph}/{user_id}/media_publish",
        data={"creation_id": container_id, "access_token": token},
    )
    media_id = published.get("id")
    if not media_id:
        raise RuntimeError("Instagram publish did not return a media id")
    meta = http_json(
        "GET",
        f"{graph}/{media_id}?fields=permalink&access_token={urllib.parse.quote(token)}",
    )
    return meta.get("permalink") or f"instagram://media/{media_id}"


def publish_youtube(row: dict[str, str], asset: Path, *, dry_run: bool) -> str:
    env = load_env(YT_ENV)
    client_id = env.get("YOUTUBE_CLIENT_ID") or ""
    client_secret = env.get("YOUTUBE_CLIENT_SECRET") or ""
    refresh_token = env.get("YOUTUBE_REFRESH_TOKEN") or ""
    privacy = env.get("YOUTUBE_PRIVACY_STATUS") or "unlisted"
    category = env.get("YOUTUBE_CATEGORY_ID") or "10"
    if not client_id or not client_secret or not refresh_token:
        raise RuntimeError(
            "config/youtube.env needs YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN "
            "(run python scripts/youtube_auth.py)"
        )

    title = note_value(row.get("notes") or "", "title") or asset.stem.replace("-", " ")
    title = title[:100]
    description = row.get("caption") or ""
    if dry_run:
        return f"dry-run youtube {asset.name} title_chars={len(title)} desc_chars={len(description)} privacy={privacy}"

    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        from googleapiclient.http import MediaFileUpload
    except ImportError as exc:
        raise RuntimeError("Install deps: python -m pip install -r scripts/requirements.txt") from exc

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )
    creds.refresh(Request())
    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category,
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(str(asset), chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    try:
        while response is None:
            _, response = request.next_chunk()
    except HttpError as exc:
        raise RuntimeError(sanitize_error(exc.reason or str(exc))) from None
    video_id = response.get("id")
    if not video_id:
        raise RuntimeError("YouTube upload did not return a video id")
    return f"https://www.youtube.com/watch?v={video_id}"


def publish_one(post_id: str, *, dry_run: bool) -> str:
    fieldnames, rows, row = find_post(post_id)
    platform = (row.get("platform") or "").strip().lower()
    if platform not in {"instagram", "youtube"}:
        raise RuntimeError(f"{post_id} is {platform or 'unknown'}; live publish is Instagram and YouTube only")
    if (row.get("status") or "").strip().lower() == "posted" and not dry_run:
        raise RuntimeError(f"{post_id} is already posted")
    media_id = row.get("media_id") or ""
    if not media_id:
        raise RuntimeError(f"{post_id} has no media_id")
    asset = media_file(media_id)
    if platform == "instagram":
        permalink = publish_instagram(row, asset, dry_run=dry_run)
    else:
        permalink = publish_youtube(row, asset, dry_run=dry_run)
    if not dry_run:
        mark_posted(fieldnames, rows, post_id, permalink)
    return permalink


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish queued Instagram/YouTube posts")
    parser.add_argument("--post-id", action="append", dest="post_ids", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        for post_id in args.post_ids:
            result = publish_one(post_id, dry_run=args.dry_run)
            print(f"{post_id}\t{result}")
    except Exception as exc:  # noqa: BLE001 — CLI boundary
        print(sanitize_error(str(exc)), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
