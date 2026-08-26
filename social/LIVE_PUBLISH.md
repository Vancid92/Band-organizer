# Live publish — Instagram and YouTube

Queue first (`social/posts.csv`), then say **publish** / **post this live**. The agent runs `scripts/publish.py` and marks rows `posted`. Facebook, TikTok, X, and Threads stay queue-only.

Copy example env files; never commit `*.env` or paste tokens in chat.

```
config/instagram.example.env  →  config/instagram.env
config/youtube.example.env    →  config/youtube.env
```

Install YouTube libs once (Instagram uses the stdlib only):

```
python -m pip install -r scripts/requirements.txt
```

## Instagram

Needs an **Instagram professional** account (Business or Creator) linked to a **Facebook Page**, plus a Meta app with Instagram Graph API.

1. [Meta for Developers](https://developers.facebook.com/apps/) — create an app, add **Instagram** / Graph API.
2. Add yourself as an app tester if the app is in Development.
3. In [Graph API Explorer](https://developers.facebook.com/tools/explorer/), generate a **Page** token with:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
   - `pages_read_engagement`
4. Exchange it for a long-lived token (≈60 days). Put that in `INSTAGRAM_ACCESS_TOKEN`.
5. Resolve the IG user id (not the @handle):

   `GET /{page-id}?fields=instagram_business_account`

   Put `instagram_business_account.id` in `INSTAGRAM_USER_ID`.

**Photos:** Graph API only accepts a **public HTTPS** `image_url`. Either set `INSTAGRAM_PUBLIC_MEDIA_BASE_URL` so the script uses `{base}/{library-filename}`, or put `image_url: https://...` in the post `notes`. Local JPGs are not uploaded.

**Video / Reels:** local files in `media/library/` upload via Meta’s resumable API.

## YouTube

1. [Google Cloud Console](https://console.cloud.google.com/) — new project, enable **YouTube Data API v3**.
2. OAuth consent screen (External is fine). Add your channel Google account as a **test user**.
3. Create an OAuth client: **Desktop app**. Copy client id + secret into `youtube.env`.
4. From the repo root:

   `python scripts/youtube_auth.py`

   Sign in as the channel account. The script writes `YOUTUBE_REFRESH_TOKEN` into `youtube.env` (it does not print the token).

Default privacy is **unlisted** (`YOUTUBE_PRIVACY_STATUS`). Change to `public` when you want that.

## Commands the agent runs

```
python scripts/publish.py --post-id P0001
python scripts/publish.py --post-id P0001 --post-id P0002
python scripts/publish.py --post-id P0001 --dry-run
```

`--dry-run` checks file + caption length only; it does not call APIs.
