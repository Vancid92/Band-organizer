# Band organizer

Workspace for members, gigs, rehearsals, songs/setlists, and a **queue-only** social post pipeline. Dump notes or files in chat; the agent writes CSVs and markdown. You publish from drafts until APIs exist.

## Quick start

1. Open this folder in Cursor.
2. Fill profile URLs in [`config/socials.csv`](config/socials.csv) (Instagram, Facebook, TikTok, X, YouTube, Threads).
3. Tell the agent things like:

   - “Add member: Alex, drums, phone …”
   - “Gig Saturday at The Hideout, 9pm, confirmed”
   - “Rehearsal Thursday 7pm at the practice space — run the Saturday set”
   - “New song: Neon River, key of G, we’re learning it”
   - “Setlist for The Hideout: …”
   - Drop a photo/video and: “Queue this for Instagram and Facebook”
   - “Posted on Instagram”

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

## Media and posting (v1)

1. Drop a file in `media/inbox/` or attach it in chat.
2. Name platforms (or paste profile URLs).
3. The agent files the asset as `A0001-slug.ext` in `media/library/`, drafts captions, and appends one `social/posts.csv` row **per platform** with `status=queued`.
4. You post yourself. Then say “posted on Instagram” so that row becomes `posted`.

The agent does **not** log into socials or publish.

## Out of scope for now

Finances, merch, gear inventories, and live publish APIs.
