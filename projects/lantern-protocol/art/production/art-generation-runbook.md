# Art Generation Runbook

1. Confirm doctrine and guardrails in `../README.md`.
2. Select prompt pack and IDs from `../asset-manifest/`.
3. Append shared negative prompts to every generation request.
4. Generate low-resolution proofs only.
5. QA for policy/canon/style violations.
6. Record approved outputs metadata in `../exports/`.
7. Never commit binary images unless explicitly approved.
8. Run validator and archive report.
