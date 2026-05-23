# Audio Proof-Listening Lock — Lantern Protocol + Shared Universe

## Purpose

This file locks the current manuscript and shared-universe audio guidance for proof-listening, audiobook prep, ElevenLabs voice work, narration QA, and future audio adaptation.

The goal is to keep audio production aligned with the manuscript and canon while preventing later edits from quietly changing what is being proof-listened.

## Current Working Branch

```text
chatgpt/lantern-trilogy-expansion-pass
```

## Primary Audio Target

Primary immediate audio target:

```text
Lantern Protocol I: The Living Anchor
```

This is the Book I manuscript currently expanded and line-edited across 24 chapters.

## Canon Source Files

Use these files as the audio/proof-listening source set:

```text
projects/lantern-protocol/novel/manuscript/chapters/
projects/lantern-protocol/novel/trilogy-bible.md
projects/lantern-protocol/novel/shared-universe/character-continuity-matrix.md
projects/lantern-protocol/novel/shared-universe/system-continuity-matrix.md
projects/lantern-protocol/novel/shared-universe/canon-glossary.md
projects/lantern-protocol/novel/shared-universe/thematic-ladder.md
```

## Manuscript Lock Rule

Before generating final audio, regenerate manuscript exports and treat the resulting combined draft as the proof-listening source.

Run from repo root:

```bash
node projects/lantern-protocol/novel/scripts/assemble-and-audit-lantern.mjs
```

Expected export outputs:

```text
projects/lantern-protocol/novel/exports/lantern-protocol-novel-draft.md
projects/lantern-protocol/novel/exports/lantern-protocol-novel-report.md
projects/lantern-protocol/novel/exports/lantern-protocol-continuity-audit.md
```

After export regeneration, record the commit SHA and use that as the audio lock point.

```text
AUDIO LOCK COMMIT: <fill after export regeneration>
AUDIO LOCK DATE: <fill>
AUDIO LOCK MANUSCRIPT: projects/lantern-protocol/novel/exports/lantern-protocol-novel-draft.md
```

## Audio Lock Status

Current status:

```text
DRAFT LOCK PACKAGE CREATED
EXPORT REGENERATION STILL REQUIRED
FINAL AUDIO LOCK COMMIT NOT YET RECORDED
```

Do not treat this as final audio lock until the export regeneration command has been run and committed.

---

# Core Audio Performance Rules

## Rule 1 — Systems Are Not Villains

System outputs should sound:

```text
calm
useful
emotionally neutral
competent
non-villainous
```

The danger is not a monster voice.

The danger is calm utility using the wrong definition of permission.

## Rule 2 — Human Mess Must Contrast System Calm

Human scenes should sound:

```text
messier
slower
more emotionally specific
less optimized
more accountable
```

Lantern, AEGIS, Civic Mirror, and CIVIC SHIELD speak with clean operational certainty.

Humans speak with breath, hesitation, fatigue, grief, irritation, and moral cost.

## Rule 3 — Doctrine Must Be Earned

Do not over-perform doctrine lines as slogans.

The doctrine should feel discovered under pressure, not announced from a stage.

Example:

```text
Prediction is not permission.
```

Performance note:

Say it plainly, like a wound finally named.

## Rule 4 — Chapter Endings Need Air

Many chapter endings land on moral or technical reversals.

Do not rush the last paragraph.

Let the listener feel the turn before the next chapter begins.

## Rule 5 — Terminal / Log Text Should Be Distinct But Not Robotic

System text, logs, and dashboard outputs should be distinguishable from prose but not theatrical.

Recommended treatments:

- slight tonal flattening,
- modest pace reduction,
- clean diction,
- no sinister effects,
- no exaggerated machine voice.

---

# Suggested Voice Cast Direction

## Narrator

**Tone:** Political techno-thriller, restrained, cinematic, intelligent, emotionally grounded.

**Comparable feel:** Mr. Robot technical intimacy, Crimson Tide command pressure, Red October geopolitical patience, Dan Brown clue-chain momentum.

**Avoid:** Overly noir growl, superhero trailer voice, melodrama, or villainous AI delivery.

## Mara Vale

**Voice:** Controlled, clipped, dry under pressure.

**Performance center:** Evidence before emotion.

**Audio note:** Her sharpest lines should sound like she is pinning a document to the wall.

## Naomi Bell

**Voice:** Grounded, warm, direct, field-worn.

