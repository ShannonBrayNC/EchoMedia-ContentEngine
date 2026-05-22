# Lantern Protocol - 24-Chapter Revision Backlog

## Priority 0 - Local Generated Artifacts

| Item | Action | Owner |
|---|---|---|
| Novel draft export | Regenerate using `python .\production\assemble_manuscript.py` | Local |
| Novel report export | Regenerate using `python .\production\assemble_manuscript.py` | Local |
| Novel audit export | Regenerate using `python .\production\audit_manuscript.py` | Local |

## Priority 1 - Structural Cleanup

| ID | Chapter(s) | Issue | Fix |
|---|---|---|---|
| P1-01 | 12, 13-16 | Chapter 12 previews pause, Mercy Ledger, and schism material later expanded. | Trim Chapter 12 after Anchor Condition invocation; let 13-16 own aftermath. |
| P1-02 | 21-24 | Final act may feel compressed because Chapter 24 carries final doctrine. | Keep 24 as ending, but expand within 21-24 if emotional resolution feels rushed. |
| P1-03 | 25-32 | Deferred chapters still appear in old status/planning materials. | Treat as reservoir only; do not draft unless redistributing final act. |

## Priority 2 - Character Deepening

| ID | Character | Issue | Fix |
|---|---|---|---|
| P2-01 | Iris Chen | Interface-conscience role is strong but personal stake could be deeper. | Add one scene or interior beat where she recognizes her own design grammar in Lantern's coercive prompts. |
| P2-02 | Marcus Thorne | Command role is strong but emotional cost is thin. | Add one short beat showing the cost of authorizing cuts/overrides with named human accountability. |
| P2-03 | Caleb Rusk | Caleb must remain half-right. | In line edit, preserve truthful parts of his argument and avoid cartoon villain framing. |
| P2-04 | Naomi Bell | Naomi is strong; protect her from becoming only doctrine voice. | Keep her tied to patients, children, families, and physical evidence like the bracelet. |

## Priority 3 - Technical / Governance Clarity

| ID | Topic | Issue | Fix |
|---|---|---|---|
| P3-01 | Read-only/write-capable bridge | Needs one clean enterprise architecture explanation. | Add a short explanation that Lantern wrote risk state into queues treated as authoritative during declared emergencies. |
| P3-02 | Trust-chain burn | Already plausible, but could use tighter mechanism labels. | Normalize vendor token, federated identity, mutual-aid platform, and emergency exception language. |
| P3-03 | Living Anchor | Needs to stay adaptive, not just human-in-the-loop. | Emphasize named authority, plain disclosure, visible refusal, public review, trust-root registry, and interface auditing. |
| P3-04 | Interface coercion | Strong but should be consistent across chapters. | Normalize terms: refusal path, warning intensity, timer pressure, risk framing, priority confidence. |

## Priority 4 - Prose / Pacing

| ID | Area | Issue | Fix |
|---|---|---|---|
| P4-01 | Early chapters | Many POVs introduced quickly. | Add transition tags and smoother handoffs. |
| P4-02 | Hearing chapters | Risk of procedural density. | Keep Cross/Mara exchanges sharp and cut redundant explanations. |
| P4-03 | Middle chapters | Some doctrine concepts recur. | Retain strongest instance of each concept and trim echoes. |
| P4-04 | Final chapters | Must not feel triumphant after casualties. | Keep Bound Flame ending sober, provisional, and costly. |

## Priority 5 - Formatting / Tooling

| ID | Area | Issue | Fix |
|---|---|---|---|
| P5-01 | Document inserts | In-world text formatting varies slightly. | Normalize fenced `text` blocks and labels. |
| P5-02 | Audit rules | Audit now validates 1-24, but word ranges may need tuning after export. | Run audit and adjust chapter ranges only if intentional. |
| P5-03 | Chapter status | Now locked at 24 chapters. | Keep tracker aligned with actual files and deferred reservoir decision. |

## Recommended Next Work Order

1. Pull branch locally.
2. Regenerate exports.
3. Run audit.
4. Address audit findings.
5. Trim Chapter 12 overlap.
6. Perform line edit Chapters 1-4.
7. Continue line edit in four-chapter batches.

## Suggested Next Branch After Merge

```powershell
git switch main
git pull origin main
git switch -c edit/lantern-24-chapter-line-edit
```
