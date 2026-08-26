# Band categories

Use values from this list in the CSVs. Prefer lowercase snake_case. Ask before adding a new status unless it is obviously needed.

## Gig status (`band/gigs.csv`)

| Status | Meaning |
|--------|---------|
| `inquiry` | Date/venue floated; not locked |
| `confirmed` | Booked |
| `played` | Done |
| `cancelled` | Off the books |

## Rehearsal status (`band/rehearsals.csv`)

| Status | Meaning |
|--------|---------|
| `scheduled` | On the calendar |
| `done` | Happened |
| `cancelled` | Called off |

## Member status (`band/members.csv`)

| Status | Meaning |
|--------|---------|
| `active` | Current member |
| `inactive` | Not playing right now |
| `substitute` | Fill-in |

## Member role

Examples: `vocals`, `guitar`, `bass`, `drums`, `keys`, `other`. Combine with a space-free qualifier if needed (`lead_vocals`, `rhythm_guitar`).

## Song status (`band/songs.csv`)

| Status | Meaning |
|--------|---------|
| `learning` | Not ready for a gig |
| `ready` | Can put on a set |
| `retired` | Off the list |

## Post status (`social/posts.csv`)

| Status | Meaning |
|--------|---------|
| `queued` | Draft ready; you still publish |
| `posted` | You confirmed it went live |
| `skipped` | Not posting this platform |

## Platforms

`instagram`, `facebook`, `tiktok`, `x`, `youtube`, `threads`. Ask before inventing a new platform row in `config/socials.csv`.