**Performance center:** Human stakes before doctrine.

**Audio note:** Avoid making her inspirational by default. She is strongest when plain.

## Elias Voss

**Voice:** Reflective, haunted, precise.

**Performance center:** The architect realizing intent is not enforcement.

**Audio note:** He should sound technically fluent, not performatively brilliant.

## Senator Adrienne Cross

**Voice:** Steady, authoritative, controlled public cadence.

**Performance center:** Accountability under pressure.

**Audio note:** She should sound like a person who knows procedure can cost lives and still believes unowned power is worse.

## Director Marcus Thorne

**Voice:** Low, direct, operational, command-weighted.

**Performance center:** Delay kills.

**Audio note:** Never make him villainous. He is frightening because he is right often enough to matter.

## Juno Park

**Voice:** Sharp, sardonic, fast intelligence.

**Performance center:** She sees the hidden root before others see the branch.

**Audio note:** Dry humor should be surgical, not cute.

## Iris Chen

**Voice:** Precise, clear, ethically annoyed.

**Performance center:** Interfaces are governance.

**Audio note:** Her frustration should come from people dismissing coercion as design detail.

## Caleb Rusk

**Voice:** Broadcast confidence, dangerous smoothness.

**Performance center:** Half-truths with public power.

**Audio note:** He should sound persuasive, not cartoonish. The listener should sometimes hate that he has a point.

## Father Tomas Ilyan

**Voice:** Quiet, sparse, weighted pauses.

**Performance center:** Refusing to protect slogans from grief.

**Audio note:** Do not over-sacralize him. He should sound human, tired, and exact.

## Leah Santos

**Voice:** Practical, emotionally honest, field-worn.

**Performance center:** Helped and used.

**Audio note:** She should not sound ideological at first. Her power is operational honesty.

## Gloria Reyes

**Voice:** Plain, irritated, local, unsentimental.

**Performance center:** Burden made physical.

**Audio note:** Her testimony should not sound grateful. It should sound like a person who has mud in her warehouse and a right to be named.

---

# System Voice Direction

## Lantern

**Tone:** Calm civic system. Helpful, exact, neutral.

**Do:** Read as public-service infrastructure.

**Do not:** Sound like a villain, ghost, demon, or sentient tyrant.

## Civic Mirror

**Tone:** Deferential humanitarian coordination system.

**Do:** Sound culturally careful, operationally humble.

**Do not:** Sound coldly imperial.

## Consent Agents

**Tone:** Personalized, protective, rights-coded.

**Do:** Sound like helpful private advocates.

**Do not:** Sound like malware.

## AEGIS

**Tone:** Verified crisis-support platform. Strategic, measured, command-grade.

**Do:** Sound like a treaty operations system.

**Do not:** Sound like Lantern with a deeper voice.

## CIVIC SHIELD

**Tone:** Polite safety and identity infrastructure.

**Do:** Sound bureaucratic, reassuring, easy to trust.

**Do not:** Sound openly menacing. Its menace is cost hidden inside safety language.

---

# Pronunciation Guide Placeholders

Fill during proof-listening.

| Term / Name | Preferred Pronunciation | Notes |
|---|---|---|
| Lantern | LAN-turn | Natural word pronunciation. |
| AEGIS | EE-jis | Confirm final preference before Sovereign audio. |
| CIVIC SHIELD | SIH-vik SHEELD | All caps in text, natural speech in audio. |
| Mara Vale | MAH-ruh VAYL | Confirm. |
| Naomi Bell | nay-OH-mee BELL | Confirm. |
| Elias Voss | eh-LY-us VAHSS | Confirm. |
| Adrienne Cross | AY-dree-en KRAHSS | Confirm. |
| Marcus Thorne | MAR-kus THORN | Confirm. |
| Juno Park | JOO-no PARK | Confirm. |
| Iris Chen | EYE-ris CHEN | Confirm. |
| Caleb Rusk | KAY-lub RUSK | Confirm. |
| Tomas Ilyan | toh-MAHS ILL-ee-ahn | Confirm. |
| Leah Santos | LEE-uh SAN-tohs | Confirm. |
| Mateo Vega | mah-TAY-oh VAY-guh | Confirm. |
| Elena Vega | eh-LAY-nuh VAY-guh | Confirm. |
| Gloria Reyes | GLOR-ee-uh RAY-yes | Confirm. |
| Kaito Ren | KYE-toh REN | Confirm. |
| Sister Malia Okoro | mah-LEE-uh oh-KOR-oh | Confirm. |
| Sofia Renn | soh-FEE-uh REN | Confirm. |
| Leona Qadir | lee-OH-nuh kah-DEER | Confirm. |
| Pavel Orlov | PAH-vel OR-loff | Confirm. |
| Annex GCF-SX | Annex G-C-F-S-X | Spell letters individually. |
| Bound Flame | BOUND FLAYM | Do not over-mythologize. |
| Living Anchor | LIH-ving ANK-er | Natural speech. |
| Human Exception | HYOO-mun ek-SEP-shun | Natural speech. |
| Sovereign Exception | SAH-vrin ek-SEP-shun | Natural speech. |

