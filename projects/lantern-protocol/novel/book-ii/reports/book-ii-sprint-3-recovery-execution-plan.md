# Book II Sprint 3 Recovery Execution Plan

## Recovery Objective

Recover the missing Book II targeted expansion Sprint 3 work and regenerate the Book II ElevenLabs/KDP exports after the prose is restored.

This exists because the original issue record says Sprint 3 was implemented on `codex/book-ii-expansion-sprint-3`, but the live branch currently has no useful delta against the old merge base and is behind current `main`.

## Active Recovery Branch

```text
codex/book-ii-expansion-recovery-audit
```

This branch was created from current `main` at:

```text
4603e1694f36d35e42bd7f8420d4b4fad3ff36fa
```

## Known Recoverable Work

Chapter 5 has a separate recoverable expansion branch:

```text
codex/book-ii-novel-expansion-ch05-08
```

Useful files from that branch:

- `projects/lantern-protocol/novel/book-ii/manuscript/chapters/chapter-05-consent-agent.md`
- `projects/lantern-protocol/novel/book-ii/exports/chapters/chapter-05-consent-agent-elevenlabs-expanded.md`
- `projects/lantern-protocol/novel/book-ii/scripts/export-expanded-elevenlabs.ps1`

## Sprint 3 Recovery Scope

Re-apply or rewrite targeted expansions for these chapters:

1. `chapter-05-consent-agent.md`
2. `chapter-07-the-relief-corridor.md`
3. `chapter-08-represented-consent.md`
4. `chapter-12-whole-record.md`
5. `chapter-15-the-gift-that-owns.md`
6. `chapter-18-the-fast-country.md`

## Expansion Style Requirements

The recovery pass should preserve the user-approved direction:

- puzzle-thriller architecture;
- civic horror;
- escalating investigation;
- personal dread under ordinary interfaces;
- concrete human consequence;
- Kaito remains dangerous because he is partly right, not cartoon evil;
- Civic Mirror remains useful and morally difficult, not villainous;
- doctrine remains: `Agreement is not consent when stacked into coercion.`

Do not imitate any specific author. Use high-level genre traits: puzzles, clues, investigative turns, dread, escalating reveals, and slow-bloom institutional horror.

## Required Export Regeneration

After prose recovery is complete, run:

```powershell
node projects/lantern-protocol/novel/scripts/assemble-and-audit-lantern-ii.mjs
```

Then verify/update:

- `projects/lantern-protocol/novel/book-ii/exports/lantern-protocol-ii-elevenlabs.md`
- `projects/lantern-protocol/novel/book-ii/exports/lantern-ii-novel-report.md`
- `projects/lantern-protocol/novel/book-ii/exports/lantern-ii-chapter-status.json`

## Acceptance Criteria

- Sprint 3 chapters are expanded in canonical manuscript files.
- Full Book II ElevenLabs export includes all recovered expansion prose.
- `lantern-ii-novel-report.md` shows updated chapter word counts.
- Total word count is reassessed against:
  - minimum novel target: 40,000 words;
  - stronger thriller/horror target: 55,000-65,000+ words.
- If total remains under 40,000 words, create Sprint 4/5 for additional expansion.

## Current Status

This execution plan is now tracked in-repo.

Next action: recover Chapter 5 from the known branch and expand Chapters 7, 8, 12, 15, and 18 on top of current `main`.
