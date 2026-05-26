# ElevenLabs Capability Matrix for EchoMedia Content Engine

Status: Sprint deliverable for Issue #40  
Scope: Documentation and configuration planning only. No runtime integration is implemented here.

## Purpose

The Content Engine should treat ElevenLabs as a full audio, voice, dialogue, localization, and agent platform rather than a single text-to-speech endpoint. This matrix maps Content Engine artifact types to ElevenLabs capabilities so future implementation work can be split into small, provider-aware issues.

ElevenLabs publishes AI-agent-friendly documentation indexes at:

- https://elevenlabs.io/docs/llms.txt
- https://elevenlabs.io/docs/llms-full.txt

The index confirms documentation coverage for text to speech, speech to text, music, text to dialogue, image/video, voice changer, voice isolator, dubbing, sound effects, voices, voice remixing, forced alignment, Speech Engine, ElevenCreative products, Audio Native, Voiceover Studio, ElevenAgents, agent voice customization, multi-voice support, pronunciation dictionaries, expressive mode, language support, knowledge base, tools, integrations, telephony, WhatsApp, and operations.

## Capability Phases

| Phase | Meaning | Implementation posture |
|---|---|---|
| MVP | Needed to make Content Engine audio-aware and usable for generated production packages | Define schema, export specs, and one provider adapter at a time |
| Phase 2 | Needed for richer story production and creator workflows | Add advanced audio, dialogue, alignment, and publishing workflows |
| Later | Valuable but not required for first production-ready movie/audio packages | Add telephony, advanced automation, marketplace, and managed-production integrations |

## Content Engine Artifact Types

| Artifact type | Description |
|---|---|
| Project registry | The canonical project/book/story-world metadata layer |
| Character sheet | Voice identity, role, performance range, accent, emotional tone, consent/licensing state |
| Manuscript chapter | Long-form source prose for audiobook or narration generation |
| Screenplay scene | Dialogue-heavy source artifact for staged voice/dialogue generation |
| Scene card | Scene summary, characters, mood, camera/audio notes, continuity references |
| Storyboard panel | Visual beat that may need narration, SFX, caption, timing, or lipsync metadata |
| Movie-generation package | Tool-ready bundle for AI video systems, including audio guidance |
| Voice package | Provider-neutral reusable voice definition for narrator, character, or agent |
| Agent profile | Realtime chat agent configuration with voice, tools, knowledge, and behavior |
| Localization package | Dubbing/translation outputs and target-language variants |
| Publishing package | Embeds, web/audio player configuration, show notes, accessibility artifacts |

## Capability Matrix

