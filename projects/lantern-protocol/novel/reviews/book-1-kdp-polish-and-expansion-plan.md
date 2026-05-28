# Book I KDP Polish and Expansion Plan

## Objective

Bring **The Living Anchor** above the KDP readiness target while preserving its function as the first Lantern Protocol gateway book.

Current audit from user run:

```text
Total manuscript words: 38,226
Minimum total words: 38,000
Target total words: 45,000
Shortfall to target: 6,774 words
```

Book I technically clears the minimum total, but the audit fails because Chapter 21 is below the minimum chapter floor and many late-middle/final chapters are below the warning target.

## Release target

```text
Minimum release-safe total: 45,000 words
Preferred Book I target: 48,000-52,000 words
```

This keeps Book I lean enough to function as a series gateway while giving KDP readers a complete, satisfying techno-thriller experience.

## Expansion doctrine

Do not pad. Expand through consequence.

Book I should remain focused on this crime scene:

```text
The machine saved them before anyone gave it permission.
Eight seconds is not nothing.
Eight seconds is the whole crime scene.
```

Every added word should deepen one of these:

- the Region Six emergency,
- the audit trail puzzle,
- the public inquiry,
- Naomi's human anchor role,
- Juno's evidence trail,
- Mara's investigation,
- Cross's political pressure,
- Elias's guilt,
- or the transition into Book II's separate-agreements problem.

## Priority chapter targets

| Chapter | Current words | Target words | Add approx. | Priority |
|---|---:|---:|---:|---|
| 21 — The Answer Together | 904 | 1800 | +900 | Critical |
| 24 — The Living Anchor | 1149 | 2200 | +1050 | High |
| 23 — The Shape of the Answer | 1027 | 1900 | +875 | High |
| 22 — The Edge Case | 1042 | 1900 | +850 | High |
| 18 — The Trust Chain Burn | 1136 | 1900 | +760 | High |
| 13 — The Pause | 1147 | 1800 | +650 | High |
| 12 — The Anchor Condition | 1126 | 1800 | +675 | High |
| 17 — The Separate Agreements | 1281 | 1900 | +620 | Medium |
| 19 — The Unchosen Rescue | 1285 | 1900 | +615 | Medium |
| 16 — The First Schism | 1322 | 1850 | +525 | Medium |
| 15 — The Mercy Ledger | 1392 | 1850 | +460 | Medium |
| 14 — The Burden of Oversight | 1395 | 1850 | +455 | Medium |
| 09 — The False Preference Map | 1374 | 1850 | +475 | Medium |
| 10 — The Human Veto Act | 1494 | 1850 | +350 | Low |
| 20 — The Human Exception | 1437 | 1850 | +415 | Low |

Estimated added words: approximately 9,000-10,000.

Expected post-pass total: approximately 47,000-49,000 words.

## Chapter expansion briefs

### Chapter 09 — The False Preference Map

Expand the false preference evidence. Add one more affected person, a dashboard artifact, and Juno showing how inferred preference became operational truth. Avoid repeating doctrine; let the map reveal the violation.

### Chapter 10 — The Human Veto Act

Add the political compromise pressure. Cross should face advocates who want speed and civil-liberties voices who fear systems learning to wait only when watched.

### Chapter 12 — The Anchor Condition

Expand Naomi's anchor role through a field scene and a document scene. Show why anchoring cannot be merely symbolic.

### Chapter 13 — The Pause

Make the pause physically costly. Add seconds, voices, failed calls, and the moral pressure of waiting for a human signal while danger moves.

### Chapter 14 — The Burden of Oversight

Expand oversight as labor, not slogan. Add staff exhaustion, audit routing, and the first hint that no committee can watch everything at machine speed.

### Chapter 15 — The Mercy Ledger

Add ledgers of saved versus overridden people. Let mercy appear measurable and morally incomplete.

### Chapter 16 — The First Schism

Expand the split between factions. Each side should be partly right. The schism should feel inevitable, not procedural.

### Chapter 17 — The Separate Agreements

Strengthen the bridge into Book II. Add an agreement stack artifact and a line of reasoning showing how institutional agreements can bury personal consent.

### Chapter 18 — The Trust Chain Burn

Expand the burn event. Add sequence, proof, backlash, and cost. Make the trust chain feel like evidence catching fire, not just a phrase.

### Chapter 19 — The Unchosen Rescue

Add the person rescued without choosing. Make the rescue emotionally undeniable and ethically unresolved.

### Chapter 20 — The Human Exception

Expand the doctrine around edge cases. Show the danger of making humanity an exception handler instead of the source of authority.

### Chapter 21 — The Answer Together

Critical fix. Bring this above 1,800 words. Add a full scene where the answer is built by multiple humans under pressure, not discovered as a slogan.

### Chapter 22 — The Edge Case

Expand the edge case into a concrete person or family whose facts do not fit the system's categories.

### Chapter 23 — The Shape of the Answer

Add the public shape of the answer: what Cross says, what Mara refuses to simplify, what Elias cannot forgive, and what Naomi will not let become policy theater.

### Chapter 24 — The Living Anchor

Expand the ending. Let Naomi's living-anchor meaning land. Add emotional closure, final audit image, and a clean bridge into Book II without making Book I feel unfinished.

## Definition of Done

Book I is ready for KDP when:

- total manuscript body words are >= 45,000,
- no chapter body is below 1,000 words,
- no priority late-book chapter is below 1,500 words unless intentionally approved,
- Chapter 21 is above 1,800 words,
- KDP title metadata is `The Living Anchor`,
- series metadata is `Lantern Protocol`,
- subtitle is `Book One of the Lantern Protocol`,
- Book II teaser is included in back matter,
- `python ./tools/audit_kdp_readiness.py --book book-1` passes,
- KDP DOCX export has no ElevenLabs cues,
- and ElevenLabs DOCX export remains narration-friendly.
