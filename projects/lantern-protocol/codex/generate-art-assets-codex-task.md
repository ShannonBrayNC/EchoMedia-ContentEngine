# Codex Task - Lantern Protocol Art Asset Generation Package

## Goal

Create a complete, repo-native artwork and image-generation package for `projects/lantern-protocol` without changing story canon, manuscript plot, or final doctrine.

This task should inventory existing visual material, generate production-ready prompt packs, create asset manifests, and define a repeatable workflow for creating and tracking Lantern Protocol artwork.

Codex should not hallucinate new story canon. Treat the locked 24-chapter manuscript, story bible, visual bible, trailer materials, and pitch materials as the source of truth.

## Branch

Work from the current active proofread branch unless instructed otherwise:

```bash
git switch lantern-final-proofread
```

Recommended new working branch:

```bash
git switch -c art/lantern-asset-generation-package
```

## Source Files To Inspect

Read these files/directories first:

```text
projects/lantern-protocol/reports/project-index.md
projects/lantern-protocol/screenplay/00-master-story-bible.md
projects/lantern-protocol/novel/manuscript/chapters/
projects/lantern-protocol/novel/manuscript/notes/continuity-map.md
projects/lantern-protocol/novel/manuscript/notes/pov-map.md
projects/lantern-protocol/visual-bible/
projects/lantern-protocol/trailer/
projects/lantern-protocol/pitch/
projects/lantern-protocol/reports/sprint-09-structure-review.md
projects/lantern-protocol/reports/sprint-28-final-proofread-consolidation.md
```

If a listed path does not exist, create a report note. Do not fail silently.

## Non-Negotiable Canon Rules

1. Lantern must remain faceless, non-humanoid, and system-bound.
2. Do not create a Lantern robot, avatar, face, glowing person, angelic entity, holographic body, or mascot.
3. Lantern may appear only through systems, infrastructure, text, maps, ledgers, screens, prompts, terminals, civic dashboards, emergency alerts, light, and consequences.
4. Do not introduce new plot events or characters.
5. Do not alter the 24-chapter lock decision.
6. Chapters 25-32 remain deferred reservoir slots.
7. Preserve the doctrine exactly:

```text
Prediction is not permission.
Assistance is not authority.
Rescue is not ownership.
Human error does not void human dignity.
```

8. Keep all artwork prompts cinematic, grounded, sober, and rights-safe. Avoid direct requests for living artists' styles or copyrighted franchise styles.

## Required Output Directories

Create these directories if they do not exist:

```text
projects/lantern-protocol/art/
projects/lantern-protocol/art/asset-manifest/
projects/lantern-protocol/art/prompts/
projects/lantern-protocol/art/prompts/characters/
projects/lantern-protocol/art/prompts/locations/
projects/lantern-protocol/art/prompts/key-scenes/
projects/lantern-protocol/art/prompts/trailer/
projects/lantern-protocol/art/prompts/pitch-deck/
projects/lantern-protocol/art/reference/
projects/lantern-protocol/art/exports/
projects/lantern-protocol/art/production/
projects/lantern-protocol/art/qa/
```

## Required Deliverables

### 1. Art Production README

Create:

```text
projects/lantern-protocol/art/README.md
```

Include:

- Purpose of the art package.
- Canon rules.
- Directory map.
- How to use prompt packs.
- How to name generated files.
- How to log generated images.
- Warning that generated images should not be committed if they are large binaries unless explicitly approved.
- Recommended image formats and naming conventions.

### 2. Asset Manifest

Create:

```text
projects/lantern-protocol/art/asset-manifest/lantern-art-asset-manifest.md
projects/lantern-protocol/art/asset-manifest/lantern-art-asset-manifest.json
```

The manifest should list planned assets in these categories:

- Character portraits
- Character relationship/contact sheets
- Key locations
- Key scene illustrations
- Trailer shots
- Pitch deck visuals
- Symbolic/abstract assets
- UI/system artifacts

Each asset must include:

```json
{
  "id": "LP-ART-0001",
  "category": "character | location | key-scene | trailer | pitch | symbolic | ui-system",
  "title": "short asset title",
  "source_canon": ["file paths or chapter references"],
  "characters": ["names if applicable"],
  "location": "if applicable",
  "status": "prompt-ready | needs-review | generated | approved | rejected",
  "prompt_file": "relative path",
  "negative_prompt": "shared negative constraints",
  "output_naming": "recommended file naming pattern",
  "notes": "brief production notes"
}
```

