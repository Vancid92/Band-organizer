---
name: manage-insurance
description: Add and update life insurance funnel stats (dials, pickups, presentations, applications, sales), prospects, and carrier/CRM account labels in insurance/*.csv. Use when the user mentions dials, pickups, presentations, applications, closes, policies, premiums, leads, prospects, or insurance production.
---

# Manage insurance

## Files

- `insurance/daily.csv` — production counts by day
- `insurance/prospects.csv` — people
- `insurance/activities.csv` — one row per touch
- `insurance/applications.csv` — submitted apps
- `insurance/sales.csv` — issued / counted sales
- `insurance/CATEGORIES.md` — allowed stages, types, statuses
- `config/insurance-accounts.csv` — carrier/CRM/dialer/email labels and URLs (no secrets)

## Columns

Daily: `id,date,dials,pickups,presentations,applications,sales,notes,created_at,updated_at`

Prospects: `id,name,phone,email,source,stage,notes,created_at,updated_at`

Activities: `id,date,time,prospect_id,type,outcome,notes,created_at`

Applications: `id,date,prospect_id,carrier,product,face_amount,monthly_premium,annual_premium,status,notes,created_at,updated_at`

Sales: `id,date,prospect_id,application_id,carrier,product,monthly_premium,annual_premium,status,notes,created_at,updated_at`

Accounts: `kind,name,url,notes`

## IDs

Read the matching CSV; next id is prefix + zero-padded four digits, one past the highest existing.

| Entity | Prefix | Example |
|--------|--------|---------|
| Daily | `D` | `D0001` |
| Prospect | `L` | `L0001` |
| Activity | `T` | `T0001` |
| Application | `N` | `N0001` |
| Sale | `C` | `C0001` |

## Privacy

- Do not invent names, phones, emails, policy numbers, or portal URLs.
- Do not store SSN, DOB, medical, bank, or login secrets. If the user dumps those, keep them out of CSVs and say so.
- Do not log into carrier, CRM, email, or dialer accounts. Queue and file only.
- Do not scan Outlook, browser profiles, or Windows credentials unless the user names a specific file to import.

## Daily dump (counts only)

User: “80 dials, 12 pickups, 3 presentations, 1 app today.”

1. Date = stated date, else today (`YYYY-MM-DD`).
2. If `insurance/daily.csv` already has that date, **add** the new counts to the existing numbers (same day, more work) unless they say “replace” or “correction.”
3. Otherwise append a row. Empty count fields = `0`.
4. Recap counts + conversion rates from `CATEGORIES.md`.

## Named people

Require **name** when logging a person. Phone/email/source when known.

1. Match existing prospect by id, name+phone, or exact name. Update; don’t duplicate.
2. Default new `stage=lead`.
3. Log an `activities.csv` row for the step they described.
4. Move `stage` forward to match the furthest step: pickup → `pickup`, presentation → `presented`, application → `applied`, sale → `sold`.
5. Application mentioned → append `applications.csv` (`status=submitted` unless they say otherwise). Required when known: **prospect + date**. Carrier/product/premium if given.
6. Sale mentioned → append `sales.csv` (`status=issued` unless they say otherwise). Link `application_id` when it exists. Required when known: **prospect + date**.
7. Also bump that day’s `daily.csv` counts for each new activity type unless they said the daily totals already include it.

## Accounts

When they name a carrier, CRM, dialer, or paste a portal URL: fill `config/insurance-accounts.csv`. Match `kind` from `CATEGORIES.md`. Never write passwords. Ask before adding a new `kind`.

## List / recap

Filter by date range, stage, carrier, or type. Compact table. For a range, sum `daily.csv` and show conversion rates. Don’t rewrite whole CSVs unless merging duplicates they asked for.

## Import

If they point at a spreadsheet or CSV path, map columns onto these files. Skip SSN/DOB/medical/bank columns. Confirm row counts after import.
