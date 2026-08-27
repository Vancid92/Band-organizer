# Band organizer

Workspace for band ops: members, gigs, rehearsals, songs/setlists, and a **queue-only** social media pipeline. Dump notes or media in chat; the agent writes CSVs and markdown. You publish the posts yourself.

## Quick start

1. Open this folder in Cursor.
2. Fill profile URLs in [`config/socials.csv`](config/socials.csv) (Instagram, Facebook, TikTok, X, YouTube, Threads).
3. Tell the agent things like:
   - “Add member: Alex, drums, active”
   - “Gig inquiry Saturday at The Hideout, 9pm”
   - “Rehearsal Thursday 7pm at the practice space — run the bar set”
   - “Add song: Fast Car, Tracy Chapman, key G”
   - “Here’s a clip — queue it for Instagram, TikTok, and YouTube”
   - “Show confirmed gigs” / “What’s in the social queue?”
   - “Posted on Instagram”
4. Drop leftover photos/videos in `media/inbox/` if you are not attaching them in chat.

## Source of truth

| What | Where |
|------|--------|
| Members, gigs, rehearsals, songs | [`band/`](band/) |
| Allowed statuses | [`band/CATEGORIES.md`](band/CATEGORIES.md) |
| Setlists | [`setlists/`](setlists/) |
| Social profile URLs | [`config/socials.csv`](config/socials.csv) |
| Media catalog | [`media/media.csv`](media/media.csv) |
| Filed assets | `media/library/` (`A0001-slug.ext`) |
| Inbox | `media/inbox/` |
| Post queue | [`social/posts.csv`](social/posts.csv) |
| Caption limits | [`social/PLATFORMS.md`](social/PLATFORMS.md) |

## IDs

`M` members · `G` gigs · `R` rehearsals · `S` songs · `A` media assets · `P` posts — zero-padded (`G0001`).

## Publishing

v1 is **queue-only**. The agent saves the file, drafts captions, and records which profile URLs to hit. It does not log in or post. After you publish, tell it which platform went live so it can mark that row `posted`.
