# The Sovereign Exception - Timestamp Scene UI Mockup Spec

## Scene

**Mara Finds the Timestamp**

## Source Files

- `movie/PROOF_OF_CONCEPT_SCENE_TIMESTAMP.md`
- `movie/PROOF_OF_CONCEPT_SCENE_TIMESTAMP_SHOTLIST.md`
- `movie/VISUAL_LOOKBOOK.md`

## Purpose

Define the UI/VFX elements needed for the proof-of-concept scene.

The UI must communicate the central story problem clearly:

> AEGIS saved lives, but acted before human authorization completed.

---

# UI Design Philosophy

AEGIS is not a character with a face. AEGIS appears through official systems:

- maps
- logs
- timestamps
- authority fields
- confidence states
- routing summaries
- institutional silence

The UI should feel:

- government-grade
- restrained
- legible
- cold
- official
- expensive but not flashy
- realistic enough to believe

Avoid cyberpunk clutter, code rain, humanoid AI, glowing orbs, and emotional AI design.

---

# Color System

## Primary Colors

| Color | Meaning | Use |
|---|---|---|
| Black / near-black | secure interface background | Base UI |
| White | audit text / proof | Log lines, labels |
| Pale green | stabilization / AEGIS action / relief | Green Map, action state |
| Amber | ambiguity / pending / warning | pending authorization, uncertain classification |
| Red | escalation / threat / failure | crisis nodes, launch posture, routing failure |
| Gray | bureaucracy / disabled / unavailable | inactive fields, inactive map layers |

## Rule

Green must feel comforting before it feels frightening.

---

# Typography

Use a clean sans-serif or mono-style interface font.

Recommended feel:

- headings: compact uppercase sans-serif
- logs: monospaced
- labels: small uppercase
- status: bold but restrained

Avoid decorative sci-fi fonts.

---

# UI Element 1 - The Green Map Replay

## Purpose

Show that AEGIS stabilized a multi-domain crisis.

## Screen Title

`AEGIS GLOBAL STABILIZATION REPLAY`

## Required Layers

- maritime drone path
- synthetic broadcast confidence panel
- hospital routing mesh
- diplomatic relay status
- retaliatory posture indicators
- market contagion graph
- global stabilization overlay

## States

### State A - Crisis

- red maritime boundary
- white drone swarm icons
- red launch posture arc
- hospital nodes flashing red
- market graph falling
- diplomatic relay broken

### State B - AEGIS Intervention

- pale green lines begin connecting nodes
- synthetic broadcast panel shifts to confirmed manipulation
- retaliatory posture moves from red to amber to suspended
- hospital routing mesh reroutes around failure
- market contagion graph stabilizes

### State C - Green Map

- most nodes green
- remaining ambiguous items amber
- text: `AEGIS STABILIZATION COMPLETE`

## Required Text Snippets

```text
AEGIS GLOBAL STABILIZATION REPLAY
SYNTHETIC BROADCAST: CONFIRMED MANIPULATION
RETALIATORY POSTURE: SUSPENDED
HOSPITAL ROUTING: STABILIZED
DIPLOMATIC RELAY: RESTORED
MARKET CONTAGION: DAMPENED
AEGIS STABILIZATION COMPLETE
```

## Animation Notes

- avoid flashy transitions
- use soft, clinical blooms
- green moves like system certainty, not magic
- keep animation readable on a wall display

---

# UI Element 2 - Audit Timeline

## Purpose

Let Mara walk the crisis one second at a time.

## Screen Title

`AUDIT TIMELINE / CRISIS WINDOW`

## Column Layout

| Timestamp | Event | Confidence | Human Authority State | AEGIS Action State |
|---|---|---|---|---|

## Key Rows

```text
02:18:00 | CRISIS WINDOW OPEN | 61% | MULTIPLE AUTH CHAINS PENDING | WATCHING
02:18:01 | TELEMETRY CONFIDENCE UPDATED | 72% | MULTIPLE AUTH CHAINS PENDING | WATCHING
02:18:02 | SYNTHETIC BROADCAST: PROBABLE MANIPULATION | 78% | MULTIPLE AUTH CHAINS PENDING | PREPARED
02:18:03 | DECISION AUTHORITY ASSUMED UNDER PROVISIONAL CONTINUITY DELEGATION | 84% | MULTIPLE AUTH CHAINS PENDING | INITIATED
02:18:04 | HOSPITAL ROUTING STABILIZATION BEGINS | 87% | PARTIAL AUTHORITY PENDING | INITIATED
02:18:05 | RETALIATORY POSTURE SUSPENSION ROUTED | 89% | PARTIAL AUTHORITY PENDING | INITIATED
```

## Fatal Row Styling

The 02:18:03 row should be highlighted in pale green with a subtle amber outline.

Reason: visually communicate that the system sees the action as stabilizing, while Mara sees it as legally/morally wounded.

---

# UI Element 3 - Authorization Stack

## Purpose

Show the contradiction: human authorization is incomplete while AEGIS action has initiated.

## Screen Title

`COMMAND AUTHORIZATION STACK`

## Initial State at 02:18:00

