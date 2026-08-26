# Social platforms

Queue-only in v1: draft copy here, then the user publishes. One `social/posts.csv` row per platform.

Fill handles/URLs in [`config/socials.csv`](../config/socials.csv). Do not invent profile URLs.

## Field notes

| Platform | Caption | Extra fields |
|----------|---------|--------------|
| `instagram` | ~2,200 characters; first ~125 show before “more”. Aim 1–3 short paragraphs + line-break hashtags. | Square/4:5 stills; Reels as `video`. |
| `facebook` | Long captions OK; lead with the hook in the first 2 lines. | Link in caption is fine. |
| `tiktok` | ~4,000 characters; first ~150 matter. Native vertical video. | On-screen text ≠ caption; keep caption punchy. |
| `x` | **280 characters** for the queued draft (Premium limits are higher; still keep a short variant). | No title field. Put the link last. |
| `youtube` | Caption column = **description** (up to ~5,000). Put a **title** (≤100 chars) on the first line of `notes` as `title: ...`. | Needs `video`. |
| `threads` | ~500 characters. Closer to a short Instagram caption than a tweet. | |

## Drafting

- Write a full Instagram/Facebook/Threads-style caption, then a **short X variant**.
- YouTube: title in `notes`, description in `caption`.
- Don’t stuff every hashtag onto X.
- `status=queued` until the user says it was posted; then `posted` + `posted_at`.
