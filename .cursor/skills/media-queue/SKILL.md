---
name: media-queue
description: Intake photos/videos, file them in media/library, draft captions, and queue per-platform rows in social/posts.csv. Use when the user dumps media, drops files in media/inbox, names Instagram/Facebook/TikTok/X/YouTube/Threads, pastes profile URLs, or says a post was published.
---

# Media queue

Queue first. Do **not** log into socials or drive a browser to post. Call publish APIs only when the user explicitly asks to publish — then follow `.cursor/skills/live-publish/SKILL.md` (Instagram + YouTube).

## Files

- `media/inbox/` — unsorted drops
- `media/library/` — filed assets `A0001-slug.ext`
- `media/media.csv` — `id,filename,type,caption_notes,created_at`
- `config/socials.csv` — `platform,handle,url` (six starter rows)
- `social/posts.csv` — `id,media_id,platform,profile_url,caption,status,scheduled_for,posted_at,notes`
- `social/PLATFORMS.md` — caption limits

## IDs

- Assets: `A` (`A0001`) — next id from `media/media.csv`
- Posts: `P` (`P0001`) — next id from `social/posts.csv` (one id per **platform row**, not per asset)

## Dump-to-queue workflow

When the user attaches a photo/video, points at `media/inbox/`, and/or names platforms / pastes profile URLs:

1. **File the asset**
   - Copy into `media/library/` as `A0001-slug.ext` (slug from a short descriptive name; keep the original extension).
   - `type`: `photo` / `video` / `audio` / `other`.
   - Append `media/media.csv`. If the source was `media/inbox/`, remove the inbox copy after a successful library write.
2. **Resolve destinations**
   - Platforms from the user’s list, else all rows in `config/socials.csv` that have a `url`.
   - Look up `profile_url` from `config/socials.csv`. Extra URLs the user pastes win for that platform.
   - Unknown platform or empty url with no pasted link → **ask** before inventing a `config/socials.csv` row.
3. **Draft copy** (see `PLATFORMS.md`)
   - Instagram/Facebook/Threads: full caption.
   - X: short ≤280-character variant (own row).
   - YouTube: `caption` = description; `notes` starts with `title: ...` (≤100 chars).
4. **Queue rows**
   - One `social/posts.csv` row **per platform** so Instagram can stay `queued` while Facebook is `posted`.
   - `status=queued`. Escape commas/newlines in captions with CSV quoting.
5. **Recap** — file saved, queued platforms, draft copy (or where to read it), next action: publish live (Instagram/YouTube) or post the rest by hand.

## Mark posted

If they say “posted on Instagram” after doing it themselves: match `media_id` + `platform`, set `status=posted` and `posted_at` to today’s ISO date. If they ask to **publish live**, use `.cursor/skills/live-publish/SKILL.md` instead of hand-marking.

## Required when known

Media file + which platforms.
