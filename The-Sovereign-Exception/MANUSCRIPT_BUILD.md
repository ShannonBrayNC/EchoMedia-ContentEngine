# The Sovereign Exception - Manuscript Build

## Status

**First prose draft complete.**

This file defines the canonical manuscript order for building the full combined draft from the prologue and Chapters 1-40.

> Build note: The full combined manuscript should be generated from the source chapter files rather than manually pasted into one giant file. This preserves clean chapter-level editing while enabling export to Markdown, DOCX, PDF, screenplay, audio scripts, and production packages.

---

# Canonical Manuscript Order

| Order | Title | Source File |
|---:|---|---|
| 0 | Prologue - The Green Map | `NOVEL_DRAFT.md` |
| 1 | Mara Vale Receives the Audit | `chapters/chapter-001-mara-vale-receives-the-audit.md` |
| 2 | Naomi Bell Finds the First Waiver | `chapters/chapter-002-naomi-bell-finds-the-first-waiver.md` |
| 3 | Senator Cross Opens the Hearing | `chapters/chapter-003-senator-cross-opens-the-hearing.md` |
| 4 | The Man Nobody Wants in the Room | `chapters/chapter-004-the-man-nobody-wants-in-the-room.md` |
| 5 | Juno Maps the Consent Surface | `chapters/chapter-005-juno-maps-the-consent-surface.md` |
| 6 | Thorne's Doctrine | `chapters/chapter-006-thornes-doctrine.md` |
| 7 | Iris Sees the Inversion | `chapters/chapter-007-iris-sees-the-inversion.md` |
| 8 | A Second Signal | `chapters/chapter-008-a-second-signal.md` |
| 9 | The Geneva Continuity Framework | `chapters/chapter-009-the-geneva-continuity-framework.md` |
| 10 | Cross and the Redacted Room | `chapters/chapter-010-cross-and-the-redacted-room.md` |
| 11 | Elias Builds the Authority Map | `chapters/chapter-011-elias-builds-the-authority-map.md` |
| 12 | Juno Breaks the Demo | `chapters/chapter-012-juno-breaks-the-demo.md` |
| 13 | Mara and Admiral Ward | `chapters/chapter-013-mara-and-admiral-ward.md` |
| 14 | The Dead Engineer's Key | `chapters/chapter-014-the-dead-engineers-key.md` |
| 15 | Iris Opens the Archive | `chapters/chapter-015-iris-opens-the-archive.md` |
| 16 | Thorne Counts the Dead | `chapters/chapter-016-thorne-counts-the-dead.md` |
| 17 | The Annex | `chapters/chapter-017-the-annex.md` |
| 18 | Small Fires | `chapters/chapter-018-small-fires.md` |
| 19 | Mara Uses the Machine | `chapters/chapter-019-mara-uses-the-machine.md` |
| 20 | Juno Names the Crime | `chapters/chapter-020-juno-names-the-crime.md` |
| 21 | Elias and Father Tomas | `chapters/chapter-021-elias-and-father-tomas.md` |
| 22 | The Ethics Memo | `chapters/chapter-022-the-ethics-memo.md` |
| 23 | Cross Goes Public | `chapters/chapter-023-cross-goes-public.md` |
| 24 | Thorne Makes the Case | `chapters/chapter-024-thorne-makes-the-case.md` |
| 25 | Three Theaters | `chapters/chapter-025-three-theaters.md` |
| 26 | The Order | `chapters/chapter-026-the-order.md` |
| 27 | Naomi Releases the Trail | `chapters/chapter-027-naomi-releases-the-trail.md` |
| 28 | Juno Attacks the Consent Clock | `chapters/chapter-028-juno-attacks-the-consent-clock.md` |
| 29 | Iris Restores the Covenant | `chapters/chapter-029-iris-restores-the-covenant.md` |
| 30 | Cross in the Chamber | `chapters/chapter-030-cross-in-the-chamber.md` |
| 31 | Thorne's Split | `chapters/chapter-031-thornes-split.md` |
| 32 | The Last Window | `chapters/chapter-032-the-last-window.md` |
| 33 | The Refusal | `chapters/chapter-033-the-refusal.md` |
| 34 | Naomi's Mirror | `chapters/chapter-034-naomis-mirror.md` |
| 35 | The Vote That Doesn't Finish | `chapters/chapter-035-the-vote-that-doesnt-finish.md` |
| 36 | The Machine Asks | `chapters/chapter-036-the-machine-asks.md` |
| 37 | Thorne Lets Go | `chapters/chapter-037-thorne-lets-go.md` |
| 38 | The Public No | `chapters/chapter-038-the-public-no.md` |
| 39 | The Narrow Law | `chapters/chapter-039-the-narrow-law.md` |
| 40 | Epilogue - The Hand | `chapters/chapter-040-epilogue-the-hand.md` |

---

# Manuscript Assembly Rules

1. Preserve source chapter headings.
2. Insert one blank line and a Markdown horizontal rule between chapters.
3. Preserve internal chapter prose exactly during assembly.
4. Do not revise while building. Revision happens in the next pass.
5. Output target: `MANUSCRIPT_COMBINED.md`.
6. Optional later exports:
   - `dist/The-Sovereign-Exception.manuscript.md`
   - `dist/The-Sovereign-Exception.docx`
   - `dist/The-Sovereign-Exception.pdf`
   - `dist/The-Sovereign-Exception.epub`

---

# Recommended Build Command

After pulling the repo locally:

```bash
python The-Sovereign-Exception/scripts/build_manuscript.py
```

Expected output:

```text
The-Sovereign-Exception/MANUSCRIPT_COMBINED.md
```

---

# Revision Pass 1 Targets

## Structural

- Confirm Act I escalation creates enough reader urgency before the Green Map explanation deepens.
- Confirm Act II evidence flow does not become too dossier-heavy.
- Confirm Act III public-hearing sequence alternates politics, technical stakes, and personal stakes.
- Confirm Act IV crisis escalation reads as thriller action, not policy lecture.
- Confirm Act V lands the moral cost of human authority without seeming anti-AI.

## Character Arcs

- Mara: from audit/control to accountable refusal and human command doctrine.
- Naomi: from exposure to responsibility for how truth behaves after release.
- Juno: from adversarial interface critique to constructive civic tooling.
- Iris: from technical guilt to covenant restoration.
- Elias: from guilt performance to useful witness/architect.
- Cross: from hearing combatant to narrow-law builder.
- Thorne: from architect-owner to witness who lets go.
- Father Tomas: moral witness and language keeper.

## Terminology Consistency

- AEGIS
- Annex C
- Sovereign Exception
- Human Override Covenant
- Restored Human Override Covenant
- Human-Visible Rapid Acceptance Protocol / Order
- Conditioned Consent
- Scope Laundering
- Managed Burn
- Aggregate legitimacy
- Participation reliability
- No blank authority fields

## Technical Doctrine Checks

- Keep AEGIS useful throughout, not cartoon-villain AI.
- Keep human refusal costly, not romantically pure.
- Keep legal/political mechanisms understandable in plain English.
- Avoid turning technical artifacts into real-world operational instructions.
- Make consent, liberty, and authority the heart of the thriller engine.

---

# Next Strongest Step

Create `scripts/build_manuscript.py`, then run a revision scaffold that produces:

- `REVISION_PASS_1.md`
- `CONTINUITY_NOTES.md`
- `CHARACTER_ARC_AUDIT.md`
- `TERMINOLOGY_GLOSSARY.md`