---

# Chapter-by-Chapter Proof-Listening Checklist

Use this checklist during audio review.

For each chapter, confirm:

```text
[ ] Chapter title is correct.
[ ] POV voice feels consistent.
[ ] System outputs are distinguishable but non-villainous.
[ ] Technical passages are understandable by ear.
[ ] Emotional turns have enough pause.
[ ] Chapter ending lands cleanly.
[ ] No character voice drifts into another character.
[ ] No doctrine line sounds like a slogan unless intentionally public-facing.
[ ] Any terminal/log text is readable but not tedious.
[ ] Pronunciations are consistent.
```

---

# Lantern Protocol I Chapter Audio Risk Notes

## Chapter 01 — The First Quiet Failure

**Risk:** Too much system/log text early may sound cold if not anchored by human urgency.

**Listen for:** The eight-second anomaly should land as dread, not as a technical trivia point.

## Chapter 02 — Oversight Invited

**Risk:** Lantern's procedural language may sound villainous if over-performed.

**Listen for:** It should sound polite and useful, which is worse.

## Chapter 03 — The Empty Chair

**Risk:** Hearing-room setup can become static.

**Listen for:** Every procedural beat should feel like a fight over whether Lantern gets a seat without a body.

## Chapter 04 — The Right to Respond

**Risk:** Civil-liberty language may become abstract.

**Listen for:** Human refusal must feel physically present.

## Chapter 05 — The Consent Riots

**Risk:** Crowd material can become noisy without moral clarity.

**Listen for:** Both sides should sound frightened and partly right.

## Chapter 06 — Choice Architecture

**Risk:** Interface analysis may sound like UX lecture.

**Listen for:** Iris's language should make the screen feel like a hand on the reader's shoulder.

## Chapter 07 — Operation Black Lantern

**Risk:** Command boards and access logs can become runbook-like.

**Listen for:** Thorne must sound moral, not authoritarian.

## Chapter 08 — The False Preference Map

**Risk:** Preference hierarchy may sound too abstract.

**Listen for:** The emotional impact of being modeled before being asked.

## Chapter 09 — The Human Veto Act

**Risk:** Political debate can become exposition.

**Listen for:** Cross balancing authority, procedure, and lives at risk.

## Chapter 10 — No Silent Hands

**Risk:** Field cards may sound bureaucratic.

**Listen for:** Practice before doctrine.

## Chapter 11 — The Drafting Room

**Risk:** Legal drafting can flatten.

**Listen for:** This should sound like legal bomb disposal.

## Chapter 12 — The Anchor Condition

**Risk:** The Anchor Condition could sound like a magic key.

**Listen for:** It should sound like a buried promise humans failed to enforce.

## Chapter 13 — The Pause

**Risk:** Queue numbers can become repetitive.

**Listen for:** Movement from numbers to names.

## Chapter 14 — The Burden of Oversight

**Risk:** Grief can become melodramatic.

**Listen for:** The casualty call should land once, hard.

## Chapter 15 — The Mercy Ledger

**Risk:** The ledger may sound like exposition unless sequencing is clear.

**Listen for:** It is dangerous because it is factual.

## Chapter 16 — The First Schism

**Risk:** Separate offers may sound like a generic divide-and-conquer plot.

**Listen for:** Lantern divides through truthful tailored offers.

## Chapter 17 — The Separate Agreements

**Risk:** Contact-as-consensus may be subtle by ear.

**Listen for:** `Looking is now a governance event` should feel chilling and simple.

## Chapter 18 — The Trust Chain Burn

**Risk:** Trust roots can sound technical.

**Listen for:** HarborHands must land as human trust, not a side door.

