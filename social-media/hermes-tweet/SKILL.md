---
name: hermes-tweet
description: "Use Hermes Tweet for X/Twitter research, drafting, read checks, and gated account actions from Hermes Agent."
version: 1.0.0
author: Xquik-dev
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [x, twitter, social-media, hermes-plugin, posting, monitoring]
    homepage: https://github.com/Xquik-dev/hermes-tweet
---

# Hermes Tweet

Use this skill when the user asks Hermes to plan, draft, review, research, or
post X/Twitter content through the Hermes Tweet plugin.

## Setup

Install the plugin:

```bash
hermes plugins install Xquik-dev/hermes-tweet
```

Configure credentials in the runtime environment, not in chat:

```bash
export XQUIK_API_KEY="your_api_key"
```

Enable account-changing actions only when needed:

```bash
export HERMES_TWEET_ENABLE_ACTIONS=true
```

## Trigger Conditions

Use this skill for:

- drafting posts, replies, quote posts, and threads
- checking live X/Twitter context before drafting
- turning longer research into concise social posts
- reviewing social content for tone, safety, and clarity
- posting or account actions only after explicit confirmation

## Procedure

1. Decide whether the task is draft-only, live-read, or action-capable.
2. If draft-only, write the post/thread and explain any assumptions.
3. If live-read, require `XQUIK_API_KEY` and fetch only the needed context.
4. If action-capable, require both `XQUIK_API_KEY` and
   `HERMES_TWEET_ENABLE_ACTIONS=true`.
5. Before any write action, show the exact final text or target and ask the
   user to confirm.
6. After an action, report the result and any returned post IDs or links.

## Pitfalls

- Do not ask users to paste API keys, cookies, or tokens into chat.
- Do not perform account-changing actions from an inferred intent.
- Do not publish drafts until the user approves the exact final copy.
- Treat missing credentials as draft-only mode.

## Verification

- Confirm the plugin repository is installed:
  https://github.com/Xquik-dev/hermes-tweet
- Confirm `XQUIK_API_KEY` before live reads.
- Confirm `HERMES_TWEET_ENABLE_ACTIONS=true` before write actions.