| ElevenLabs capability | Content Engine use | Target artifacts | Phase | Expected inputs | Expected outputs | Notes / open questions |
|---|---|---|---|---|---|---|
| Text to Speech | Generate narration, character reads, chapter previews, and scene scratch audio | Manuscript chapter, scene card, screenplay scene, movie-generation package, voice package | MVP | Text, voice ID, model ID, voice settings, output format, optional pronunciation rules | Audio file, generation metadata, optional timing data | First audio adapter should support short scene narration before long-form generation |
| Text-to-Speech WebSocket streaming | Stream partial LLM output into spoken audio for chat agents or interactive previews | Agent profile, generation workspace, scene preview | Phase 2 | Voice ID, streamed text chunks, session token, model ID, output format, latency settings | Audio chunks, final event, alignment metadata when enabled | Use when text arrives incrementally or alignment is needed; standard HTTP TTS remains simpler for full text |
| Speech Engine | Add voice to Content Engine chat agents and assistant-style project guides | Agent profile, generation workspace | Phase 2 | Agent response stream, selected voice package, user/session context | Realtime spoken response, transcript alignment, interruption state | Should be designed after the generation job/state model exists |
| ElevenAgents | Provider-hosted conversational agents for project guidance, character agents, or support flows | Agent profile, project registry, knowledge base package | Later | Agent instructions, voice config, knowledge base, tools, guardrails, dynamic variables | Hosted agent, embed/widget, conversation logs | Decide whether Content Engine owns the agent loop or delegates to ElevenAgents |
| Text to Dialogue | Generate multi-character performed dialogue from screenplay scenes | Screenplay scene, character sheet, voice package | MVP | Speaker-separated dialogue, assigned voices, pacing/emotion notes | Multi-voice dialogue audio, speaker metadata | Critical for pre-movie scene packages and table-read generation |
| Multi-voice support | Allow agents and scenes to switch voices for multi-character workflows | Agent profile, screenplay scene, dialogue package | Phase 2 | Speaker map, voice map, turn-taking rules | Multi-speaker audio or realtime agent voice switching | Must align with the canonical voice package schema |
| Voices / Voice Library | Select reusable voices for narrators, characters, and demo agents | Character sheet, voice package, project registry | MVP | Voice search criteria, provider voice ID, licensing metadata | Voice profile reference | Store provider voice ID separately from canonical character voice identity |
| Voice cloning | Create approved custom voices for narrators, characters, or creator-branded agents | Voice package, character sheet, agent profile | Later | Consent/licensing record, clean voice samples, voice naming/versioning | Provider voice ID, cloning metadata, consent trail | Must require explicit consent and licensing metadata before activation |
| Voice design | Create synthetic concept voices from text descriptions | Character sheet, voice package | Phase 2 | Character voice description, accent, age range, tone, style | Candidate voice references | Useful before cloning or final casting |
| Voice remixing | Iterate on voice attributes like accent, gender, pacing, quality, or style | Voice package, character sheet | Later | Source voice, transformation instructions | Variant voice references | Needs versioning to avoid accidental drift from approved character canon |
| Voice changer | Transform existing actor/audio takes into target voices while preserving delivery | Voice package, screenplay scene, production package | Later | Source audio, target voice, quality settings | Converted audio | Potential bridge for human scratch performances |
| Speech to Text / Transcription | Convert uploaded audio/video into text for editing, reuse, and accessibility | Publishing package, source media, review package | Phase 2 | Audio/video file, language hints | Transcript, speaker/timing metadata where available | Supports review loops and reverse-engineering source takes |
| Forced Alignment | Align text to spoken audio for subtitles, captions, lipsync, and shot timing | Storyboard panel, movie-generation package, publishing package | MVP | Final script text plus generated/recorded audio | Time-aligned transcript | Core requirement for AI video handoff and subtitle exports |
| Alignment from WebSocket TTS | Capture character or word timing while generating realtime or chunked audio | Agent profile, scene preview, subtitle package | Phase 2 | Streamed TTS request with alignment enabled | Character timing arrays, normalized alignment | Useful for realtime UI and generated caption previews |
| Dubbing | Translate and localize audio/video while preserving speaker timing and tone | Localization package, publishing package, movie-generation package | Phase 2 | Source audio/video, source language, target languages, speaker handling | Dubbed audio/video, translated script, timing metadata | Needed for multilingual release packages |
| Dubbing Studio | Manual/fine-grained review and correction of dubs | Localization package | Later | Draft dub, transcript, target-language edits | Human-reviewed dub package | May remain an external review workflow rather than engine-owned implementation |
| Sound effects | Generate scene SFX from text prompts | Storyboard panel, scene card, movie-generation package | Phase 2 | SFX prompt, duration, style, intensity, scene timing | SFX audio file, metadata | Add as optional scene audio layer beside dialogue and narration |
| Music | Generate music beds, themes, stingers, and trailer cues | Scene card, storyboard panel, pitch package, publishing package | Later | Music prompt, mood, duration, genre, instrumentation | Music audio file, license metadata | Useful for trailers and pitch materials, not first MVP |
| Voice isolator | Clean voice recordings before transcription, cloning, or voice conversion | Source media, voice package | Later | Audio file with noise/music/ambience | Isolated speech file | Helpful for creator-uploaded samples and rough takes |
| Audio Native | Embed audio playback into web pages or content previews | Publishing package, marketing site, preview UI | Phase 2 | Published audio, embed configuration, page metadata | Web audio embed/player | Useful for EchoMedia demos and audiobook landing pages |
| Voiceover Studio / Audiobooks | Long-form audiobook production workflow | Manuscript chapter, book project, publishing package | MVP | Chapter text, narrator voice, pronunciation dictionary, chapter metadata | Chapter audio, audiobook sequence metadata | Must be treated separately from short scene preview generation |
| Pronunciation dictionaries | Control names, invented terms, acronyms, and world-specific language | Voice package, project registry, manuscript, screenplay | MVP | Canon terms, pronunciation spellings, language context | Provider dictionary reference or export payload | Critical for Lantern Protocol and other story-world consistency |
| Agent expressive mode / voice customization | Give agents emotional delivery, pacing, and context-aware speech | Agent profile, character agent, generation workspace | Phase 2 | Agent persona, voice package, speed/emotion settings | Voice-agent behavior config | Should use canonical voice package values as source of truth |
| Agent tools / server tools / client tools | Let voice agents trigger Content Engine actions | Agent profile, generation workspace | Later | Tool definitions, permissions, target operations | Tool-enabled voice workflow | Must wait until validation/generation/export/save actions are cleanly separated |
| Knowledge base / RAG | Give voice agents access to project canon and documentation | Agent profile, project registry, canon package | Later | Canon docs, project docs, generated package metadata | Searchable agent knowledge | Connect only after project registry and traceability are stable |
| Telephony / Twilio / SIP / WhatsApp | Expose agents over phone or messaging channels | Agent profile, publishing package | Later | Phone/channel config, agent ID, compliance rules | Voice/SMS/WhatsApp agent endpoint | Useful for marketing demos, not core production-file generation |
| Usage analytics / billing groups / workspaces | Track provider cost, workspace governance, and quota allocation | Provider config, admin settings | Phase 2 | Workspace/API config, project attribution, run metadata | Usage reports, cost allocation | Needed before open-ended generation features are exposed to users |

