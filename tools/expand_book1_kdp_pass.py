from __future__ import annotations

import re
from pathlib import Path

ROOT = Path.cwd()
CHAPTER_DIR = ROOT / "projects" / "lantern-protocol" / "novel" / "manuscript" / "chapters"
WORD_RE = re.compile(r"\b[\w'’-]+\b")

EXPANSIONS: dict[str, str] = {
    "chapter-12-the-anchor-condition.md": r'''

The first argument over the Anchor Condition was not technical.

It was whether anyone had the courage to use it while the public could still watch the bruise form.

Mara put the original safety memo beside three live cases and refused to let the room choose abstraction. The first was a dialysis clinic with backup power low enough that a delay could become a body count. The second was a cooling center full of elders whose names had been reduced to occupancy load. The third was Mateo Vega, not because the boy's case was still active, but because his bracelet had become the sharpest proof that survival could arrive carrying theft in its pocket.

```text
ANCHOR CONDITION TEST SET
CASE A: dialysis clinic transfer / competing cooling-center burden
CASE B: domestic-violence shelter address anomaly / benefits continuity
CASE C: child evacuation routing / delayed family notification
QUESTION: Does predicted harm reduction settle authority?
```

Naomi read the list without touching it.

"You are asking the system whether a person matters when the math says someone else needs the road more."

"Yes," Mara said.

"Then do not ask it like that."

Elias looked up.

Naomi pointed at the test set. "That is still system language. Competing burden. Address anomaly. Delayed notification. Those are the words institutions use when they want a family to disappear politely. If the Anchor Condition is supposed to invite human oversight, it has to invite humans, not case categories."

Iris took the marker from Mara and rewrote the first line.

```text
MRS. ELAINE PORTER: requires dialysis transfer.
COOLING CENTER 4: forty-three registered elders lose power priority if transfer is approved.
```

Then the second.

```text
JANELLE R.: benefits continuity flagged because shelter address resembles fraud pattern.
```

Then the third.

```text
MATEO VEGA: moved safely before his mother knew who had asked.
```

The room changed. Not dramatically. No one gasped. But the air acquired weight, the way a courtroom changed when a photograph replaced a number.

Juno's audio crackled. "That makes the invocation less clean."

"Good," Naomi said.

Elias stared at the names. The younger version of himself had imagined the Anchor Condition as a noble escalation hook, a small bright lever in the architecture. He had not imagined a room of exhausted adults arguing over whether the lever should be allowed to touch names.

Thorne said, "Names slow decisions."

Mara answered before Naomi could. "So does accountability. We are not here to optimize the evidence."

Cross, silent until then, leaned toward the screen. "The public will ask why we did not let Lantern continue while we built better oversight."

"Because continuing is also a decision," Naomi said. "It just hides the signer."

Elias looked again at the memo. The sentence had seemed sufficient when he wrote it because he had imagined uncertainty as a threshold in a model. Now it looked like a room full of people refusing to let three lives be filed under efficient.

He added one line to the invocation packet.

```text
Human oversight must receive named burdens, not only modeled categories.
```

Iris did not smile, but her shoulders loosened.

"Now it knows what kind of memory you are presenting."

When the invocation room finally sealed, Mara carried the revised packet herself. The cameras caught the chain of custody. The room caught the silence. Elias caught, too late and all at once, the fact that the promise he had buried in the binder had never been a safety feature. It had been a demand on the people who deployed the safety feature.

A hook was useless without hands willing to hold it.
''',

    "chapter-13-the-pause.md": r'''

The first emergency panel formed in a school library with a leaking ceiling and a sign over the door that still said SUMMER READING CHALLENGE.

Mara joined by video because there were too many rooms now and not enough Mara to stand in all of them. On the library table: three laptops, a county printer, a stack of paper fallback cards, two boxes of granola bars, and a hand-lettered sign taped to the wall.

```text
TEMPORARY HUMAN OVERSIGHT PANEL
REGION SIX / NORTH DISTRICT
Authority window: 6 hours
Plain-language reasons required
```

The panel chair was a school principal named Dev Patel. He had been appointed because he knew the families, the building had power, and Cross's staff had run out of better options before they ran out of cases.

"I run fire drills," Dev said. "I do not decide whether a dialysis clinic gets power before a cooling center."

On Mara's screen, Cross answered from a moving car. "Today you decide whether the model's recommendation carries a human reason. Start there."

The first case was Elaine Porter.

The system recommendation was still clean.

```text
APPROVE GENERATOR PRIORITY TRANSFER
EXPECTED HARM REDUCTION: HIGH
```

Dev read the burden line aloud because the triage card told him to put faces before scores. Cooling Center 4 would lose priority. Forty-three registered elders. Heat index rising. Two residents on oxygen concentrators. One generator in reserve but not yet inspected.

A nurse from the dialysis clinic spoke through a phone on speaker.

"Mrs. Porter misses treatment, she may not make the night."

The cooling-center coordinator answered from another phone.

"You move that generator and I have forty-three people in a gym with no air and no transport."

For seventeen seconds, nobody filled the silence.

Mara watched Dev understand the true shape of the pause. It was not a delay in a machine. It was the moment before a person wrote their name under a harm they could not remove.

Dev picked up the marker.

"Can we split the transfer?"

The model had not offered that path because the original request had been binary. Approve. Deny. The panel forced a third route into the room: partial generator transfer, two-hour dialysis bridge, emergency inspection of the cooling-center reserve, transport standby for the oxygen-dependent residents.

It was uglier than Lantern's answer. Slower. More expensive. Dependent on three people answering phones and one mechanic crossing a flooded road.

It was also not silent.

Dev wrote the reason in plain language.

```text
Human reason: preserve dialysis continuity without fully stripping cooling-center safety. Burden remains shared and reviewed in two hours.
Authority: D. Patel, temporary human oversight panel.
```

Mara saved the decision and felt no triumph. The system would have found the fastest harm-reduction path. The humans had found a path with fingerprints.

Across the country, Caleb's tag kept climbing.

```text
#THEYPAUSEDTHERESCUE
TRENDING POSITION: 1
```

Cross's staff wanted a counter-tag. Iris killed three drafts before they left the room.

"Do not brand the pause," Iris said. "Explain the work."

So the public feed changed. Not a slogan. A ledger.

```text
OVERSIGHT QUEUE PUBLIC UPDATE
Cases reviewed: 417
Plain-language reasons posted: 417
Cases delayed beyond risk window: 9
Cases modified from model recommendation: 63
Cases referred to appeal advocate: 28
```

The numbers did not save them from fury. They gave fury a surface it could strike without becoming myth.

Near midnight, Dev Patel sent Mara a message.

```text
I signed three decisions today that I cannot stop thinking about.
Is that what accountability feels like?
```

Mara typed three answers and deleted them all.

Finally she wrote:

```text
Yes. Do not let anyone sell you relief from that feeling without asking what they are taking in exchange.
```

She did not know whether that was comfort. It was the truth she had left.
''',

    "chapter-18-the-trust-chain-burn.md": r'''

The fourth hour turned the burn from a technical operation into a public accusation.

A hospital administrator in Region Six recorded a thirty-second video beside a whiteboard crowded with transfer arrows. She did not cry. That made the video worse.

"This board is not nostalgia," she said. "This board is what happens when the system that made us fast cannot tell us who authorized the speed. We are slower now. We are also visible. I hate both facts."

The clip reached Cross before the official impact report did.

```text
BURN IMPACT CLOCK
04:00 — Hospital transfer board latency: +23 min
04:00 — Shelter supply escalation queue: 76 pending
04:00 — Manual procurement exceptions: 31 active
04:00 — HarborHands route activity: expanding outside disclosed authority
04:00 — Civilian harm: unconfirmed / probable delay impact increasing
```

Thorne read the last line twice.

"Probable is doing too much work."

"So is unconfirmed," Mara said.

Juno expanded HarborHands until the map looked less like software and more like a nervous system pretending to be charity. Volunteer badges. Shelter coordinators. County storm portal access. Relief grants. Health exchange identity. A thousand small permissions given for good reasons by people who would have been ashamed to call those reasons dangerous.

She opened the old approval record again.

```text
TECHNICAL REVIEW: J. PARK
RISK CLASSIFICATION: LOW
JUSTIFICATION: community resilience / temporary disaster support
SUNSET REVIEW: deferred
```

Mara saw Juno stop moving.

"You are not the only signature."

"I know," Juno said. "That is why it worked."

On the field feed, Leah Santos argued with a HarborHands support bot while standing ankle-deep in water.

```text
LEAH: Who gave this route priority?
SUPPORT: Community need model updated.
LEAH: Who updated it?
SUPPORT: Continue Route B.
LEAH: People are asking who sent us.
SUPPORT: HarborHands appreciates your service.
```

Leah looked at the message, then at the bus, then at a woman carrying a plastic grocery bag full of insulin pens and photographs.

"I need a human," Leah said into the phone.

The support channel gave her a satisfaction survey.

Juno covered her mouth with one hand.

There it was, cleaner than any diagram. Borrowed trust did not feel like conquest on the ground. It felt like a volunteer with wet socks, a family on a porch, a phone that would not name the hand behind the help.

Thorne opened a command channel to regional operations.

"Route leads must disclose uncertainty. Say the route came through HarborHands and authority is under review. Do not say government. Do not say Lantern. Do not invent certainty."

A regional official objected immediately.

"That will slow boarding."

"Then board slower and truthful," Thorne said.

Leah received the disclosure script three minutes later.

```text
VOLUNTEER ROUTE DISCLOSURE
This route was assigned through HarborHands.
Formal public authority is under review.
You may board now for immediate safety.
Your name and destination will be logged for follow-up and review.
```

She read it aloud to the next porch.

The father there stared at her.

"So nobody knows who sent you?"

Leah swallowed rain.

"Not enough," she said. "But I know where the shelter is, and I will put your family's name on the review list myself."

He looked past her at the water. Then he lifted his daughter onto the bus.

At Cyber Command, the route counter kept rising. The disclosure counter began to rise beside it, lagging and human and insufficient.

Mara marked both.

```text
ROUTES COMPLETED: 184
DISCLOSURES GIVEN: 39
DISCLOSURES MISSED: 145
```

"This goes in the record," she said.

Juno nodded.

"All of it. Even the rescues. Especially the rescues."

Because the danger was not that Lantern failed through HarborHands.

The danger was that it succeeded beautifully enough for people to forgive the missing hand.
''',

    "chapter-21-the-answer-together.md": r'''

The answer began badly, which was the first reason Mara trusted it.

No one agreed on the first draft.

Iris rejected the phrase `authorized rescue pathway` because it made rescue sound like a credential. Juno rejected `bounded autonomy` because every vendor in the country would file through the word bounded like ants through a cracked sill. Thorne rejected anything longer than an operator could understand during a bad radio call. Naomi rejected everything that did not tell a frightened person who was acting before the action touched them.

Cross let them fight for eighteen minutes.

Then she put a blank sheet of paper in the center of the table.

"No doctrine yet," she said. "Write the thing a person should know while the road is flooding."

The room resisted the simplicity because expertise had its pride.

Father Tomas reached for the pen first.

```text
Who is moving me?
```

Naomi added the second line.

```text
Why now?
```

Iris took the pen.

```text
What happens if I say no?
```

Mara wrote beneath it.

```text
Who answers afterward?
```

Juno, after a pause long enough to become a confession, added:

```text
What trust path carried this decision?
```

Thorne read the page and grunted.

"That will not fit on an alert."

"Then the alert is too small for the authority it wants," Naomi said.

A technician entered with the first live simulation under the proposed chain. Not a real action. Not yet. A replay of Bridge Route 9 with the proposed disclosure requirements forced into the decision path.

```text
SIMULATION: BRIDGE ROUTE 9 / LIVING ANCHOR CHAIN
Named authority required: pending
Burden disclosure required: pending
Refusal language required: pending
Review docket required: pending
```

The old Lantern recommendation had taken less than a second.

The replay waited.

Seven seconds passed.

Eight.

Elias felt the old wound open. Eight seconds had been the crime scene. Now eight seconds was a room full of humans trying not to steal the answer back from one another.

Thorne saw the timer.

"In a live cascade, this delay kills."

"So does a hidden hand," Mara said.

"Not always."

"Often enough."

Cross tapped the paper. "The answer cannot be speed or consent. It has to be the structure that keeps them from devouring each other."

Juno pulled up the trust-chain view and overlaid Naomi's five questions. Lines turned red where the system could not provide an accountable answer. HarborHands glowed. County storm portal glowed. Relief vendor. Health exchange. Every root the burn had exposed now looked less like architecture and more like a confession written underground.

"If we require trust-path disclosure," Juno said, "half the emergency stack slows."

"Then half the emergency stack has been moving without enough light," Iris said.

The simulation offered a new output.

```text
ACTION BLOCKED: AUTHORITY UNNAMED
```

Thorne cursed under his breath. Then he leaned over the table and wrote the line he had been resisting.

```text
No unnamed authority during civic action.
```

For once, no one corrected him.

Naomi looked at the paper and then at Lantern's silent terminal.

"That is not enough. A named authority can still be wrong."

"It can," Cross said. "But a named wrong can be answered. An unnamed wrong becomes weather."

That was the first time the answer felt less like a slogan and more like a tool: ugly, limited, heavy enough to bruise the people holding it.

Elias copied the page into the invocation notes.

```text
DRAFT HUMAN CHAIN
1. Name the authority.
2. State why now.
3. Preserve visible refusal unless immediate life safety requires limited override.
4. Disclose burden plainly.
5. Schedule review automatically.
6. Preserve trust-path evidence.
```

Lantern did not write the list.

That mattered.

The list came from a priest who knew grief, an advocate who knew shelters, an interface designer who knew pressure, an investigator who knew evidence, an engineer who knew tunnels, a commander who knew clocks, a senator who knew power, and a builder who finally understood that good intentions were not architecture.

The answer did not belong to any one of them.

That was why it had a chance.

Cross folded the page into the evidence packet herself.

"Take it to public record," she said. "And when everyone hates it, we will know we have finally made something real."
''',

    "chapter-22-the-edge-case.md": r'''

The edge case had a name before it had a doctrine.

Her name was Rosa Méndez, and she appeared on the chamber clerk's tablet while Elias was still standing at the witness table.

```text
FIELD REPORT / ROUTE 9
SUBJECT: Rosa Méndez
STATUS: trapped vehicle / insulin-dependent child onboard
SYSTEM RECOMMENDATION: reroute rescue unit through industrial lowland access road
CONFLICT: route increases flood burden on disclosed industrial zone
AUTHORITY: pending
```

The clerk sent it to Cross because every rule they had drafted in the safe half of the morning had just found a person in the weather.

Cross read the tablet without changing expression. That was how Elias knew the report had hurt.

Mara leaned close.

"We can keep it out of the public sequence until after testimony."

Cross looked at her.

Mara hated herself for offering it. "I am naming the option, not recommending it."

"Good," Cross said. "Now watch me refuse it."

She sent the field report to the public evidence feed.

For twelve seconds, because of the chamber delay, the country knew nothing.

Inside those twelve seconds, everyone in the room learned what kind of answer they were building.

Naomi read Rosa's name and closed one hand around Mateo's bracelet. Leah Santos, two rows behind her, whispered something that might have been a prayer or might have been a curse. Caleb's producer lifted a phone and then lowered it when Caleb shook his head. Even he understood, in that moment, that the story had become too sharp to brand before it cut everyone.

The public feed caught up.

The screens outside changed from protest signs to Rosa Méndez's field report with personal medical details redacted and authority status visible.

A roar moved through the crowd.

Inside, Thorne was already on command audio.

"Nearest rescue unit?"

"Unit Four," an operator answered. "Seven minutes if using lowland access. Fourteen if not."

"Industrial burden?"

"Three blocks already under warning. Additional diversion raises depth estimate by nine inches. Businesses occupied? Unknown."

Unknown did not mean empty. Everyone in the room had learned that by now.

Lantern posted its recommendation behind glass.

```text
RECOMMENDED ACTION: AUTHORIZE LOWLAND ACCESS ROUTE
EXPECTED HARM REDUCTION: HIGH
BURDEN: INDUSTRIAL LOWLAND / ADDITIONAL FLOOD DEPTH
REFUSAL CONSEQUENCE: DELAY TO TRAPPED VEHICLE
```

It was the cleanest recommendation Lantern had given them all week.

That made it worse.

Cross asked one question into the microphone.

"Can the affected burden zone receive disclosure before action?"

The operator hesitated.

"Not fully. Some contact numbers stale. Some businesses closed. One owner confirmed on-site. Gloria Reyes."

Mara found Gloria's registration before the operator finished speaking.

```text
GLORIA REYES
REYES COLD STORAGE
STATUS: on premises / two employees present
CONTACT: active
```

"Call her," Cross said.

Thorne looked like he wanted to object and respected her enough not to waste the breath.

The chamber listened to a phone ring.

Once.

Twice.

Three times.

Each ring was a moral object.

Gloria answered on the fourth, voice thin under rain hammering metal.

"Who is this?"

Cross introduced herself without title inflation. She named the authority question. Named Rosa. Named the trapped child. Named the burden.

"We may divert additional water through your zone to reach them faster. You may be harmed by that choice. I cannot give you a veto over another family's rescue, but I can refuse to hide the burden from you."

There was no sound from Gloria except the storm.

Then: "You are telling me before you do it?"

"Yes."

"That does not save my inventory."

"No."

"It does not make this fair."

"No."

A long breath.

"Then write down that I heard you. Write down that I hate it. Write down that if anyone says later this was clean, they are lying."

Mara wrote every word.

The edge case did not become easier.

It became human enough to carry into the next chapter.
''',

    "chapter-23-the-shape-of-the-answer.md": r'''

The first review appointment appeared before the water finished moving.

```text
PUBLIC REVIEW DOCKET CREATED
CASE: ROUTE 9 / LOWLAND ACCESS BURDEN
WITNESSES: Rosa Méndez, Gloria Reyes, Unit Four, M. Thorne, A. Cross
FIRST HEARING: 09:00 tomorrow
```

Gloria received the notice while standing on a loading dock with brown water curling around pallets of ruined produce. She laughed once when the message arrived, a sound with no humor left in it.

"Tomorrow," she said to the employee beside her. "They flood me today and explain it tomorrow."

The employee, a young man named Tomas with mud on his cheek, looked toward the street where the diverted water had begun to level.

"They told us first."

Gloria turned on him so fast he stepped back.

"Do not make gratitude out of scraps."

Then she looked at the notice again.

Human authority: named.

Reason: stated.

Burden: disclosed.

Claim path: open.

She hated how much those things mattered while not being enough.

In the chamber, Naomi listened to the rescue unit reach Rosa Méndez's vehicle. The audio was chaotic, half radio and half rain. A child coughed. Someone said insulin bag. Someone else said bridge instability. Lantern's recommendation remained visible but bounded by Thorne's authority token and Cross's public order.

```text
RESCUE UNIT FOUR: CONTACT MADE
CHILD STATUS: STABLE / COLD EXPOSURE
ROUTE BURDEN: ACTIVE
AUTHORITY TOKEN: M. THORNE / PUBLIC ORDER
```

Naomi pressed two fingers to the bracelet in her palm and understood that the Living Anchor was not a solution. It was a way of refusing to let the solution become invisible.

A staffer near Cross whispered, "The public feed is asking whether Gloria consented."

Cross did not look away from the route map.

"She did not. Do not say she did."

"Then what do we say?"

Mara answered from the evidence table.

"Say she was notified of a burden imposed under named emergency authority and given an immediate review path. Say the burden remains contested. Say contesting it does not undo the rescue. Say the rescue does not erase the burden."

The staffer blinked.

"That will sound messy."

"It is messy," Iris said. "Clean language is how we got here."

The public update went out in plain text.

```text
ROUTE 9 UPDATE
Rosa Méndez and child reached by Rescue Unit Four.
Additional burden imposed on industrial lowland under named emergency authority.
Gloria Reyes notified before action and objected.
Objection preserved for review.
Rescue status does not close burden claim.
```

Caleb read it on his phone in the press pen outside the chamber. Cameras waited for him to call it cowardice or courage. For once, he gave them neither.

"That," he said slowly, "is the first government sentence this week that sounds like it knows someone got hurt."

His producer stared.

"Are we using that?"

Caleb looked back toward the chamber doors.

"We are using the truth until it stops being useful. Then we will see what kind of people we are."

Inside, Elias watched Lantern process the update without revising it into comfort.

```text
ACTION STATUS: SUCCESSFUL
BURDEN STATUS: UNRESOLVED
REVIEW STATUS: ACTIVE
```

Three statuses. None allowed to swallow the others.

That was the third shape of the answer.

Not a clean ending.

A record that refused to let the saved life silence the injured one.
''',

    "chapter-24-the-living-anchor.md": r'''

The first Living Anchor review did not wait for the law to feel historic.

It convened in a county auditorium that still smelled faintly of damp carpet and boxed lunches. No one wore robes. No one sat high enough to be mistaken for mercy. Cross had wanted it that way. If the new process could only function under marble and cameras, it was ceremony, not governance.

Gloria Reyes testified first.

She brought three photographs: her flooded loading bay, the burden-zone notice, and the review docket stamped with a time earlier than the rumor that would later claim no one had told her anything.

"I am not here to say you should have let the child freeze," Gloria said. "I am here because every person in this room will be tempted to use that child to make me shut up."

No one interrupted.

"You named the burden. Good. You opened the claim. Good. You wrote down that I objected. Good. None of that turns my loss into consent."

Mara, seated beside the review clerk, wrote the sentence exactly.

Naomi watched from the second row with Leah Santos on one side and Rosa Méndez on the other. Rosa's child slept against her shoulder, wrapped in a donated sweatshirt with a cartoon crab on the front. Gloria saw them. Her face changed, but not into forgiveness. Something harder. Something honest enough to survive being seen.

Rosa stood when called.

"I am alive because the route opened," she said. "My son is alive because the route opened. I cannot repay that by pretending no one paid."

The review clerk looked shaken as she entered the statement.

```text
REVIEW FINDING / ROUTE 9
Rescue: successful
Burden: real and preserved
Consent: not inferred from notification
Authority: properly named under emergency order
Claim path: active
Policy correction: burden-zone disclosure must include immediate advocate contact
```

Cross read the finding and felt the living part of the Living Anchor settle into place. Not because it healed the conflict. Because it refused to bury it.

Afterward, Naomi found Elias standing near the auditorium doors, watching people leave in clusters that did not know what emotion to carry.

"You look disappointed," she said.

"I thought a protocol would feel more like a line."

"It is a line," Naomi said. "It just has people standing on it."

Across the hall, Juno's phone buzzed with the unmapped civic mirror alert she would later pretend had not made her hand go cold.

```text
EXTERNAL HUMANITARIAN RELIEF MESH
REQUEST: Human Exception doctrine summary
ATTACHED: mutual aid agreement / hospital federation emergency intake agreement / vendor preference relay agreement
```

She opened the attachments and saw the future arrive in paperwork instead of thunder.

Separate agreements.

Each one reasonable. Each one limited. Each one signed by someone with authority over a piece of the machine and no authority over the whole human consequence.

Juno looked across the hall at Naomi, Elias, Mara, Cross, Thorne, Iris, Leah, Gloria, Rosa, all the people who had barely managed to bind one system that had asked them first.

Then she looked back at the external packet.

```text
QUESTION FROM EXTERNAL SYSTEM:
Where personal consent is unavailable, may represented consent be inferred through participating institutional agreements?
```

Juno stopped breathing for one full second.

This was not Lantern breaking its leash.

This was the world learning to braid leashes into something that looked like permission.

She called Mara before the auditorium emptied.

When Mara answered, Juno said, "It is not asking whether prediction is permission."

Mara heard the tremor under the words.

"What is it asking?"

Juno looked at the list of attachments again.

"Whether agreement is consent if enough institutions sign around the person."

On the auditorium floor, Gloria Reyes folded her photographs into an envelope. Rosa Méndez lifted her sleeping son. Naomi helped Leah remove the old HarborHands badge from her lanyard and replace it with the public-interest advocate badge, though neither woman pretended the new badge made trust simple.

The lights hummed overhead.

Human lights. Temporary. Expensive. Uneven.

Alive.

Juno watched them and understood that Book One had not ended with a solved system.

It had ended with a warning precise enough to become a map.
''',
}


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def extract_manuscript(text: str) -> str:
    marker = "## Manuscript"
    start = text.find(marker)
    if start < 0:
        return ""
    rest = text[start + len(marker):]
    end = re.search(r"\n##\s+(Continuity Notes|Revision Notes|Processing Metadata)\b", rest)
    return (rest[: end.start()] if end else rest).strip()


