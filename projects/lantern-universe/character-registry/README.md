# Lantern Universe Character Registry

**Sprint:** PUB-007  
**Status:** Active registry  
**Owner:** Lantern Publishing / EchoMedia Content Engine

## Purpose
The Character Registry is the canonical home for Lantern Universe character truth. It prevents character drift across Silver Bullet, The Voss Files, Lantern Protocol Case Files, scripts, marketing, audiobook packages, and visual packages.

## Registry Scope
The registry tracks:

- stable character identifiers
- names and aliases
- series relationships
- canon status
- first appearance
- role and function
- motivations
- fears
- relationships
- trauma continuity
- current state
- review requirements

## Canon Rule
A character profile in this registry overrides ad hoc notes in individual manuscripts or chapter drafts unless a later Producer Review-approved update changes the profile.

## Required Character Profile Fields
Each character profile should include:

- `character_id`
- `display_name`
- `canon_status`
- `primary_series`
- `first_appearance`
- `role`
- `function`
- `motivations`
- `fears`
- `relationships`
- `continuity_notes`
- `producer_review_required`

## Character Status Values
Recommended status values:

- `canon-locked`
- `canon-draft`
- `concept-locked`
- `needs-review`
- `retired`
- `conflict`

## Update Process
1. Propose a character change.
2. Check affected books, series, and timelines.
3. Update the profile only if the change does not violate canon.
4. Route major changes through Producer Review.
5. Record continuity impact in timeline registry when available.

## Initial Profiles

- `jack-mercer.yaml`
- `elias-voss.yaml`
- `evelyn-blackwood.yaml`

## Follow-Up Work
Future sprints should add full relationship maps, visual bible references, voice/narration notes, and timeline-linked status tracking.
