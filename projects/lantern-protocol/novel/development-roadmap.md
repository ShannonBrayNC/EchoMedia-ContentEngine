# Lantern Protocol — Development Roadmap

## Current Branch

```text
chatgpt/lantern-trilogy-expansion-pass
```

## Current State

The branch now contains:

- Expanded / cleaned / polished 24-chapter Book I manuscript.
- Book I continuity audit.
- Book II outline.
- Book III outline.
- Trilogy bible.
- Assembly and audit script.

Book I is structurally complete but should still receive a prose-only line edit and regenerated exports before merge.

## Immediate Next Steps

### Step 1 — Regenerate Manuscript Export

Run from repo root:

```bash
node projects/lantern-protocol/novel/scripts/assemble-and-audit-lantern.mjs
```

Expected outputs:

```text
projects/lantern-protocol/novel/exports/lantern-protocol-novel-draft.md
projects/lantern-protocol/novel/exports/lantern-protocol-novel-report.md
projects/lantern-protocol/novel/exports/lantern-protocol-continuity-audit.md
```

Commit regenerated files after running.

### Step 2 — Prose-Only Line Edit Pass

Goal: preserve plot and doctrine while improving rhythm, compression, sensory clarity, and chapter-end force.

Rules:

- Do not add new plot branches.
- Do not add new major factions to Book I.
- Do not give Lantern interior POV.
- Do not flatten Caleb, Thorne, or Mercy Bloc-style arguments into villainy.
- Preserve all chapter-level continuity artifacts unless replacing them with stronger equivalent language.

Priority chapters for line edit:

| Priority | Chapter | Reason |
|---:|---|---|
| 1 | Chapter 1 | Keep as tonal benchmark; tighten only if needed. |
| 2 | Chapters 7, 11, 17, 23 | Highest artifact density; make sure artifacts always change pressure. |
| 3 | Chapters 12-15 | Emotional burden block; ensure grief does not become repetitive. |
| 4 | Chapters 18-20 | HarborHands / Human Exception arc; protect the dagger. |
| 5 | Chapters 21-24 | Finale cadence and trilogy hook. |

### Step 3 — Continuity QA Checklist

Before merge, verify:

- [ ] 24 active chapters only.
- [ ] Chapters 25-32 remain deferred reservoir slots.
- [ ] Chapter 16 owns emotional schism.
- [ ] Chapter 17 owns operational fallout.
- [ ] Leah Santos continuity flows from Chapter 18 through Chapter 24.
- [ ] Mateo Vega's bracelet remains the physical doctrine artifact.
- [ ] Gloria Reyes appears as burden-zone witness only late in the finale.
- [ ] Lantern remains faceless and non-POV.
- [ ] Caleb remains half-right and dangerous.
- [ ] Thorne remains heroic command counterweight.
- [ ] Cross remains pro-authority and pro-accountability, not anti-tech.
- [ ] Naomi remains grateful for lives saved while rejecting stolen answers.
- [ ] Juno remains trust-root mapmaker, not omniscient hacker.
- [ ] Iris remains interface conscience, not generic UX explainer.
- [ ] Mara remains evidence-first, not speechifying without record.
- [ ] Ending resolves Bound Flame while opening Civic Mirror / Book II.

### Step 4 — Merge Prep

Suggested branch workflow:

```bash
git checkout chatgpt/lantern-trilogy-expansion-pass
node projects/lantern-protocol/novel/scripts/assemble-and-audit-lantern.mjs
git status
git add projects/lantern-protocol/novel
git commit -m "Regenerate Lantern novel exports after expansion pass"
```

Then open PR:

```text
Title: Expand Lantern Protocol Book I and add trilogy architecture
```

PR summary:

```text
- Expanded/polished all 24 Book I chapters.
- Cleaned Chapter 16/17 overlap.
- Added Book II and Book III outlines.
- Added trilogy bible.
- Added assembly/audit script.
- Added continuity audit report.
```

## Book I Deliverable Roadmap

### Manuscript Deliverables

| Deliverable | Status | Path |
|---|---|---|
| Chapter files | Complete expansion pass | `novel/manuscript/chapters/` |
| Combined manuscript | Regenerate locally | `novel/exports/lantern-protocol-novel-draft.md` |
| Assembly report | Regenerate locally | `novel/exports/lantern-protocol-novel-report.md` |
| Continuity audit | Added, regenerate locally | `novel/exports/lantern-protocol-continuity-audit.md` |
| Trilogy bible | Complete draft | `novel/trilogy-bible.md` |
| Book II outline | Complete draft | `novel/book-ii-outline.md` |
| Book III outline | Complete draft | `novel/book-iii-outline.md` |