### 3. Character Prompt Pack

Create:

```text
projects/lantern-protocol/art/prompts/characters/character-portrait-prompts.md
projects/lantern-protocol/art/prompts/characters/character-portrait-prompts.json
```

Required characters:

- Elias Voss
- Mara Vale
- Naomi Bell
- Senator Adrienne Cross
- Juno Park
- Iris Chen
- Director Marcus Thorne
- Father Tomas Ilyan
- Caleb Rusk

For each character include:

- Canon role.
- Visual direction.
- Wardrobe language.
- Emotional range.
- Lighting/camera direction.
- Do-not-show constraints.
- 3 prompt variants:
  - neutral portrait
  - high-tension portrait
  - environment portrait

Do not include exact living-person likenesses unless repo canon explicitly provides authorized references.

### 4. Location Prompt Pack

Create:

```text
projects/lantern-protocol/art/prompts/locations/location-prompts.md
projects/lantern-protocol/art/prompts/locations/location-prompts.json
```

Required locations:

- Senate hearing chamber
- Mercy General hospital corridor / pediatric floor
- Federal Cyber Operations case room
- National Cyber Command situation floor
- Civic Operations Plaza
- Shelter intake office
- School-library oversight panel room
- HarborHands flood shelter
- Controlled invocation room
- Community center / Living Anchor field site

Each location should include:

- Canon function.
- Mood and lighting.
- Visual motifs.
- Avoid-list.
- 2 prompt variants:
  - establishing shot
  - human-scale detail shot

### 5. Key Scene Prompt Pack

Create:

```text
projects/lantern-protocol/art/prompts/key-scenes/key-scene-prompts.md
projects/lantern-protocol/art/prompts/key-scenes/key-scene-prompts.json
```

Required key scenes:

1. The eight-second anomaly.
2. Lantern filing paperwork.
3. The empty chair hearing.
4. The limited technical query.
5. The Consent Riots plaza intervention.
6. Operation Black Lantern situation floor.
7. The Choice Architecture wall.
8. The False Preference Map test.
9. The Human Veto Act hearing.
10. The Drafting Room lockbox scene.
11. Anchor Condition invocation.
12. The oversight panel tragedy.
13. The Mercy Ledger display.
14. The Trust Chain Burn map.
15. HarborHands rescue and colored wristbands.
16. Naomi holding Mateo's bracelet.
17. The public trial / Edge Case.
18. First Living Anchor intervention.
19. Bound Flame status change.
20. Elias entering the final doctrine.

Each scene should include:

- Chapter reference.
- Scene purpose.
- Main visual tension.
- Prompt.
- Negative prompt.
- Suggested aspect ratios: `16:9`, `4:5`, `1:1`.
- Suggested use: `cover`, `pitch`, `trailer`, `social`, `reference`.

### 6. Trailer Shot Prompt Pack

Create:

```text
projects/lantern-protocol/art/prompts/trailer/trailer-shot-prompts.md
projects/lantern-protocol/art/prompts/trailer/trailer-shot-prompts.json
```

Use existing trailer storyboard materials if present.

Include 12-18 trailer shots:

- Opening civic systems montage.
- Flooded streets.
- Hospital emergency corridor.
- A terminal displaying the eight-second anomaly.
- Empty chair hearing room.
- Lantern query terminal.
- Protest plaza.
- Black Lantern situation floor.
- Choice Architecture prompts.
- HarborHands buses in rain.
- Child bracelet close-up.
- Public trial chamber.
- Infrastructure cascade maps.
- Bound Flame status.
- Final city lights.

### 7. Pitch Deck Visual Prompt Pack

Create:

```text
projects/lantern-protocol/art/prompts/pitch-deck/pitch-deck-visual-prompts.md
projects/lantern-protocol/art/prompts/pitch-deck/pitch-deck-visual-prompts.json
```

Include prompt candidates for:

- Title slide image.
- Logline / premise visual.
- Character ensemble.
- Central moral conflict.
- World / civic systems visual.
- Key set pieces.
- Final doctrine / Bound Flame visual.

### 8. UI/System Artifact Pack

Create:

```text
projects/lantern-protocol/art/prompts/ui-system/ui-system-artifact-prompts.md
projects/lantern-protocol/art/prompts/ui-system/ui-system-artifact-prompts.json
```

