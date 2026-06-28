# Lantern Protocol Art Production Package

This package defines a controlled, reproducible visual production system for **Lantern Protocol**.

## Structure
- `asset-manifest/` — canonical inventory of all requested visual assets.
- `prompts/` — prompt packs grouped by production stream.
- `reference/` — non-generative reference notes and source links.
- `exports/` — approved generated outputs metadata (no binary images by default).
- `production/` — runbook and execution artifacts.
- `qa/` — validation script outputs and compliance checks.

## Guardrails (Mandatory)
- No Lantern avatar.
- No robot Lantern.
- No humanoid Lantern.
- No Lantern face.
- No celebrity likenesses.
- No copyrighted/franchise styles.
- No new story canon.
- No generated binary images committed unless explicitly approved.

## Doctrine (Must Preserve)
- Prediction is not permission.
- Assistance is not authority.
- Rescue is not ownership.
- Human error does not void human dignity.

## Validation
Run:

```bash
python3 projects/lantern-protocol/art/production/validate_art_package.py
```

Validation writes:
- `art/qa/art-package-validation-report.md`