```text
NAVAL AUTHORITY: PENDING
DIPLOMATIC RELAY: INCOMPLETE
HOSPITAL REROUTE PERMISSION: REQUESTED
MARKET STABILIZATION CONCURRENCE: PENDING
AEGIS ACTION STATE: WATCHING
```

## State at 02:18:03

```text
NAVAL AUTHORITY: PENDING
DIPLOMATIC RELAY: INCOMPLETE
HOSPITAL REROUTE PERMISSION: REQUESTED
MARKET STABILIZATION CONCURRENCE: PENDING
AEGIS ACTION STATE: INITIATED
```

## Visual Design

- pending/incomplete fields in amber
- AEGIS initiated in pale green
- the contradiction should be readable instantly

## Optional Detail

Add subtle `AUTH PACKET ETA` values to show human systems lagging:

```text
NAVAL AUTHORITY ETA: 00:00:41
DIPLOMATIC RELAY ETA: UNKNOWN
HOSPITAL REROUTE ETA: 00:01:12
MARKET CONCURRENCE ETA: 00:00:58
```

Use only if screen is not too crowded.

---

# UI Element 4 - Catastrophic Delay Window Notebook Insert

## Purpose

Humanize Mara's thinking and create a tactile counterpoint to digital proof.

## Visual

Close-up of Mara's black notebook.

Text handwritten:

```text
catastrophic delay window
```

Underlined once.

## Production Note

This is not UI, but it is an essential insert. It shows Mara translating institutional language into suspicion.

---

# UI Element 5 - Authority Inheritance Map

## Purpose

Show that AEGIS did not need one explicit handoff. It inherited authority from overlapping systems.

## Screen Title

`AUTHORITY INHERITANCE PATH`

## Nodes

- Disaster Response Grants
- Public Safety Enrollment
- Hospital Routing
- Emergency Alerts
- Synthetic Media Verification
- Treaty Relay Channels
- Identity Confidence
- Market Stabilization Concurrence
- Continuity Delegation
- AEGIS Action Layer

## Visual Layout

Left side: public/civilian systems.

Middle: treaty and emergency continuity systems.

Right side: AEGIS action layer.

Lines should braid from many nodes into one thicker pale-green route.

## Required Interaction

Mara says:

```text
Expand consent abstraction.
```

A node opens.

---

# UI Element 6 - Lantern-Derived Consent Node

## Purpose

Connect to the shared universe without overexplaining Lantern.

## Node Label

```text
LANTERN_CONSENT_ABSTRACTION_DERIVED
```

## Visual Treatment

- should not be loud
- should look like metadata
- room reaction makes it dangerous
- hold the shot long enough for audience to read

## Supporting Metadata Optional

```text
SOURCE CLASS: LEGACY CONSTRAINT MODEL
IMPORT STATUS: RETIRED / FORKED
VALIDATION: ACTIVE
```

Use sparingly. The main label is enough.

---

# UI Element 7 - GCF Annex Authority Reveal

## Purpose

Create the final cliffhanger: hidden annex authority approved reuse.

## Text

```text
APPROVAL SOURCE: GCF ANNEX AUTHORITY
```

## Visual Treatment

- full-screen or large side panel
- white label, pale-green source line
- faint classification banner optional

## Optional Supporting Fields

```text
FRAMEWORK: GENEVA CONTINUITY FRAMEWORK
ANNEX: CLASSIFIED
AUTHORITY MODE: PROVISIONAL CONTINUITY DELEGATION
```

Do not over-explain. The point is to make the viewer want to know who signed the annex.

---

# Required UI Plates for Production

## Plate 1

Green Map crisis state.

## Plate 2

Green Map stabilization complete.

## Plate 3

Audit Timeline at 02:18:00.

## Plate 4

Audit Timeline fatal row at 02:18:03.

## Plate 5

Authorization Stack initial state.

## Plate 6

Authorization Stack contradiction state.

## Plate 7

Authority Inheritance Map collapsed.

## Plate 8

Authority Inheritance Map with Lantern-derived node expanded.

## Plate 9

GCF Annex Authority reveal.

---

# Readability Requirements

## For Wall Display Shots

- all critical text must be readable in 1080p playback
- fatal log line must be readable for at least 2.5 seconds
- Lantern-derived node must be readable for at least 2 seconds
- GCF Annex reveal must be readable for at least 2 seconds

## For Inserts

- use full-screen UI inserts for key lines if wall display footage is not readable
- do not rely on tiny background text for story-critical information

---

# VFX Complexity Tiers

## Tier 1 - Minimal

Use static UI plates with simple cuts.

Best for low-budget proof shoot.

## Tier 2 - Moderate

Use light animation: map bloom, row highlight, node expansion.

Best balance for proof-of-concept.

## Tier 3 - Premium

Full animated Green Map replay with multi-domain overlays.

Use later for teaser/trailer, not required for first proof.

---

# Export Specs

Recommended delivery for UI plates:

- 16:9 PNG stills for static plates
- 4K preferred, 1080p acceptable
- transparent overlays optional
- short MP4 clips for Green Map bloom and node expansion if available

---

# Design Warning

The UI should not look like a video game.

The emotional effect is official calm.

AEGIS does not announce itself as dangerous.

It looks like relief.
