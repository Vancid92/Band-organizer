---
name: manage-setlists
description: Add and update songs in band/songs.csv and write setlist markdown under setlists/. Use when the user mentions songs, covers, originals, keys, setlists, set order, or what to play at a gig or rehearsal.
---

# Manage setlists

## Files

- `band/songs.csv` — catalog
- `setlists/<YYYY-MM-DD>-<venue-slug>.md` — one file per set
- `band/gigs.csv` / `band/rehearsals.csv` — `setlist_path` points at the file
- `band/CATEGORIES.md` — song statuses

## Song columns

`id,title,artist,key,duration,status,notes,created_at,updated_at`

IDs: `S` + zero-padded number (`S0001`). Increment from the highest existing `S` id.

Leave `artist` blank for originals. Duration like `3:42` when known.

## Add / update a song

1. Match by title (case-insensitive) before inserting.
2. Default `status=learning` unless they clearly play it (`ready`).
3. Require **title** when known; capture key, artist, duration.
4. Append or patch one row; bump `updated_at`.

## Write a setlist

1. Filename: `setlists/YYYY-MM-DD-<venue-or-rehearsal-slug>.md`. Reuse the same-day file for that venue.
2. Resolve each song to an `S` id (create the song row if missing).
3. Use this template:

```markdown
# Setlist — <Venue or rehearsal>
- Date: YYYY-MM-DD
- Gig / rehearsal: G0001 or R0001

## Set 1
1. Song title (S0001) — key
2. ...

## Encore
1. ...

## Notes
- Target runtime:
-
```

4. Set `setlist_path` on the gig or rehearsal row if one exists.
5. Recap song count + estimated runtime if durations are known.
