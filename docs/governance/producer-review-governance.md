# Producer Review Governance

**Sprint:** PUB-005  
**Status:** Active governance standard  
**Owner:** Lantern Publishing / EchoMedia Content Engine

## Purpose
Producer Review is the central approval layer for Lantern Publishing. It protects canon, continuity, IP, likeness, legal/reputation risk, emotional tone, publishing readiness, and brand value before any work becomes release-ready.

## Governance Position
Producer Review sits after drafting and canon review, but before final publishing package approval.

```text
Concept
  -> Writers Room
  -> Draft / Rewrite
  -> Canon Review
  -> Continuity Review
  -> Producer Review
  -> Publishing Package
  -> Release Gate
```

## Required Review Areas

### Canon
Does the artifact preserve established Lantern Universe truth?

### Continuity
Does the artifact maintain character state, timeline, location, event, and mythology consistency?

### IP
Does the artifact avoid unauthorized use of protected intellectual property?

### Likeness
Does the artifact avoid unsafe or unauthorized real-person likeness usage?

### Legal / Reputation Risk
Does the artifact reduce avoidable legal, defamation, privacy, or reputational exposure?

### Emotional Tone
Does the artifact deliver the intended tone without becoming exploitative, weak, or off-brand?

### Publishing Readiness
Is the artifact ready for proofreading, formatting, packaging, vendor preparation, and release sequencing?

### Brand Value
Does the artifact strengthen Lantern Publishing and EchoMedia rather than dilute the brand?

## Gate Decisions
Supported Producer Review decisions:

- `approve`
- `approve-with-notes`
- `revise`
- `block`
- `waive`

## Mandatory Use Cases
Producer Review is required for:

- full manuscripts
- final outlines
- trilogy roadmaps
- canon-changing edits
- character registry changes
- marketing packages
- audiobook packages
- publishing packages
- visual packages
- any real-person-inspired or sensitive material

## Review Record
Each review should produce a structured record validated by:

```text
schemas/publishing/producer-review.schema.json
```

## Release Rule
No book, case file, audiobook package, marketing package, or publishing package may be considered release-ready unless Producer Review is approved, approved with notes, or explicitly waived.

## Escalation Rule
If a Producer Review identifies unresolved risk in canon, likeness, legal exposure, emotional tone, or publishing readiness, the artifact must return to revision before packaging.

## Scale Rule
Producer Review must remain lightweight enough to operate across hundreds of books but strict enough to prevent canon drift, brand dilution, and release of unsafe material.
