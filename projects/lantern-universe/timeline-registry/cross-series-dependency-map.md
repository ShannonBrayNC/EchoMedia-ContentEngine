# Cross-Series Dependency Map

**Sprint:** PUB-008  
**Status:** Active dependency map  
**Registry:** Lantern Universe Timeline Registry

## Purpose
Track how Silver Bullet, The Voss Files, and Lantern Protocol Case Files connect without collapsing series independence.

## Dependency Principle
A dependency should clarify shared canon, not make one series unreadable without another.

## Core Dependencies

## Voss Files → Lantern Protocol
The Voss Files provides the deep mythology behind narrative-system corruption, Black Lantern, and the Living Anchor revelation.

### Key Dependency
`voss-living-anchor-revelation` supports `lantern-protocol-living-anchor-case`.

### Constraint
Lantern Protocol may reference the Living Anchor doctrine, but should not retell the full Voss trilogy inside case files.

## Canon Bible → All Series
PUB-006 Canon Bible governs:

- Living Anchor
- Narrative Corruption
- Witness Protocols
- Lantern
- Widow Circle
- Black Lantern

### Key Dependency
All timeline events that affect these concepts must follow Canon Bible definitions.

### Constraint
No series may redefine the Living Anchor as technology.

## Character Registry → Timeline Registry
PUB-007 Character Registry defines stable character IDs that timeline events must use.

### Key Dependency
Timeline events affecting Jack Mercer, Elias Voss, Evelyn Blackwood, or Widow Circle must use existing registry IDs.

### Constraint
Character-state changes must be added to timeline records before final Producer Review.

## Silver Bullet → Lantern Protocol
Silver Bullet contributes grounded witness-preservation themes and shows how narrative corruption destroys a life at human scale.

### Key Dependency
`jack-witness-adaptation` supports future case-file or trilogy continuity involving witness preservation.

### Constraint
Silver Bullet Book 1 should foreshadow Lantern without fully explaining the organization or mythology.

## Widow Circle → Silver Bullet Trilogy
Widow Circle is primarily a Silver Bullet antagonist system.

### Key Dependency
SB-002 Widow Circle design supports Silver Bullet Book 1 and later trilogy escalation.

### Constraint
The group should not become generic shared-universe villain machinery unless Producer Review approves that expansion.

## Black Lantern → Voss Files and Case Files
Black Lantern is most directly developed through The Voss Files and may appear as case-file material.

### Key Dependency
`black-lantern-truth-infrastructure-reveal` constrains future Black Lantern references.

### Constraint
Black Lantern must remain tied to corrupted truth infrastructure, not generic evil branding.

## Release-Order Guidance
Preferred development order:

1. Canon Bible
2. Character Registry
3. Timeline Registry
4. Silver Bullet Book 1 rewrite
5. Widow Circle and trauma integration
6. Voss mythology expansion
7. Lantern Protocol case-file expansion

## Producer Review Trigger
Any change that makes one series dependent on unreleased material from another series requires Producer Review.