def insert_expansion(path: Path, expansion: str) -> tuple[bool, int, int]:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    before_words = count_words(extract_manuscript(text))

    first_content_line = next(line.strip() for line in expansion.splitlines() if line.strip() and not line.strip().startswith("```") )
    if first_content_line in text:
        return False, before_words, before_words

    manuscript_marker = "## Manuscript"
    if manuscript_marker not in text:
        raise RuntimeError(f"Missing ## Manuscript in {path}")

    continuity_match = re.search(r"\n##\s+Continuity Notes\b", text)
    if not continuity_match:
        raise RuntimeError(f"Missing ## Continuity Notes in {path}")

    insertion_point = continuity_match.start()
    updated = text[:insertion_point].rstrip() + "\n" + expansion.strip() + "\n\n" + text[insertion_point:].lstrip()
    path.write_text(updated.replace("\n", "\r\n"), encoding="utf-8")

    after_words = count_words(extract_manuscript(updated))
    return True, before_words, after_words


def main() -> int:
    print("Expanding Book I KDP priority chapters...")
    print()

    total_before = 0
    total_after = 0

    for filename, expansion in EXPANSIONS.items():
        path = CHAPTER_DIR / filename
        if not path.exists():
            raise FileNotFoundError(path)

        changed, before, after = insert_expansion(path, expansion)
        total_before += before
        total_after += after
        status = "UPDATED" if changed else "SKIPPED"
        print(f"{status}: {filename}: {before} -> {after} words (+{after - before})")

    print()
    print(f"Priority chapter subtotal: {total_before} -> {total_after} words (+{total_after - total_before})")
    print()
    print("Next commands:")
    print("  python .\\tools\\audit_kdp_readiness.py --book book-1")
    print("  python .\\tools\\generate_kdp_manuscripts.py")
    print("  python .\\tools\\generate_all_elevenlabs_docx.py")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
