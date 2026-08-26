---
name: live-publish
description: Publish queued Instagram and YouTube posts via Graph API and YouTube Data API using config/instagram.env and config/youtube.env. Use when the user says publish, post live, post now, upload to YouTube, or post to Instagram.
---

# Live publish (Instagram + YouTube)

Only when the user **explicitly** asks to publish/post live. Dumps still queue first. Do **not** log into socials in a browser. Do **not** print tokens, env files, or API headers.

Setup: `social/LIVE_PUBLISH.md`

## Gate

1. Identify `social/posts.csv` rows (`P0001` or media + platform). Queue via `.cursor/skills/media-queue/SKILL.md` if missing.
2. Platforms: `instagram` and `youtube` only. Other platforms stay `queued` — tell the user to post those by hand.
3. Config:
   - Instagram → `config/instagram.env` (from `config/instagram.example.env`)
   - YouTube → `config/youtube.env` (from `config/youtube.example.env`) plus `python scripts/youtube_auth.py` once
4. If env is missing, stop and point at `social/LIVE_PUBLISH.md`. Do not guess tokens.

## Publish

From repo root (never `echo` env or `--verbose` that dumps bodies):

```
python scripts/publish.py --post-id P0001
```

Multiple ids: repeat `--post-id`. Optional `--dry-run` to check file + caption length without calling APIs.

The script updates that row to `status=posted`, sets `posted_at`, and writes `permalink: ...` into `notes`.

## Recap

File saved, which platforms went live (with permalinks from the script stdout), which stayed queued, next action.

## Photos on Instagram

Local stills need a public HTTPS URL (`INSTAGRAM_PUBLIC_MEDIA_BASE_URL` or `image_url:` in notes). Reels/video upload from `media/library/`. YouTube always uploads the local file.

## Failures

Leave the row `queued`. Quote only the script’s short stderr (already sanitized). Do not retry in a loop.
