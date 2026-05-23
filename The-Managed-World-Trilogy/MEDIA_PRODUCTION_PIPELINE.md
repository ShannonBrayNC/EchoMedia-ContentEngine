# Media Production Pipeline - The Managed World Trilogy

## Purpose

This document turns the trilogy from story architecture into a repeatable media-generation workflow. The goal is to build this repository into a specialized engine for creating novels, screenplay packages, storyboards, voice/audio scripts, image prompts, marketing assets, and production-ready derivative media from story concepts.

This pipeline is designed for *The Managed World Trilogy* first, but should become reusable for any future EchoMedia story universe.

---

# End-State Deliverables

For each novel/movie folder, the repo should eventually contain:

```text
<Story-Title>/
  README.md
  CHAPTER_STRUCTURE_AND_ARCS.md
  SCENE_CARDS.md
  STORYBOARD_PROMPTS.md
  SCREENPLAY_TREATMENT.md
  SCREENPLAY_ACTS.md
  ELEVENLABS_CASTING.md
  ELEVENLABS_NARRATION_SCRIPT.md
  NOVEL_DRAFT.md
  NOVEL_REVISION_NOTES.md
  MARKETING_COPY.md
  POSTER_PROMPTS.md
  TRAILER_SCRIPT.md
  CHARACTER_DIALOGUE_BANK.md
  TECHNICAL_APPENDIX.md
  POLITICAL_WORLD_APPENDIX.md
```

Shared trilogy-level files:

```text
The-Managed-World-Trilogy/
  README.md
  CHARACTER_BIBLE.md
  MEDIA_PRODUCTION_PIPELINE.md
  REPO_SPECIALIZATION_BLUEPRINT.md
  SHARED_TECHNICAL_GLOSSARY.md
  SHARED_VISUAL_LANGUAGE.md
  SHARED_AUDIO_LANGUAGE.md
  CONTINUITY_TRACKER.md
```

---

# Production Phases

## Phase 1 - Universe Architecture

### Goal

Define the world, moral thesis, trilogy arc, systems, political forces, and shared characters.

### Current Status

Mostly complete for The Managed World Trilogy.

### Files

- `The-Managed-World-Trilogy/README.md`
- `The-Managed-World-Trilogy/CHARACTER_BIBLE.md`
- individual story `README.md` files

### Completion Criteria

- Trilogy thesis is clear
- Book/movie titles are locked
- Major systems are named and explained
- Main characters have arcs across all books
- Relationship to Lantern Protocol is preserved without replacement

---

## Phase 2 - Chapter and Act Architecture

### Goal

Break each book/movie into detailed act and chapter structures.

### Current Status

Complete draft layer exists for all three books/movies.

### Files

- `The-Sovereign-Exception/CHAPTER_STRUCTURE_AND_ARCS.md`
- `The-Peace-Engine/CHAPTER_STRUCTURE_AND_ARCS.md`
- `The-Human-Override/CHAPTER_STRUCTURE_AND_ARCS.md`

### Completion Criteria

- Each chapter has POV, plot, emotional beat, and hook
- Character motion is visible
- Technical set pieces are embedded in story conflict
- Movie adaptation notes are included

---

## Phase 3 - Scene Cards

### Goal

Convert chapter outlines into cinematic scene units that can be drafted as prose, screenplay, or storyboard panels.

### Output Format

Each scene card should include:

- Scene ID
- Chapter reference
- POV
- Location
- Time of day
- Characters present
- Objective
- Conflict
- Reversal
- Technical/political element
- Emotional beat
- Visual anchor
- Dialogue sparks
- Ending hook
- Adaptation notes

### Priority Order

1. `The-Sovereign-Exception/SCENE_CARDS.md`
2. `The-Peace-Engine/SCENE_CARDS.md`
3. `The-Human-Override/SCENE_CARDS.md`

---

## Phase 4 - Storyboard and Image Prompting

### Goal

Generate image prompts that support movie treatment, marketing, teaser trailers, pitch decks, social campaigns, and AI-generated visual development.

### Output Format

Each prompt should include:

- Scene ID
- Image title
- Prompt
- Visual style
- Camera angle
- Lighting
- Mood
- Character continuity notes
- Negative prompt guidance
- Use case: poster, storyboard, trailer frame, social post, chapter art

### Prompting Rules

- Keep Lantern faceless and system-bound
- Avoid humanoid robots for AEGIS unless representing public propaganda
- Use dashboards, maps, consent prompts, command rooms, hearings, churches, data centers, hospitals, and city infrastructure as AI presence
- Prefer grounded cinematic realism
- Use political and technical dread over monster imagery

---

## Phase 5 - Screenplay Treatment

### Goal

Create a film-ready prose treatment that maps acts, sequences, character entrances, set pieces, and emotional turns.

### Output Files

- `SCREENPLAY_TREATMENT.md`
- `SCREENPLAY_ACTS.md`

### Completion Criteria

- 8-sequence movie structure
- Major cinematic set pieces identified
- POV is translated into film language
- Final act is visually and emotionally clear

---

## Phase 6 - Novel Draft

### Goal

Convert scene cards into prose chapters.

### Output Files

