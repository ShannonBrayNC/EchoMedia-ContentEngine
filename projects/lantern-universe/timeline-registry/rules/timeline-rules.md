# Timeline Rules

**Sprint:** PUB-008  
**Status:** Active timeline governance  
**Registry:** Lantern Universe Timeline Registry

## Purpose
Timeline rules prevent chronology drift, character-state drift, mythology drift, and release-order mistakes as the Lantern Universe scales.

## Rule 1: Stable Event IDs
Every major timeline event must have a stable `event_id`. Once used in dependencies, the ID must not be renamed without a migration note.

## Rule 2: Relative Order Before Absolute Dates
Use `relative_order` and `timeline_position` until exact dates are canon-locked. Avoid assigning exact dates too early.

## Rule 3: Character-State Events Must Be Tracked
Any event that changes a character's status, reputation, trust, injury state, institutional position, relationship, or witness role must be added to the relevant timeline.

## Rule 4: Mythology Reveals Require Dependencies
Major reveals about Living Anchor, Black Lantern, Lantern, Witness Protocols, or Narrative Corruption must include `depends_on` and `blocks_or_constrains` fields.

## Rule 5: Series Autonomy Must Be Protected
Each series should remain readable on its own. Timeline dependencies may connect series, but they should not make one trilogy incomprehensible without another.

## Rule 6: Book 1 Should Not Resolve Trilogy-Level Mystery
Silver Bullet Book 1 may foreshadow Lantern and Living Anchor themes, but it should not fully explain or resolve the entire shared mythology.

## Rule 7: Voss Files Independence
The Voss Files remains independent and must preserve its own internal chronology. Voss mythology can support Lantern but must not be reduced to Silver Bullet exposition.

## Rule 8: Case Files Support, Not Override
Lantern Protocol Case Files may clarify, echo, or deepen canon, but they should not casually override trilogy events.

## Rule 9: Producer Review for Timeline Changes
Producer Review is required when a timeline change affects canon, mythology, character state, release strategy, or cross-series dependency.

## Rule 10: Conflict Handling
If a conflict is found, mark the event `canon_status: conflict` and resolve through documented revision. Do not silently overwrite timeline history.

## Review Checklist
Before a timeline event is canon-locked, verify:

- Canon Bible alignment
- Character Registry alignment
- Series continuity
- Cross-series dependencies
- Producer Review status
- Risk flags
- Release-order implications
