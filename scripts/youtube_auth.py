"""One-time YouTube OAuth. Writes YOUTUBE_REFRESH_TOKEN into config/youtube.env.

Does not print tokens. Run from the repo root:
    python scripts/youtube_auth.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / "config" / "youtube.env"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


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


def upsert_env(path: Path, key: str, value: str) -> None:
    lines: list[str] = []
    found = False
    if path.is_file():
        for raw in path.read_text(encoding="utf-8").splitlines():
            if raw.strip().startswith(f"{key}="):
                lines.append(f"{key}={value}")
                found = True
            else:
                lines.append(raw)
    if not found:
        if lines and lines[-1].strip():
            lines.append("")
        lines.append(f"{key}={value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    env = load_env(ENV_PATH)
    client_id = env.get("YOUTUBE_CLIENT_ID") or ""
    client_secret = env.get("YOUTUBE_CLIENT_SECRET") or ""
    if not client_id or not client_secret:
        print(
            "Missing YOUTUBE_CLIENT_ID or YOUTUBE_CLIENT_SECRET in config/youtube.env",
            file=sys.stderr,
        )
        print("Copy config/youtube.example.env to config/youtube.env and fill those two fields.", file=sys.stderr)
        return 1

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("Install deps: python -m pip install -r scripts/requirements.txt", file=sys.stderr)
        return 1

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent")
    if not creds.refresh_token:
        print("Google did not return a refresh token. Revoke app access and retry.", file=sys.stderr)
        return 1
    upsert_env(ENV_PATH, "YOUTUBE_REFRESH_TOKEN", creds.refresh_token)
    print("Saved YOUTUBE_REFRESH_TOKEN to config/youtube.env")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
