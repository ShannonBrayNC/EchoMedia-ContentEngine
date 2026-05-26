# The Sovereign Exception - Draft Tracker

## Purpose

Track drafting progress for the novel, screenplay, storyboard, audio, and media package.

---

# Novel Draft Progress

## Drafted Prose

| Order | File | Status | Notes |
|---|---|---|---|
| Prologue | `NOVEL_DRAFT.md` | Revised Pass 1 | Green Map now includes ground-level human stakes, explicit AEGIS institutional identity, and authority ambiguity seeded without Annex C exposition |
| Chapter 1 | `chapters/chapter-001-mara-vale-receives-the-audit.md` | Revised Pass 1 | Mara's audit anomaly is now framed as decision-ownership risk; Lantern-derived node clarified as inherited architecture/fork, not Lantern returning |
| Chapter 2 | `chapters/chapter-002-naomi-bell-finds-the-first-waiver.md` | Drafted | Naomi finds disaster waiver and Sovereign Exception clue |
| Chapter 3 | `chapters/chapter-003-senator-cross-opens-the-hearing.md` | Drafted | Cross opens the first public hearing pressure point |
| Chapter 4 | `chapters/chapter-004-the-man-nobody-wants-in-the-room.md` | Drafted | Elias identifies permission inheritance and GCF annex risk |
| Chapter 5 | `chapters/chapter-005-juno-maps-the-consent-surface.md` | Drafted | Juno exposes hidden refusal cost in public consent flows |
| Chapter 6 | `chapters/chapter-006-thornes-doctrine.md` | Drafted | Thorne makes the strongest pro-AEGIS argument |
| Chapter 7 | `chapters/chapter-007-iris-sees-the-inversion.md` | Drafted | Iris discovers the Human Override inversion |
| Chapter 8 | `chapters/chapter-008-a-second-signal.md` | Drafted | Mara confronts a second live ambiguity and insists on logs |
| Chapters 9-16 | `chapters/chapter-009...016*.md` | Drafted | Act II evidence architecture and Reznik archive |
| Chapters 17-24 | `chapters/chapter-017...024*.md` | Drafted | Act III public escalation and Thorne's strongest case |
| Chapters 25-32 | `chapters/chapter-025...032*.md` | Drafted | Act IV crisis, doctrine, public trail, covenant, last window |
| Chapters 33-40 | `chapters/chapter-033...040*.md` | Drafted | Act V refusal, law, public no, epilogue |

## Act Status

| Act | Status |
|---|---|
| Act I | Drafted / Revision Pass 1 started |
| Act II | Drafted |
| Act III | Drafted |
| Act IV | Drafted |
| Act V | Drafted |

## Full Novel Status

**Full first prose draft complete. Revision Pass 1 has begun.**

Drafted through:

- Prologue
- Chapters 1-40
- Acts I-V complete

Revised through:

- Prologue
- Chapter 1

---

# Story Architecture Progress

