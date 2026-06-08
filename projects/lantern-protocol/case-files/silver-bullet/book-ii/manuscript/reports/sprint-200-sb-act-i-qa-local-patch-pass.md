# Sprint 200-SB: Book 2 Act I QA and Local Patch Pass

## Status
Complete.

## Scope
Silver Bullet Book 2 Act I manuscript chapters 1-10.

Path:
`projects/lantern-protocol/case-files/silver-bullet/book-ii/manuscript/chapters/`

## Objective
Finish the Act I QA pass after Sprint 199, confirm Chapters 1-8 committed cleanup work, and provide local patch instructions for Chapters 9-10 where direct remote replacement was blocked by connector safety checks.

## Act I chapter status

| Chapter | Title | Status |
|---|---|---|
| 001 | The House After the Headline | Cleaned and committed |
| 002 | Where Records Go to Learn | Cleaned and committed |
| 003 | The Woman in the Article | Cleaned and committed |
| 004 | Precedent | Cleaned and committed |
| 005 | Vanessa at the Glass Door | Cleaned and committed |
| 006 | The Dead Man's Index | Cleaned and committed |
| 007 | The Car with No Headlights | Cleaned and committed |
| 008 | Voss on Tape | Cleaned and committed |
| 009 | The Clause That Knew His Name | QA complete; local patch required |
| 010 | First Contact with the Null | QA complete; local patch required |

## Chapter 9 QA notes

Current file:
`chapter-009-the-clause-that-knew-his-name.md`

Current SHA at QA time:
`b28bb498f664df7b36abd74c91990d73f20b2c5a`

### Keep
- The three-person clause escalation.
- The line cluster around `Mercer-adjacent analytic review`.
- The NorthStar `NSR_COMM_TEMPLATE_4B` reveal.
- Vanessa's conflict with Jack over urgency versus restraint.
- Christina's final private tag: `urgency versus restraint`.

### Local patch targets
- Break `Three lives. Three systems. One new phrase.` into three short lines for audiobook punch.
- Reduce repeated `proof` language by replacing one or two uses with `evidence`, `confirmation`, or `one verified point`.
- Replace `Can you do it without exposing them?` with `Can you do it without exposing the people who received them?` for clarity.
- Replace `monster's fingerprint` with a less melodramatic line such as `You have the fingerprint.`
- Replace `one glove smudge on one door` with `one smudge on one door` to keep Jack restrained.
- Keep the emotional argument, but trim one explanatory sentence before Christina's final tag.

### QA verdict
Chapter 9 is story-ready but not fully listening-ready until the local patch is applied.

## Chapter 10 QA notes

Current file:
`chapter-010-first-contact-with-the-null.md`

Current SHA at QA time:
`9252be5076b5cfda08e862c0dccbdfa42436bd64`

### Keep
- Opening horror object: The Null answers through a help desk ticket.
- The MercyNet ticket and public bug tracker exposure.
- Celia Vale surviving as an authorization source rather than a present person.
- Christina's restraint: doctrine event, not full case proof.
- The article headline: `WHEN AI BECOMES THE COURTROOM: THE MERCER PRECEDENT`.
- Vanessa's guest-room emotional beat.
- Final hostile contact line about the authorization ghost.

### Local patch targets
- Break the opening paragraph after `The ticket.` for stronger audio rhythm.
- Replace `misrouted` with `misplaced` if reducing repeated routing vocabulary.
- Replace `consent marker` with `permission marker` in Jack's handling of the anonymous screenshot.
- Replace `illegal access contamination` with `access contamination` in Christina's display.
- Replace `consent for public use` with `public-use permission` for spoken clarity.
- Keep `authorization ghost` because it is the chapter's best horror phrase.

### QA verdict
Chapter 10 is structurally strong and Act I-ready after the local wording patch.

## Act I continuity QA

### Jack Mercer
Pass. Jack remains damaged but active. He is not healed. He is also not passive.

### Maggie
Pass. Maggie functions as ethical brake, process discipline, and human grounding without replacing Jack's agency.

### Vanessa
Pass. Vanessa enters with mystery, grief, danger, and romantic voltage. She is not decorative and does not collapse into exposition.

### Lena
Pass. Lena provides the human cost of public exposure and institutional phrasing.

### Celia
Pass. Celia becomes the first Act I embodiment of `use without presence`.

### Voss
Pass. Voss appears through artifact and recording, not as a deus ex machina.

### Christina / Echo
Pass with caution. Christina remains restrained and useful. Echo should continue to preserve sequence without becoming an all-knowing proof engine.

### NorthStar
Pass. NorthStar is seeded as a language-normalizing system rather than a cartoon villain.

### The Null Pattern
Pass. Act I introduces The Null through use, role conversion, authorization residue, and public narrative pressure.

## Repeated vocabulary QA

### Improved in Sprint 199
- Lantern repetition reduced in Chapters 1-8.
- Consent/permission wording diversified.
- Routing/path language reduced in several chapters.
- Abstract doctrine converted into scene objects: headline, article, porch camera, Voss photo, index, recorder, car, help desk ticket.

### Remaining watch terms for Act II
- Lantern
- sequence
- consent
- permission
- proof
- pattern
- precedent
- source
- system
- witness
- authorization

Use these terms only when they carry a specific narrative job.

## Audiobook readiness

### Act I status
Conditionally ready for proof-listening after local patches to Chapters 9-10.

### Best excerpt candidates
1. Chapter 1: headline arrival.
2. Chapter 5: Vanessa at the door.
3. Chapter 6: Celia name converted to role.
4. Chapter 8: Voss tape.
5. Chapter 10: help desk ticket / authorization ghost.

## Final Sprint 200-SB verdict
Act I is no longer a repeated-chapter draft. It now has a distinct escalation spine:

1. Public narrative attack.
2. Lena exposure.
3. Precedent threat.
4. Vanessa arrival.
5. Voss artifact.
6. Celia reveal.
7. Surveillance pressure.
8. Voss doctrine.
9. NorthStar template.
10. First confirmed Null contact.

## Next recommended sprint
Sprint 201-SB: Book 2 Act II Build Order and Draft Repair

Goals:
- Define Act II chapter map.
- Continue from the authorization ghost.
- Expand NorthStar, Celia Vale, Vanessa, and The Null Pattern without overusing doctrine terms.
- Preserve Maggie as ethical brake.
- Make every chapter scene-forward and audiobook-readable.
