# Sprint 4 - Preview Review Gate and Artifact Traceability

## Status

Complete.

## Related issues

- #38 - Add preview/review gate before generated artifacts are saved
- #36 - Add artifact traceability from manuscript to screenplay to video package

## Sprint goal

Prevent generated artifacts from silently entering project folders without review, and ensure every generated artifact can be traced back to its source material, generation job, review decision, and downstream exports.

Sprint 4 turns generated content from loose output into auditable production work.

---

## Completed deliverables

### 1. Review gate schema

Added:

`schemas/workflows/review-gate.schema.json`

The review gate schema defines the lifecycle required before a generated artifact can be saved, exported, or committed.

It tracks:

- Review identity
- Project slug
- Artifact identity
- Artifact type
- Source generation job
- Review state
- Preview format/path
- Destination path
- Required checks
- Review decision
- Persistence permission
- Commit/save metadata

### 2. Artifact traceability schema

Added:

`schemas/workflows/artifact-traceability.schema.json`

The traceability schema links source materials, dependencies, downstream outputs, canon impact, generation jobs, and review gates.

It tracks:

- Source links
- Dependency links
- Downstream artifacts
- Canon impact
- Required regeneration hints
- Review and generation job references

---

## Review gate lifecycle

Generated artifacts should move through this lifecycle:

```text
draft
  -> pending-review
    -> changes-requested or approved or rejected
      -> saved or exported or superseded
```

### Draft

The artifact exists only as generated preview output.

It is not final.
It is not committed.
It is not exported.

### Pending review

The artifact has enough structure to be reviewed and checked.

Required checks should include:

- Schema validation
- Source context present
- Traceability present
- Canon safety
- Visual continuity safety
- Destination path validity
- Overwrite review
- Export readiness, when applicable

### Changes requested

The artifact is not approved, but may be regenerated or edited.

### Approved

The artifact is approved for save/export.

Approval does not automatically write files.

### Saved / exported

The artifact has moved from preview output into a project artifact folder or export package.

---

## Required review checks

| Check | Purpose |
|---|---|
| `schema-valid` | Confirms the artifact matches its expected schema. |
| `source-context-present` | Confirms the artifact was generated from known project/source context. |
| `traceability-present` | Confirms the artifact can be traced to its sources. |
| `canon-safe` | Confirms no locked canon change slipped in silently. |
| `visual-continuity-safe` | Confirms visual consistency rules were considered. |
| `destination-path-valid` | Confirms the save/export path is valid for the project. |
| `overwrite-reviewed` | Confirms any overwrite risk was explicitly reviewed. |
| `export-ready` | Confirms target export profiles have the required fields. |

---

## Traceability relationship model

Trace links use explicit relationship types.

Recommended relationships:

| Relationship | Meaning |
|---|---|
| `derived-from` | Artifact was generated from the linked source. |
| `depends-on` | Artifact requires the linked source to remain valid. |
| `updates` | Artifact changes or updates the linked artifact. |
| `supersedes` | Artifact replaces a prior artifact. |
| `generates` | Artifact/job creates a downstream artifact. |
| `exports-to` | Artifact is exported into a target package. |
| `validates-against` | Artifact is checked against the linked source. |
| `blocks-save-until-reviewed` | Linked item must be reviewed before save. |
| `affected-by` | Artifact may require regeneration when the linked item changes. |

---

## End-to-end trace example

```text
Manuscript chapter
  -> screenplay scene
    -> scene card
      -> storyboard panel set
        -> visual prompt pack
          -> production package
            -> tool-specific export
```

Each step should have trace links back to source materials and forward to downstream outputs.

---

## Canon impact rules

Generated artifacts that touch locked or approved canon should not be saved without review.

Canon impact should track:

- Whether locked canon is touched.
- Whether a canon change request is required.
- Affected canon paths.
- Affected downstream paths.
- Whether regeneration is recommended.

---

## Persistence rules

A generated artifact may be saved only when:

1. A review gate exists.
2. Required checks are passed or explicitly waived.
3. Review decision is approved.
4. Persistence target path is known.
5. Any overwrite risk has been reviewed.

The engine must not silently save generated drafts into final project artifact folders.

---

## Minimum future implementation slice

The first Sprint 4 implementation PR should support this narrow path:

1. Accept a generated production package draft from a Sprint 3 generation job.
2. Create a review gate in `pending-review` state.
3. Create a traceability record linking the package to source refs and generation job.
4. Run basic checks:
   - schema valid
   - source context present
   - traceability present
   - destination path valid
5. Allow user approval.
6. Mark persistence as allowed only after approval.

Do not implement every canon/visual audit in the first PR.

---

## Relationship to Sprint 5

Sprint 5 should use the review gate and traceability states in the compact workflow/status rail.

The rail should show:

- Current generation state
- Review state
- Failed checks
- Approval status
- Export readiness
- Next action

---

## Definition of done

- [x] Review gate schema added.
- [x] Artifact traceability schema added.
- [x] Review lifecycle documented.
- [x] Required review checks documented.
- [x] Trace relationship model documented.
- [x] Canon impact rules documented.
- [x] Persistence rules documented.
- [x] Minimum future implementation slice identified.

## Next sprint

Sprint 5 should address:

- #34 - Replace redundant order display with compact workflow/status rail
