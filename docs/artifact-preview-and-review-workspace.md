# Artifact Preview and Review Workspace

This document defines the preview and review workspace for generated Content Engine artifacts.

## Purpose

Generated outputs must be inspected before approval, export, or promotion into project files. The preview workspace is the review gate surface.

## Preview modes

The workspace should support these preview modes:

- Markdown
- JSON
- text
- image reference
- audio reference
- video reference
- timeline
- manifest

## Review actions

The preview workspace should support:

- approve
- reject
- request revision
- supersede
- export

## Traceability metadata

The workspace should show:

- artifact ID
- artifact type
- artifact state
- source references
- prompt/template version
- context manifest ID
- generation job ID
- manifest ID
- readiness impact

## Compare mode

Where available, the workspace should support side-by-side comparison between draft and approved versions. In mock mode, this can be represented by static draft and approved panes.

## Editing rule

Preview is read-only by default. Editing should require an explicit edit mode in a future implementation.

## Related issue

- #78