## Canonical Configuration Objects Needed

### 1. Provider Profile

```yaml
provider: elevenlabs
providerVersionPolicy: docs-indexed
apiBaseUrl: https://api.elevenlabs.io
llmsIndex: https://elevenlabs.io/docs/llms.txt
llmsFullIndex: https://elevenlabs.io/docs/llms-full.txt
supportedCapabilities:
  - text_to_speech
  - text_to_dialogue
  - speech_engine
  - forced_alignment
  - speech_to_text
  - dubbing
  - sound_effects
  - audio_native
```

### 2. Voice Package

```yaml
voicePackageId: narrator-default
provider: elevenlabs
providerVoiceId: TBD
role: narrator
supportedModes:
  - audiobook
  - scene_preview
  - realtime_agent
voiceSettings:
  speed: 1.0
  stability: 0.5
  similarityBoost: 0.8
pronunciationDictionaryRefs: []
consent:
  required: true
  status: not_applicable_for_library_voice
```

### 3. Audio Export Package

```yaml
audioPackageId: scene-001-audio
sourceArtifact:
  type: screenplay_scene
  path: TBD
voicePackages:
  narrator: narrator-default
generationTargets:
  - elevenlabs_tts_http
  - elevenlabs_dialogue
  - elevenlabs_alignment
outputs:
  audio: TBD
  transcript: TBD
  captions: TBD
  timingJson: TBD
```

## MVP Recommendations

1. Define provider and voice-package schemas before writing integration code.
2. Start with HTTP Text to Speech for full text and avoid realtime WebSocket complexity until chat-agent architecture is ready.
3. Add Text to Dialogue once character voice packages exist.
4. Add Forced Alignment early because subtitles, scene timing, and lipsync depend on it.
5. Treat Speech Engine as a Phase 2 realtime agent layer, not the first audiobook path.
6. Store provider voice IDs as external references, never as the canonical character identity.
7. Require consent/licensing metadata before any cloned or custom voice is usable.

## Follow-up Issues This Matrix Supports

- Issue #41: realtime Speech Engine architecture for chat agents
- Issue #42: canonical voice package schema
- Issue #43: alignment and subtitle timing workflow
- Issue #44: provider documentation ingestion using llms.txt indexes
- Issue #33: export profiles for major AI video and audio tools
- Issue #32: pre-movie production package schema

## Definition of Done for Issue #40

- A provider capability matrix exists.
- Content Engine artifact types are mapped to ElevenLabs capabilities.
- MVP, Phase 2, and later capabilities are separated.
- Expected inputs and outputs are documented.
- Provider documentation sources are identified.
- Follow-up implementation work is split into smaller issues.
