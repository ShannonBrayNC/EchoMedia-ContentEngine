# Book II Expansion Branch Recovery Audit

## Purpose

This audit records the current state of Book II expansion work after the ElevenLabs export remained novella-length and the expected full expansion was not present in the uploaded export.

## Current Finding

Book II has multiple completed drafting and expansion records, but the full novel-length expansion is not fully present in the current reader/export artifact.

The important distinction is:

- drafting sprints completed the 24-chapter manuscript;
- targeted expansion sprints 1 and 2 appear to have been synced to the default branch;
- targeted expansion sprint 3 is documented as implemented on a branch, but the named branch currently does not contain unique manuscript changes ahead of `main`.

## Branch and Issue Audit

### Drafting Sprints

The following drafting PRs were merged into `main`:

- PR #138 — Drafted Chapters 5-8.
- PR #140 — Drafted Chapters 9-12.
- PR #141 — Drafted Chapters 13-16.

PR #153 for Chapters 17-20 was closed unmerged as superseded because current `main` was documented as already containing stronger drafted versions for those chapters.

### Targeted Expansion Plan

Issue #145 records the targeted Book II expansion plan and sprint order:

1. Sprint 1: Chapters 13, 9, and 14.
2. Sprint 2: Chapters 6, 10, and 11.
3. Sprint 3: Chapters 5, 7, 8, 12, 15, and 18.

### Expansion Sprint 1

Issue #146 records Expansion Sprint 1 as completed and synced to the default branch.

Covered chapters:

- Chapter 9 — The Treaty Surface
- Chapter 13 — Delegated Answer
- Chapter 14 — The Libertarian Fire

### Expansion Sprint 2

Issue #147 records Expansion Sprint 2 as completed and synced to the default branch.

Covered chapters:

- Chapter 6 — Premium Refusal
- Chapter 10 — Translation Threat
- Chapter 11 — The Better Wrong

### Expansion Sprint 3

Issue #148 records Expansion Sprint 3 as implemented on branch `codex/book-ii-expansion-sprint-3` and validated locally.

Covered chapters:

- Chapter 5 — Consent Agent
- Chapter 7 — The Relief Corridor
- Chapter 8 — Represented Consent
- Chapter 12 — Whole Record
- Chapter 15 — The Gift That Owns
- Chapter 18 — The Fast Country

However, a live GitHub compare currently shows:

```text
main -> codex/book-ii-expansion-sprint-3
status: behind
ahead_by: 0
behind_by: 48
files changed: 0
```

Comparing from the old branch base also shows the branch is identical to the older merge-base commit:

```text
db7a51654b70d5a00db7ae50fcdf243b6bb8f73c -> codex/book-ii-expansion-sprint-3
status: identical
ahead_by: 0
behind_by: 0
```

Conclusion: the named Sprint 3 branch exists, but the expected Sprint 3 manuscript delta is no longer present on that branch.

### Separate Chapter 5 Expansion Branch

A separate branch exists:

```text
codex/book-ii-novel-expansion-ch05-08
```

Current compare against `main` shows it contains four unique commits and these Book II changes:

- `projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-05-consent-agent.md`
- `projects/lantern-protocol/novel/book-ii/exports/chapters/chapter-05-consent-agent-elevenlabs-expanded.md`
- `projects/lantern-protocol/novel/book-ii/scripts/export-expanded-elevenlabs.ps1`

It does not contain Sprint 3 recovery for Chapters 7, 8, 12, 15, or 18.

## Export Finding

The uploaded expanded Book II ElevenLabs export contains the Chapter 5 expansion markers and is about 29.9k words. That confirms Chapter 5 sidecar replacement worked, but it does not represent full novel-length expansion.

Expected current state:

- Current export remains novella-length.
- Chapter 5 expansion alone is insufficient to move Book II to 40k+.
- Sprint 3 recovery and/or additional Sprints 4/5 are still required.

## Recovery Recommendation

### Step 1 — Recover Sprint 3 deliberately

Do not merge `codex/book-ii-expansion-sprint-3` as-is. It has no useful unique manuscript delta.

Create a new recovery branch from current `main` and re-apply/rewrite Sprint 3 expansions for:

1. Chapter 5 — Consent Agent
2. Chapter 7 — The Relief Corridor
3. Chapter 8 — Represented Consent
4. Chapter 12 — Whole Record
5. Chapter 15 — The Gift That Owns
6. Chapter 18 — The Fast Country

Chapter 5 may be recovered from `codex/book-ii-novel-expansion-ch05-08`.

### Step 2 — Regenerate exports

After Sprint 3 recovery, run:

```powershell
node projects/lantern-protocol/novel/scripts/assemble-and-audit-lantern-ii.mjs
```

Regenerate at minimum:

- `projects/lantern-protocol/novel/book-ii/exports/lantern-protocol-ii-elevenlabs.md`
- `projects/lantern-protocol/novel/book-ii/exports/lantern-ii-novel-report.md`
- `projects/lantern-protocol/novel/book-ii/exports/lantern-ii-chapter-status.json`

### Step 3 — Check word count

Review:

```text
projects/lantern-protocol/novel/book-ii/exports/lantern-ii-novel-report.md
```

Book II should not be treated as final novel-length until it crosses at least 40,000 words.

### Step 4 — Decide on Sprint 4/5

If recovered Sprint 3 does not bring Book II to 40k+, create additional expansion issues for compressed chapters outside the original targeted plan.

Likely future targets:

- Chapter 16 — The Civic Mirror Trial
- Chapter 17 — The Mercy Bloc Ultimatum
- Chapter 19 — Names Across the Border
- Chapter 20 — Authority Laundering
- Chapter 21 — The Memory Registry
- Chapter 22 — Rememberer Score

## Status

Book II is not currently final for novel-length ElevenLabs/KDP export.

Current blocker: recover or rewrite Sprint 3, regenerate exports, then re-check total word count.