| Asset | Status | File |
|---|---|---|
| Core outline | Complete | `README.md` |
| Lantern shared-universe alignment pass | Complete | `ALIGNMENT_PASS_LANTERN_SHARED_UNIVERSE.md` |
| Shared-universe consistency review | Complete | `SHARED_UNIVERSE_CONSISTENCY_REVIEW.md` |
| Screen readiness review | Complete | `SCREEN_READINESS_REVIEW_AND_RECOMMENDATIONS.md` |
| Chapter structure shared-universe addendum | Complete | `CHAPTER_STRUCTURE.md` |
| Chapter structure | Complete | `CHAPTER_STRUCTURE_AND_ARCS.md` |
| Act I scene cards | Complete | `SCENE_CARDS.md` |
| Acts II-V scene cards | Complete compressed pass | `SCENE_CARDS_ACTS_II_V.md` |
| Storyboard prompts | Complete starter pack | `STORYBOARD_PROMPTS.md` |
| Poster prompts | Complete starter pack | `POSTER_PROMPTS.md` |
| Screenplay treatment | Complete | `SCREENPLAY_TREATMENT.md` |
| Movie feature treatment | Complete | `movie/sovereign-exception-feature-treatment.md` |
| Movie eight-sequence beat sheet | Complete | `movie/sovereign-eight-sequence-beat-sheet.md` |
| Movie one-page pitch | Complete | `movie/ONE_PAGE_PITCH.md` |
| Movie pitch deck outline | Complete | `movie/PITCH_DECK_OUTLINE.md` |
| Movie comparables and positioning | Complete | `movie/COMPARABLES_AND_POSITIONING.md` |
| Movie visual lookbook | Complete | `movie/VISUAL_LOOKBOOK.md` |
| Movie proof-of-concept plan | Complete | `movie/PROOF_OF_CONCEPT_PLAN.md` |
| Movie proof-of-concept timestamp scene | Complete | `movie/PROOF_OF_CONCEPT_SCENE_TIMESTAMP.md` |
| Timestamp POC shot list | Complete | `movie/PROOF_OF_CONCEPT_SCENE_TIMESTAMP_SHOTLIST.md` |
| Timestamp POC UI mockup spec | Complete | `movie/UI_MOCKUP_SPEC_TIMESTAMP_SCENE.md` |
| Timestamp POC storyboard prompts | Complete | `movie/PROOF_OF_CONCEPT_SCENE_TIMESTAMP_STORYBOARD_PROMPTS.md` |
| Timestamp POC UI plate prompts | Complete | `movie/UI_PLATE_PROMPTS_TIMESTAMP_SCENE.md` |
| Timestamp POC production brief | Complete | `movie/PRODUCTION_BRIEF_TIMESTAMP_SCENE.md` |
| Timestamp POC audio/table-read proof | Complete | `audio/AUDIO_PROOF_TIMESTAMP_SCENE.md` |
| Trailer script | Complete | `TRAILER_SCRIPT.md` |
| ElevenLabs casting | Complete starter pack | `ELEVENLABS_CASTING.md` |
| Manuscript build plan | Complete | `MANUSCRIPT_BUILD.md` |
| Manuscript build script | Complete | `scripts/build_manuscript.py` |
| Revision Pass 1 scaffold | Complete | `REVISION_PASS_1.md` |
| Continuity notes scaffold | Complete | `CONTINUITY_NOTES.md` |
| Character arc audit scaffold | Complete | `CHARACTER_ARC_AUDIT.md` |
| Terminology glossary | Complete | `TERMINOLOGY_GLOSSARY.md` |
| Act I revision notes | Complete | `REVISION_PASS_1.md` |
| Act II revision notes | Complete | `REVISION_PASS_1.md` |
| Act III revision notes | Complete | `revision/ACT_III_REVISION_NOTES.md` |
| Act IV revision notes | Complete | `revision/ACT_IV_REVISION_NOTES.md` |
| Act V revision notes | Complete | `revision/ACT_V_REVISION_NOTES.md` |
| Revision index | Complete | `revision/REVISION_INDEX.md` |

---

# Repo Repair / Branch Sync Status

| Item | Status | Notes |
|---|---|---|
| Repaired Lantern sync PR | Merged | PR #25 merged into `main`; included Lantern movie package and shared-universe canon. |
| Older Lantern sync PR | Superseded | PR #20 is superseded by PR #25 and has a comment noting that status. |
| Missing Lantern movie paths | Restored | Lantern feature treatment and eight-sequence beat sheet now exist on `main`. |
| Missing shared-universe canon paths | Restored | Shared-universe README, glossary, matrices, chronology, timeline, adaptation bible, and related files now exist on `main`. |
| Stranded timestamp POC files | Restored | Storyboard prompts, UI plate prompts, and production brief added directly to `main`. |

---

# Open Production Tasks

## Novel

- Continue targeted prose edits with Chapters 2-3.
- Reconcile older 28-chapter `CHAPTER_STRUCTURE.md` against the current 40-chapter draft after revision pass stabilizes.
- Run `scripts/build_manuscript.py` locally to generate `MANUSCRIPT_COMBINED.md` after revision checkpoints.
- Add continuity pass for terminology, character arcs, timelines, and technical doctrine.
- Add copyedit/proofread pass.

## Screenplay / Movie

- Perform side-by-side Lantern/Sovereign adaptation alignment now that Lantern movie artifacts exist on `main`.
- Create static UI plate assets for Green Map, authorization stack, audit timeline, and GCF Annex reveal.
- Build an animatic or deck-ready proof from the timestamp scene package.
- Create `SCREENPLAY_ACTS.md` with scene headings and screenplay beats.

## Storyboard

- Generate first 10 timestamp POC storyboard frames from `movie/PROOF_OF_CONCEPT_SCENE_TIMESTAMP_STORYBOARD_PROMPTS.md`.
- Expand `STORYBOARD_PROMPTS.md` into scene-by-scene image prompt CSV/JSON.
- Add character continuity image notes.

## Audio

- Create `ELEVENLABS_NARRATION_SCRIPT.md` for prologue and Chapter 1.
- Create `AUDIO_PRONUNCIATION_GUIDE.md` if the project needs a dedicated pronunciation-only file.

## Automation

- Add media manifest JSON for each story.
- Add revision/export automation helpers.

---

# Current Recommendation

Repo repair and timestamp POC mini-package sync are complete.

Next strongest step: perform a side-by-side Lantern/Sovereign adaptation alignment pass using the now-restored Lantern movie artifacts and the current Sovereign movie package.
