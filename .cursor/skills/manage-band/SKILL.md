---
name: manage-band
description: Add, update, and list band members, gigs, and rehearsals in band/*.csv using name, role, date, venue, and status. Use when the user mentions members, gigs, shows, bookings, rehearsals, practice, or the band calendar.
---

# Manage band

## Files

- `band/members.csv` — people
- `band/gigs.csv` — shows
- `band/rehearsals.csv` — practice
- `band/CATEGORIES.md` — allowed statuses

## Columns

Members: `id,name,role,phone,email,status,notes,created_at,updated_at`

Gigs: `id,date,time,venue,city,status,setlist_path,notes,created_at,updated_at`

Rehearsals: `id,date,time,location,status,setlist_path,notes,created_at,updated_at`

## IDs

Read the matching CSV; next id is prefix + zero-padded four digits, one past the highest existing.

| Entity | Prefix | Example |
|--------|--------|---------|
| Member | `M` | `M0001` |
| Gig | `G` | `G0001` |
| Rehearsal | `R` | `R0001` |

## Add

1. Require or extract: **member name + role**, or **gig date + venue**, or rehearsal date + location.
2. Defaults: member `status=active`; gig `status=inquiry`; rehearsal `status=scheduled`.
3. Dates `YYYY-MM-DD`; times `HH:MM` 24h when known. `created_at` / `updated_at` = ISO date.
4. Append one CSV row; confirm with a one-line summary.
5. If a setlist is mentioned, create/link `setlists/` per `.cursor/skills/manage-setlists/SKILL.md`.

## Update

Match by id, name, venue+date, or phone. Update only changed fields. Always bump `updated_at`. Prefer statuses from `CATEGORIES.md`.

## List

Filter by status, date range, venue, or role. Compact table. Don’t rewrite the whole CSV unless merging duplicates the user asked for.

## Deduplicate

Same person (name+phone or name+role) or same gig (date+venue) → update, don’t duplicate; mention the match.