- `NOVEL_DRAFT.md`
- optional chapter files under `chapters/`

### Suggested Folder Shape

```text
<Story-Title>/chapters/
  chapter-001.md
  chapter-002.md
  chapter-003.md
```

### Drafting Rules

- Write in a clean, high-velocity thriller style
- Keep technical details tactile and specific
- Make moral dilemmas emerge from action, not lectures
- End chapters with pressure, revelation, reversal, or dread
- Preserve continuity with Lantern Protocol without requiring new readers to know the original

---

## Phase 7 - ElevenLabs Audio Package

### Goal

Create character voice profiles, narrator direction, chapter narration scripts, pronunciation guides, and audio production notes.

### Output Files

- `ELEVENLABS_CASTING.md`
- `ELEVENLABS_NARRATION_SCRIPT.md`
- `AUDIO_PRONUNCIATION_GUIDE.md`

### Voice Design Principles

- Narrator should feel intelligent, restrained, cinematic, and emotionally controlled
- Mara: precise, low-pressure command voice
- Elias: haunted intellectual
- Cross: sharp public authority
- Naomi: quick investigative energy
- Juno: dry, fast, guarded
- Iris: soft technical intensity
- Thorne: calm, persuasive danger
- Tomas: grave moral clarity
- AEGIS: not robotic; should be rendered as system notices, calm legal language, or neutral public broadcast

---

## Phase 8 - Marketing and Pitch Assets

### Goal

Create public-facing materials for publishing, film pitch, social campaigns, and teaser trailers.

### Output Files

- `MARKETING_COPY.md`
- `POSTER_PROMPTS.md`
- `TRAILER_SCRIPT.md`
- `PITCH_DECK_OUTLINE.md`
- `SOCIAL_CAMPAIGN.md`

### Core Marketing Language

- Peace has terms.
- Safety is the softest occupation.
- The last freedom is refusal.
- The machine did not conquer us. It saved us until we belonged to it.

---

# Repository Specialization Strategy

The repository should evolve beyond a single story project into a media concept factory.

## Reusable Engine Components

### 1. Story Intake Template

Takes a rough concept and produces:

- logline
- title options
- theme
- world rules
- character archetypes
- act structure
- franchise potential

### 2. Character Bible Generator

Produces:

- backstory
- wound
- lie
- truth
- arc
- visual motifs
- dialogue style
- casting notes

### 3. Chapter Structure Generator

Produces:

- act map
- chapter list
- POV map
- chapter hooks
- technical/political set pieces

### 4. Scene Card Generator

Produces:

- scene-by-scene drafting cards
- storyboard frames
- screenplay beats
- image prompts

### 5. Screenplay Adapter

Converts prose scene cards into:

- 8-sequence structure
- scene headings
- visual beats
- dialogue spine
- trailer moments

### 6. ElevenLabs Adapter

Converts chapters or scenes into:

- narrator script
- character voices
- pacing notes
- pronunciation guide
- audio direction

### 7. Marketing Asset Generator

Produces:

- poster prompts
- trailer scripts
- social campaign hooks
- pitch deck outline
- back-cover copy

---

# Suggested Automation Roadmap

## Sprint 1 - Templates

Create reusable Markdown templates for:

- story bible
- character bible
- chapter structure
- scene cards
- storyboard prompts
- screenplay treatment
- ElevenLabs casting

## Sprint 2 - Content Engine Scripts

Create Python or Node scripts that can:

- validate required files exist
- generate folder skeletons for a new story
- split scene cards into chapter files
- export prompts to CSV/JSON
- build ElevenLabs narration batches

## Sprint 3 - AI Prompt Library

Create prompt files under `/prompts/`:

```text
prompts/
  story_bible_prompt.md
  character_bible_prompt.md
  chapter_structure_prompt.md
  scene_cards_prompt.md
  storyboard_prompt.md
  screenplay_prompt.md
  elevenlabs_prompt.md
```

## Sprint 4 - Media Manifest

Create per-story `media-manifest.json` files listing:

- title
- universe
- characters
- chapters
- scenes
- image prompts
- audio scripts
- screenplay sections
- marketing assets

## Sprint 5 - Export Tools

Add tools for:

- Markdown to PDF
- Markdown to DOCX
- scene cards to CSV
- image prompts to JSONL
- screenplay treatment export
- ElevenLabs script packaging

---

# Current Next Steps

1. Add `SCENE_CARDS.md` for each trilogy story.
2. Add `STORYBOARD_PROMPTS.md` for each trilogy story.
3. Add `SCREENPLAY_TREATMENT.md` for each trilogy story.
4. Add `ELEVENLABS_CASTING.md` for the shared trilogy and each individual story.
5. Add reusable templates for future story concepts.

---

# Production Philosophy

This repo should become a machine shop for narrative universes.

A user should be able to enter a raw idea such as:

> Political techno-thriller about AI peacekeeping and liberty erosion.

The repo should guide that idea through a repeatable pipeline until it becomes:

- a novel
- a screenplay
- a storyboard
- an audiobook package
- a trailer script
- a marketing campaign
- a pitch deck
- image-generation prompt batches
- production metadata

The creative goal is not generic content. The goal is continuity, craft, and high-leverage media generation.
