# Lantern Universe Timeline Registry

**Sprint:** PUB-008  
**Status:** Active registry  
**Owner:** Lantern Publishing / EchoMedia Content Engine

## Purpose
The Timeline Registry is the canonical chronology layer for the Lantern Universe. It prevents timeline drift across Silver Bullet, The Voss Files, Lantern Protocol Case Files, character profiles, canon events, and future publishing packages.

## Registry Scope
The registry tracks:

- universe-level events
- series-level events
- book-level events
- case-file events
- character-state changes
- organization-state changes
- mythology reveals
- evidence and witness milestones
- cross-series dependencies
- release-order implications

## Canon Rule
A timeline event that affects canon, character state, public reputation, institutional status, mythology, or series continuity must be recorded before the related manuscript or publishing package can move to final Producer Review.

## Structure

```text
timeline-registry/
├── README.md
├── schemas/
│   └── timeline-event.schema.json
├── master/
│   └── lantern-master-timeline.yaml
├── series/
│   ├── silver-bullet-timeline.yaml
│   ├── voss-files-timeline.yaml
│   └── lantern-protocol-case-files-timeline.yaml
├── rules/
│   └── timeline-rules.md
├── cross-series-dependency-map.md
├── validation/
│   └── PUB-008-validation-report.md
└── sprint-status/
    └── PUB-008.md
```

## Timeline Event Status Values

- `planned`
- `drafted`
- `canon-draft`
- `canon-locked`
- `conflict`
- `retired`

## Required Review Gates
Timeline-impacting events require:

1. Canon Bible check
2. Character Registry check
3. Series continuity check
4. Cross-series dependency check
5. Producer Review if the event changes canon, character state, mythology, or release strategy

## Initial Series Coverage

- Silver Bullet Trilogy
- The Voss Files Trilogy
- Lantern Protocol Case Files

## Follow-Up Work
Future sprints should add timeline validators, automated schema checks, chapter-linked event extraction, and publishing calendar integration.