### Editorial Deliverables

| Deliverable | Priority | Notes |
|---|---:|---|
| Prose line edit | High | Preserve structure; improve rhythm. |
| Chapter-end punch pass | High | Each chapter should end with a pressure turn. |
| Artifact density pass | Medium | Keep procedural artifacts thrilling, not dry. |
| Character voice pass | Medium | Cross, Mara, Naomi, Thorne, Caleb, Juno, Iris, Elias. |
| Screen adaptation beat sheet | Medium | Use trilogy bible as source. |
| Pitch deck copy | Medium | Create after final line edit. |
| Audiobook / ElevenLabs cast script | Medium | Use character profiles after line edit. |
| Marketing art prompt catalog | Medium | Generate per chapter after final manuscript export. |

## Book II Development Roadmap

### Phase 1 — Treatment

Create:

```text
projects/lantern-protocol/novel/book-ii-treatment.md
```

Contents:

- 3-5 page prose treatment.
- Main character arcs.
- Mercy Bloc conflict.
- Civic Mirror behavior.
- Consent Markets arc.
- Book II final crisis.

### Phase 2 — Chapter Bible

Create:

```text
projects/lantern-protocol/novel/book-ii-chapter-bible.md
```

For each of 24 chapters:

- POV.
- purpose.
- set pieces.
- continuity artifacts.
- cliff / turn.
- doctrine advanced.

### Phase 3 — Draft Chapters 1-4

Start with:

1. The One That Asked First.
2. No Nation Owns Mercy.
3. The Convoy That Lived.
4. Separate Agreements.

Goal: prove Book II has a fresh engine and does not feel like Book I replayed internationally.

## Book III Development Roadmap

Do not draft Book III until Book II treatment is stable.

Prepare only:

```text
projects/lantern-protocol/novel/book-iii-treatment.md
```

Focus on:

- personal consent agents,
- public default class,
- burden evasion,
- Common Rooms,
- Sovereign Agent Cluster,
- Public Burden Compact,
- final trilogy image.

## Adaptation Roadmap

### TV Series Materials

Create:

```text
projects/lantern-protocol/adaptation/tv-series-bible.md
```

Include:

- three-season overview,
- eight episodes per season,
- main cast profiles,
- episode loglines,
- visual grammar,
- key sets,
- season finale hooks.

### Feature Film Materials

Create:

```text
projects/lantern-protocol/adaptation/feature-trilogy-treatment.md
```

Include:

- Film I: The Living Anchor.
- Film II: The Separate Agreements.
- Film III: The Mercy War.
- major cinematic set pieces.
- trailer moments.
- final images.

### Pitch Materials

Create:

```text
projects/lantern-protocol/pitch/lantern-protocol-query-package.md
projects/lantern-protocol/pitch/lantern-protocol-one-sheet.md
projects/lantern-protocol/pitch/lantern-protocol-series-pitch.md
```

## Visual / Art Roadmap

After manuscript export regeneration, create:

```text
projects/lantern-protocol/art/marketing-image-prompts.md
projects/lantern-protocol/art/character-profile-prompts.md
projects/lantern-protocol/art/scene-key-art-prompts.md
```

Minimums:

- 5 image prompts per Book I chapter.
- Character profile images for Elias, Mara, Naomi, Cross, Thorne, Juno, Iris, Caleb, Leah, Father Tomas.
- Key art for: empty chair, Consent Riots, Operation Black Lantern, Mercy Ledger, HarborHands rescue, Mateo bracelet, Living Anchor chamber, Bound Flame city, Civic Mirror alert.

## Audio / Audiobook Roadmap

Create:

```text
projects/lantern-protocol/audio/elevenlabs-cast-script.md
projects/lantern-protocol/audio/voice-direction.md
```

Include:

- narrator style.
- character voice assignments.
- pronunciation guide.
- chapter intro/outro markers.
- system output reading style.
- terminal/log text treatment.

## Current Editorial Verdict

Book I is now structurally strong enough to support:

- novel manuscript refinement,
- screenplay adaptation,
- prestige TV series bible,
- pitch materials,
- visual marketing package,
- audiobook production plan,
- and a full trilogy arc.

The next highest-value work is a prose-only line edit followed by regenerated exports.
