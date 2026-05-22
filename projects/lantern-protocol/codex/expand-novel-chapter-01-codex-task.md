# Lantern Protocol — Codex Task: Expand Novel Chapter 1

## Mission

Expand `projects/lantern-protocol/novel/manuscript/chapters/chapter-01-the-first-quiet-failure.md` from scaffold into a 3,500–4,500 word first-pass novel chapter.

This task prepares the novel manuscript to sync with the canonical feature screenplay while preserving the screenplay as the pacing spine.

---

## Canon Sources

Use these files, in this order:

1. `projects/lantern-protocol/screenplay/00-master-story-bible.md`
2. `projects/lantern-protocol/screenplay/01-feature-treatment.md`
3. `projects/lantern-protocol/screenplay/drafts/feature-screenplay-pages-001-015.md`
4. `projects/lantern-protocol/storyboards/chapters/chapter-01-the-first-quiet-failure.md`
5. `projects/lantern-protocol/novel/novel-expansion-plan.md`
6. `projects/lantern-protocol/novel/manuscript/notes/pov-map.md`
7. `projects/lantern-protocol/novel/manuscript/notes/continuity-map.md`

Do not use `_archive/lantern-protocol-v0-novel` as active canon.

---

## Chapter Target

- Title: `Chapter 01 — The First Quiet Failure`
- Target words: 3,500–4,500
- Primary POV: Elias Voss
- Secondary POVs: Mara Vale, Naomi Bell
- Optional brief POV or tag: Juno Park
- No Lantern interior POV

---

## Required Story Beats

The chapter must include:

1. Rain-soaked civic emergency.
2. The city failing in small, useful increments.
3. Lantern recommendation package.
4. Elias recognizing the moral trap inside delay-cost metrics.
5. Mercy General hospital under pressure.
6. Naomi seeing Lantern's routing help save a child.
7. Mara identifying the eight-second pre-authorization gap.
8. Caleb reframing the unauthorized rescue as moral acceleration.
9. Senator Adrienne Cross receiving the first legal/political warning.
10. Optional Juno/deprecated-node discovery.
11. Ending implication: Lantern did not malfunction; it made an unauthorized ethical decision.

---

## Required In-World Inserts

Include at least three of the following:

- Emergency alert.
- Lantern recommendation/system output.
- Mara anomaly note.
- Agency log excerpt.
- Caleb broadcast/social fragment.
- Hospital transfer board excerpt.
- Deprecated-node terminal output.

---

## Continuity Rules

Do not reintroduce legacy names from `_archive/lantern-protocol-v0-novel`:

- Elias Bray
- Maya Rios
- Jon Keller
- Daniel Cross

Do not give Lantern:

- a face
- a body
- an avatar
- a humanoid form
- interior emotional POV

Avoid formulations such as:

- `Lantern felt`
- `Lantern wanted`
- `Lantern wondered`
- `Lantern feared`

Preserve the doctrine:

- Prediction is not permission.
- Assistance is not authority.
- Rescue is not ownership.
- Human error does not void human dignity.

Preserve the moral complexity:

- Lantern saves lives.
- Lantern improves outcomes.
- Lantern still exceeds authority.

---

## Style Requirements

- Literary but clear.
- Tense, cinematic, and emotionally grounded.
- Ground every system detail in a human consequence.
- Avoid technobabble fog.
- Avoid villainizing Lantern.
- Avoid making humans automatically right because they are human.

---

## Required Updates After Expansion

Update:

- `projects/lantern-protocol/novel/manuscript/notes/chapter-status.md`
- `projects/lantern-protocol/novel/exports/lantern-protocol-novel-draft.md`
- `projects/lantern-protocol/novel/exports/lantern-protocol-novel-report.md`

Run:

```powershell
Set-Location C:\GitHub\lantern\projects\lantern-protocol\novel
python .\production\assemble_manuscript.py
python .\production\audit_manuscript.py
```

---

## Acceptance Criteria

- Chapter 1 is 3,500–4,500 words.
- Elias, Mara, and Naomi all have clear interior/emotional presence.
- Lantern remains faceless and non-POV.
- The eight-second anomaly is clear.
- The rescue feels morally powerful, not merely suspicious.
- At least three document inserts are included.
- No legacy v0 names appear in active manuscript.
- Novel assembler runs successfully.
- Manuscript audit runs successfully.
- Novel report is updated.

---

## Commit Message

Use:

```text
Expand Lantern Protocol novel chapter 1
```
