# Band organizer

Workspace for members, gigs, rehearsals, songs/setlists, and a social post pipeline. Dump notes or files in chat; the agent writes CSVs and markdown. Instagram and YouTube can publish live when env is configured; other platforms stay queue-only.

## Quick start

1. Open this folder in Cursor.
2. Fill profile URLs in [`config/socials.csv`](config/socials.csv) (Instagram, Facebook, TikTok, X, YouTube, Threads).
3. Tell the agent things like:

   - “Add member: Alex, drums, phone …”
   - “Gig Saturday at The Hideout, 9pm, confirmed”
   - “Rehearsal Thursday 7pm at the practice space — run the Saturday set”
   - “New song: Neon River, key of G, we’re learning it”
   - “Setlist for The Hideout: …”
   - Drop a photo/video and: “Queue this for Instagram and YouTube”
   - “Publish P0001 to Instagram” / “Posted on Instagram”

4. Master files live under [`band/`](band/), [`setlists/`](setlists/), [`media/`](media/), and [`social/`](social/).

## What is tracked

| Area | File | IDs |
|------|------|-----|
| Members | [`band/members.csv`](band/members.csv) | `M0001` |
| Gigs | [`band/gigs.csv`](band/gigs.csv) | `G0001` |
| Rehearsals | [`band/rehearsals.csv`](band/rehearsals.csv) | `R0001` |
| Songs | [`band/songs.csv`](band/songs.csv) | `S0001` |
| Media | [`media/media.csv`](media/media.csv) + [`media/library/`](media/library/) | `A0001` |
| Social queue | [`social/posts.csv`](social/posts.csv) | `P0001` |

Statuses: [`band/CATEGORIES.md`](band/CATEGORIES.md). Caption limits: [`social/PLATFORMS.md`](social/PLATFORMS.md).

## Media and posting

1. Drop a file in `media/inbox/` or attach it in chat.
2. Name platforms (or paste profile URLs).
3. The agent files the asset as `A0001-slug.ext` in `media/library/`, drafts captions, and appends one `social/posts.csv` row **per platform** with `status=queued`.
4. **Instagram / YouTube live:** say “publish this” after env is set up ([`social/LIVE_PUBLISH.md`](social/LIVE_PUBLISH.md)). Other networks: you post, then say “posted on Facebook”.

The agent does **not** log into socials in a browser. Tokens stay in gitignored `config/*.env`.

## Out of scope for now

Finances, merch, gear inventories, and live APIs for Facebook, TikTok, X, and Threads.
