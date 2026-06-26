# Pending Timeline Registry Update — SB-008

**Sprint:** SB-008  
**Status:** Pending safe in-place timeline update  
**Target File:** `projects/lantern-universe/timeline-registry/series/silver-bullet-timeline.yaml`

## Purpose
Record the required Timeline Registry update created by the Book 2 Title and Concept Lock sprint.

## Current Placeholder Event

```yaml
- event_id: silver-bullet-book-02-pattern-expansion
  event_title: Pattern expands beyond Jack's case
  book_id: book-02-to-be-defined
  timeline_position: book-02-placeholder
  canon_status: planned
```

## Required Replacement Direction

```yaml
- event_id: echo-ledger-pattern-expansion-begins
  event_title: The Echo Ledger pattern expansion begins
  book_id: book-02-the-echo-ledger
  event_scope: series
  timeline_position: book-02-opening-pattern-expansion
  relative_order: 100
  canon_status: canon-draft
  event_type: continuity-marker
  summary: >-
    Jack Mercer follows the surviving fragments from his own case into a broader
    ledger of prior targets, damaged witnesses, context-stripped records, and
    repeated narrative distortion patterns.
  affected_entities:
    - jack-mercer
    - widow-circle
    - mara-venn
  depends_on:
    - jack-witness-adaptation
  blocks_or_constrains:
    - echo-ledger-first-prior-case
  continuity_notes:
    - Replaces the Book 2 placeholder created during PUB-008.
    - Must align with SB-008 Book 2 concept lock.
    - Mara Venn may require Character Registry entry if retained as major character.
  producer_review_required: true
  risk_flags:
    - trilogy-continuity
    - witness-network
    - fictionalization-review
```

## Reason Not Applied Directly in SB-008
The fetched repository file view did not expose the current blob SHA required for a safe `update_file` mutation. This pending update records the exact registry change needed for a later safe timeline-sync sprint or manual update.

## Producer Note
This pending update does not block SB-008 completion. Book 2 is title-locked and concept-locked under `book-02-the-echo-ledger`.
