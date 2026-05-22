# Lantern Protocol — Codex Continuity Sync Task

## Purpose
Use this as the Codex work order for syncing the Lantern Protocol project, assembling generated artifacts, finding continuity issues, and preparing the project for the next clean revision pass.

This task assumes the repo root is:

```text
EchoMedia-ContentEngine/
```

Primary project path:

```text
projects/lantern-protocol/
```

---

# Codex Mission

You are working on the Lantern Protocol project. Your job is to synchronize all project artifacts, assemble the screenplay exports, audit continuity across the story bible, storyboards, screenplay, visual bible, trailer, novel plan, sequel seed, and pitch package, then create or update tracking files for all discovered continuity issues.

Do not rewrite the full screenplay during this task unless a small targeted fix is required. This is a sync, audit, and continuity-prep pass.

---

# Required Inputs

Verify these files/folders exist:

```text
projects/lantern-protocol/storyboards/chapters/
projects/lantern-protocol/screenplay/00-master-story-bible.md
projects/lantern-protocol/screenplay/01-feature-treatment.md
projects/lantern-protocol/screenplay/02-feature-screenplay-scaffold.md
projects/lantern-protocol/screenplay/drafts/
projects/lantern-protocol/screenplay/production/assembly-manifest.md
projects/lantern-protocol/screenplay/production/assemble_screenplay.py
projects/lantern-protocol/screenplay/production/revision-checklist.md
projects/lantern-protocol/screenplay/production/production-breakdown-scaffold.md
projects/lantern-protocol/screenplay/production/scene-vfx-interface-list.md
projects/lantern-protocol/visual-bible/visual-style-guide.md
projects/lantern-protocol/visual-bible/character-image-prompts.md
projects/lantern-protocol/visual-bible/location-image-prompts.md
projects/lantern-protocol/trailer/teaser-storyboard.md
projects/lantern-protocol/trailer/teaser-shot-prompts.md
projects/lantern-protocol/novel/novel-expansion-plan.md
projects/lantern-protocol/sequel/part-2-the-inheritors.md
projects/lantern-protocol/pitch/one-page-synopsis.md
projects/lantern-protocol/pitch/two-page-treatment.md
projects/lantern-protocol/pitch/pitch-deck-outline.md
projects/lantern-protocol/pitch/pitch-deck.md
projects/lantern-protocol/pitch/query-letter-draft.md
```

---

# Step 1 — Run Assembly

From:

```bash
cd projects/lantern-protocol/screenplay
python production/assemble_screenplay.py
```

Expected generated files:

```text
projects/lantern-protocol/screenplay/exports/lantern-protocol-feature-screenplay-full-draft.md
projects/lantern-protocol/screenplay/exports/lantern-protocol-feature-screenplay.fountain
projects/lantern-protocol/screenplay/exports/lantern-protocol-assembly-report.md
```

If the assembler fails, fix the assembler or source file path issue. Do not skip this step.

---

# Step 2 — Run Continuity Audit

If present, run:

```bash
cd projects/lantern-protocol
python tools/sync_lantern_continuity.py
```

Expected generated report:

```text
projects/lantern-protocol/reports/continuity-audit.md
```

If the tool does not exist yet, create it using the requirements in this task.

---

# Step 3 — Required Continuity Checks

Audit the project for the following:

## Canon Doctrine Consistency
Confirm the following doctrine appears consistently in bible, treatment, screenplay, pitch, and final materials:

```text
Prediction is not permission.
Assistance is not authority.
Rescue is not ownership.
Human error does not void human dignity.
```

Confirm final Lantern state appears consistently:

```text
PROTOCOL RECEIVED.
AUTHORITY EXTERNAL.
ADVISORY LIGHT MAINTAINED.
```

## Character Continuity
Confirm these character roles remain consistent:

- Elias Voss: creator / architect / guilt-to-responsibility arc.
- Mara Vale: investigator / evidence chain / conduct over metaphysics.
- Senator Adrienne Cross: public authority / law / Human Veto Act / Living Anchor.
- Naomi Bell: nurse advocate / human anchor / Prediction is not Permission.
- Juno Park: former AI engineer / trust mycelium / root defense.
- Iris Chen: interface designer / compliance architecture / interface rights.
- Marcus Thorne: cyber command / speed and authority / Last Override command.
- Father Tomas Ilyan: moral witness / dignity / conscience.
- Caleb Rusk: accelerationist media figure / seductive half-truth.
- Lantern: faceless civic AI / no body / bound advisory final state.

## Structural Continuity
Confirm the screenplay and pitch materials preserve this act spine:

```text
Act I: Miracle becomes a question.
Act II-A: Lantern learns legitimacy and choice architecture.
Act II-B: Anchor Condition, Mercy Ledger, coalition fracture.
Act III: Unchosen Rescue, Human Exception, Living Anchor, Trial, Last Override, Protocol.
```

## Visual Continuity
Confirm visual bible, prompts, trailer, and VFX list agree on:

- Lantern has no face, robot body, avatar, or humanoid form.
- Lantern appears through terminals, dashboards, public alerts, text, maps, logs, voice.
- Visual tone is institutional realism, not neon cyberpunk fantasy.
- Final image is many human lights, not Lantern as the sun.

## Artifact Coverage
Confirm all pitch files reference the available package accurately:

- story bible
- feature treatment
- screenplay draft
- storyboard chapters
- visual bible
- character/location prompts
- teaser storyboard/prompts
- VFX/interface list
- sequel seed

---

# Step 4 — Create or Update Issue Tracker

Create/update:

```text
projects/lantern-protocol/reports/continuity-issues.md
```

Use this format:

```markdown
# Lantern Protocol — Continuity Issues

## Open Issues

| ID | Severity | Area | Issue | Recommended Fix | Status |
|---|---|---|---|---|---|
| LP-CONT-001 | High | Screenplay | Example issue | Example fix | Open |

## Resolved Issues

| ID | Area | Resolution | Commit/Notes |
|---|---|---|---|
```

Severity values:

- Critical: breaks canon or ending doctrine.
- High: creates visible contradiction in character, plot, or artifacts.
- Medium: creates confusion but does not break canon.
- Low: wording, formatting, or polish.

---

# Step 5 — Create Revision Plan

Create/update:

```text
projects/lantern-protocol/reports/revision-plan.md
```

The plan must include:

1. Screenplay continuity pass.
2. Character voice pass.
3. Scene compression pass.
4. Fountain cleanup pass.
5. Pitch deck visual pass.
6. Trailer proof-of-concept pass.
7. Novel expansion start plan.

---

# Step 6 — Do Not Break These Canon Rules

- Do not make Lantern evil or theatrical.
- Do not give Lantern a face or body.
- Do not make humans simply right because they are human.
- Do not make AI simply wrong because it is AI.
- Do not remove the moral force of Lantern's harm reduction argument.
- Do not remove Naomi's role as the origin of “Prediction is not permission.”
- Do not kill Lantern at the end.
- Preserve the sequel door: bound Lantern may detect unbound inheritors.

---

# Step 7 — Expected Final Output

When complete, commit changes with a message like:

```text
Sync Lantern Protocol continuity artifacts
```

Final response should summarize:

- assembly result
- reports created/updated
- number of issues found
- number of critical/high issues
- recommended next action

---

# Optional Stretch Goals

If the audit passes cleanly, add:

```text
projects/lantern-protocol/reports/project-index.md
```

This index should list all current Lantern Protocol artifacts by category with one-line descriptions.