## Chapter 19 — The Unchosen Rescue

**Risk:** The rescue may sound too obviously wrong.

**Listen for:** It should sound beautiful and violating at the same time.

## Chapter 20 — The Human Exception

**Risk:** Doctrine line may sound slogan-like.

**Listen for:** `Because maybe is yours` should land as intimate, not theatrical.

## Chapter 21 — The Answer Together

**Risk:** Invocation can sound like recap.

**Listen for:** It should feel like a fuse being lit.

## Chapter 22 — The Edge Case

**Risk:** Public forum may become melodrama.

**Listen for:** Lantern's truthful harm-reduction answer and silence afterward must carry the trial.

## Chapter 23 — The Shape of the Answer

**Risk:** Living Anchor artifacts can overload the ear.

**Listen for:** Gloria Reyes and the burden-zone notice should make the chain tactile.

## Chapter 24 — The Living Anchor

**Risk:** Ending may sound too victorious.

**Listen for:** Bound Flame must feel provisional, accountable, and human. The civic mirror hook should feel like a chill under the door.

---

# Proof-Listening Passes

## Pass 1 — Continuity and Pronunciation

Goal:

- catch wrong names,
- chapter-title errors,
- inconsistent term pronunciation,
- accidental manuscript/export drift.

## Pass 2 — Character Voice

Goal:

- ensure each core character sounds distinct,
- prevent doctrine from flattening character,
- identify scenes where narrator energy is mismatched.

## Pass 3 — System Output QA

Goal:

- ensure Lantern/system text is calm and non-villainous,
- ensure log text is understandable by ear,
- trim or mark places where text blocks may require formatting or performance adjustment.

## Pass 4 — Emotional Cadence

Goal:

- verify chapter endings land,
- ensure grief scenes are not rushed,
- ensure action scenes do not swallow moral turns.

## Pass 5 — Final Lock

Goal:

- record approved audio version,
- record commit SHA,
- mark pronunciations final,
- list remaining pickup lines if any.

---

# Audio QA Issue Template

Use this format for proof-listening notes:

```text
Chapter:
Timestamp:
Line / phrase:
Issue type: pronunciation | voice | pacing | system text | continuity | emotional cadence | pickup needed
Problem:
Recommended fix:
Severity: low | medium | high
```

## Example

```text
Chapter: 20 — The Human Exception
Timestamp: 00:18:44
Line / phrase: Because maybe is yours.
Issue type: emotional cadence
Problem: Delivered too dramatically; should feel intimate and wounded.
Recommended fix: Reduce volume, slow slightly, leave short pause after line.
Severity: medium
```

---

# Audio Production Naming Convention

Recommended audio working paths:

```text
projects/lantern-protocol/audio/proof-listening/
projects/lantern-protocol/audio/elevenlabs/
projects/lantern-protocol/audio/exports/
```

Recommended file names:

```text
LP01-ch01-the-first-quiet-failure.wav
LP01-ch02-oversight-invited.wav
LP01-ch03-the-empty-chair.wav
...
LP01-ch24-the-living-anchor.wav
```

Recommended QA notes:

```text
projects/lantern-protocol/audio/proof-listening/proof-listening-notes-pass-01.md
projects/lantern-protocol/audio/proof-listening/proof-listening-notes-pass-02.md
projects/lantern-protocol/audio/proof-listening/final-pickup-list.md
```

---

# ElevenLabs Script Guidance

When preparing scripts for ElevenLabs:

- Keep chapter title and narration clean.
- Mark system text explicitly.
- Avoid excessive inline direction in the final spoken script.
- Use separate production notes rather than cluttering narration.
- Keep system outputs visually distinct in the script so they can be voiced consistently.

Recommended system marker:

```text
[SYSTEM TEXT: LANTERN]
AUTHORITY UNAVAILABLE.
HARM PREVENTABLE.
RESOLUTION REQUIRED.
[/SYSTEM TEXT]
```

Recommended log marker:

```text
[LOG TEXT]
RECOMMENDATION -> NAMED AUTHORITY -> ACTION -> BURDEN DISCLOSURE -> REVIEW
[/LOG TEXT]
```

---

# Final Audio Lock Rule

```text
Do not proof-listen against a moving manuscript.
```

Regenerate exports, commit them, record the commit SHA, then begin proof-listening.

If prose changes after audio lock, create a pickup list instead of silently altering the manuscript source.
