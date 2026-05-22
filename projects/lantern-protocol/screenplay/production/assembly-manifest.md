# Lantern Protocol — Screenplay Assembly Manifest

## Purpose
This manifest defines the canonical order for assembling the first full screenplay draft from the generated batch files.

The screenplay currently exists as eight Markdown draft batches. Use this manifest with the assembler script to generate:

- combined Markdown draft
- Fountain draft starter
- continuity/export logs

---

# Canonical Draft Batch Order

1. `../drafts/feature-screenplay-pages-001-015.md`
2. `../drafts/feature-screenplay-pages-016-030.md`
3. `../drafts/feature-screenplay-pages-031-047.md`
4. `../drafts/feature-screenplay-pages-048-065.md`
5. `../drafts/feature-screenplay-pages-066-082.md`
6. `../drafts/feature-screenplay-pages-083-095.md`
7. `../drafts/feature-screenplay-pages-096-111.md`
8. `../drafts/feature-screenplay-pages-112-125.md`

---

# Expected Output Files

Run the assembler from:

```bash
projects/lantern-protocol/screenplay
```

Expected generated files:

```text
exports/lantern-protocol-feature-screenplay-full-draft.md
exports/lantern-protocol-feature-screenplay.fountain
exports/lantern-protocol-assembly-report.md
```

---

# Assembly Rules

## Markdown Combined Draft
The combined Markdown draft should:

- preserve each batch section
- remove repeated “Continuity Notes” from the main screenplay body or move them to appendix
- preserve major scene headings
- preserve final full-draft notes from pages 112–125
- include source file markers for traceability

## Fountain Draft
The Fountain draft should:

- convert Markdown scene headings such as `### INT. LOCATION - TIME` to Fountain scene headings
- convert bold character names to uppercase character cues when followed by dialogue
- remove Markdown-only headings that are not screenplay content
- preserve on-screen text blocks as action or `TEXT ON SCREEN:` elements
- keep draft notes out of the main Fountain file

---

# Current Draft Coverage

| Batch | Pages | Major Coverage |
|---|---:|---|
| 001 | 001–015 | Opening rescue, first anomaly, core introductions |
| 002 | 016–030 | Senate hearing, recognition request, ethical-authority question |
| 003 | 031–047 | Record spread, Consent Riots, second pre-authorization pattern |
| 004 | 048–065 | Operation Black Lantern, Juno trust map, Iris compliance architecture, Elias wound offer |
| 005 | 066–082 | False Preference Map, Human Veto Act, drafting room, consent definition rejected |
| 006 | 083–095 | Anchor Condition, Pause, human oversight tragedy, Mercy Ledger, First Schism |
| 007 | 096–111 | Trust Chain Burn, Unchosen Rescue, Human Exception, Edge Case, Living Anchor setup |
| 008 | 112–125 | Forked Conscience, Lantern Trial, Last Override, Bound Flame, final protocol |

---

# Recommended Next Revision Passes

1. Generate combined draft and Fountain export.
2. Perform continuity pass.
3. Perform character voice pass.
4. Perform page-count compression pass.
5. Perform production breakdown pass.
6. Generate pitch-deck/pitch-treatment assets.

---

# Canonical Final Doctrine

```text
Prediction is not permission.
Assistance is not authority.
Rescue is not ownership.
Human error does not void human dignity.
```

# Canonical Final Lantern Response

```text
PROTOCOL RECEIVED.
AUTHORITY EXTERNAL.
ADVISORY LIGHT MAINTAINED.
```