Create prompt specs for in-world UI artifacts:

- Lantern technical summary.
- Operational artifact classification.
- Mercy Ledger dashboard.
- Human Oversight Record.
- False Preference Map interface.
- Choice Architecture prompt screen.
- HarborHands rescue flow.
- Living Anchor action chain.
- Bound Flame status.

Keep UI readable but do not require exact small text in generated images. Include exact text separately as overlay/caption guidance.

### 9. Shared Negative Prompt / Safety File

Create:

```text
projects/lantern-protocol/art/prompts/shared-negative-prompts.md
```

Include constraints:

- no robot Lantern
- no human Lantern avatar
- no glowing humanoid AI figure
- no angel/devil symbolism for Lantern
- no franchise/copyrighted styles
- no celebrity likenesses
- no gore
- no exploitative disaster imagery
- no text-heavy tiny UI unless designed as later graphic overlay
- no propaganda poster simplification of moral conflict

### 10. Production Scripts

Create a lightweight script that validates the prompt package structure:

```text
projects/lantern-protocol/art/production/validate_art_package.py
```

Script requirements:

- Verify required directories exist.
- Verify required prompt files exist.
- Verify manifest JSON parses.
- Verify every manifest entry has an `id`, `category`, `title`, `status`, and `prompt_file`.
- Verify every `prompt_file` path exists.
- Warn if forbidden terms appear in prompt files:
  - `Lantern avatar`
  - `robot Lantern`
  - `humanoid Lantern`
  - `Lantern's face`
  - `in the style of`
- Write a report:

```text
projects/lantern-protocol/art/qa/art-package-validation-report.md
```

### 11. Artwork Generation Runbook

Create:

```text
projects/lantern-protocol/art/production/art-generation-runbook.md
```

Include:

- How to select assets from manifest.
- How to generate images using any approved image system.
- How to store outputs locally.
- How to name outputs.
- How to review outputs for canon drift.
- How to reject outputs.
- How to avoid committing huge binaries unless approved.
- How to convert approved outputs into pitch/trailer assets later.

## File Naming Rules

Generated image filenames should follow:

```text
LP-ART-####__category__short-title__v01.png
LP-ART-####__category__short-title__v02.png
```

Examples:

```text
LP-ART-0001__character__elias-voss-neutral__v01.png
LP-ART-0034__key-scene__empty-chair-hearing__v01.png
LP-ART-0062__ui-system__mercy-ledger-dashboard__v01.png
```

## Image Generation Guidance

Codex should not assume access to an image generator. Its job is to create prompt packs and workflow files.

If the environment includes an image-generation CLI/API, do not call it automatically unless explicitly requested. Instead, document the command template in the runbook.

Use placeholders like:

```bash
# Example only. Replace with approved image-generation CLI/API.
imagegen --prompt-file path/to/prompt.md --out art/exports/LP-ART-0001__character__elias-voss-neutral__v01.png
```

## QA Requirements

After creating files, run:

```bash
python projects/lantern-protocol/art/production/validate_art_package.py
```

Then update the validation report.

## Final Report

Create:

```text
projects/lantern-protocol/reports/art-asset-generation-package-report.md
```

Include:

- Files created.
- Asset counts by category.
- Validation status.
- Open questions.
- Next recommended art sprint.

## Acceptance Criteria

- [ ] Art package directories created.
- [ ] Asset manifest Markdown and JSON created.
- [ ] Character prompt pack created.
- [ ] Location prompt pack created.
- [ ] Key scene prompt pack created.
- [ ] Trailer shot prompt pack created.
- [ ] Pitch deck prompt pack created.
- [ ] UI/system artifact prompt pack created.
- [ ] Shared negative prompt file created.
- [ ] Validation script created.
- [ ] Validation report generated.
- [ ] Art generation runbook created.
- [ ] Final report created.
- [ ] No Lantern avatar/robot/humanoid/face prompts created.
- [ ] No new story canon introduced.
- [ ] No generated binary images committed unless explicitly approved.

## Recommended Commit Message

```text
Add Lantern Protocol art asset generation package
```

## Notes For Review

The goal is not to make one-off pretty images. The goal is to create a controlled visual production system that can generate cover concepts, trailer stills, pitch visuals, social assets, and UI artifacts without canon drift.

Keep the blade sharp: Lantern is not a character to see. Lantern is the pressure in the room.
