# Insurance categories

Use values from this list in the CSVs. Prefer lowercase snake_case. Ask before adding a new status unless it is obviously needed.

Funnel (in order): **dials → pickups → presentation → application → sales**.

| Spoken | CSV `type` / daily column |
|--------|---------------------------|
| Dials | `dial` / `dials` |
| Pick ups | `pickup` / `pickups` |
| Presentation (presitation) | `presentation` / `presentations` |
| Close — application | `application` / `applications` |
| Sales | `sale` / `sales` |

## Daily production (`insurance/daily.csv`)

One row per calendar day. Counts are integers. Upsert on `date`; do not add a second row for the same day.

## Prospect stage (`insurance/prospects.csv`)

| Stage | Meaning |
|-------|---------|
| `lead` | On the list; not yet a live conversation |
| `dialed` | Called; no pickup |
| `pickup` | Answered |
| `presented` | Presentation happened |
| `applied` | Application submitted |
| `sold` | Policy issued / counted as a sale |
| `callback` | Asked to follow up |
| `not_interested` | Declined |
| `unresponsive` | No answer after attempts |

Advance stage forward with the funnel; do not move it backward unless the user says the earlier step was a mistake.

## Activity type (`insurance/activities.csv`)

`dial`, `pickup`, `presentation`, `application`, `sale`, `follow_up`.

## Application status (`insurance/applications.csv`)

| Status | Meaning |
|--------|---------|
| `submitted` | App in |
| `pending` | Underwriting / requirements |
| `issued` | Carrier issued |
| `declined` | Carrier declined |
| `withdrawn` | Client or agent pulled it |

## Sale status (`insurance/sales.csv`)

| Status | Meaning |
|--------|---------|
| `issued` | Counted as a sale |
| `delivered` | Policy in client hands |
| `paid` | Commission / premium confirmed |
| `lapsed` | Dropped after issue |
| `cancelled` | Not taken / cancelled |

## Account kind (`config/insurance-accounts.csv`)

`carrier`, `crm`, `dialer`, `email`, `calendar`, `licensing`, `other`.

URLs and labels only. Never store passwords, tokens, or security answers.

## Prospect source

Examples: `referral`, `cold_call`, `warm_call`, `inbound`, `social`, `event`, `other`.

## Conversion (when recapping a day or range)

- Pickup rate = pickups / dials
- Presentation rate = presentations / pickups
- App rate = applications / presentations
- Close rate = sales / applications

If a denominator is 0, say “n/a” instead of dividing.
