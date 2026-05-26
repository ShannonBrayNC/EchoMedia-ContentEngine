# Provider Documentation Ingestion Strategy

## Purpose

Content Engine provider adapters must be grounded in provider documentation that agents can rediscover and cite. This strategy defines how AI agents should find, cache, summarize, and version provider capability notes without building a crawler in this sprint.

## Discovery Convention

For each provider, agents should check documentation in this order:

1. Provider-maintained `llms.txt`.
2. Provider-maintained `llms-full.txt`.
3. Official Markdown documentation exports.
4. Official OpenAPI or schema documents.
5. Official product/API reference pages.

Do not use third-party gateway documentation as the primary source unless the integration has been explicitly approved as a gateway integration.

## Provider Registry

Each provider should have a registry note with:

- `providerName`,
- official docs root,
- `llms.txt` URL if available,
- `llms-full.txt` URL if available,
- last reviewed date,
- reviewed by,
- capability summary,
- known limits,
- auth and secret handling notes,
- pricing/cost warning fields,
- terms/rights notes,
- breaking-change watch areas,
- export profile mappings,
- validation rule mappings.

Initial provider set:

- ElevenLabs,
- OpenAI,
- Runway,
- Pika,
- Kling,
- Luma/Dream Machine,
- Azure Speech,
- local/offline providers,
- future avatar, video, and audio providers.

## Caching And Versioning

Provider documentation summaries should be committed as compact repo-local capability notes, not wholesale scraped docs. Each note should carry a reviewed timestamp, source URLs, and a version label. Large raw documentation snapshots should stay out of the repo unless explicitly approved.

## Capability Summaries

Provider capability notes should map source docs into canonical schemas:

- voice synthesis capability profiles,
- video generation capability profiles,
- export profile constraints,
- provider limits,
- job lifecycle states,
- rights/commercial-use constraints,
- validation gates.

## Breaking Change Detection

Agents should flag a provider for review when:

- a documented model name disappears,
- request/response fields change,
- duration, aspect, voice, or format limits change,
- auth or region rules change,
- provider terms affect commercial use,
- live adapter behavior diverges from the no-provider contract tests.

## Source Citation Rules

When a provider-specific adapter changes behavior, the issue or PR should cite the official docs source used for that mapping. If no official source is available, the provider profile must remain `planned` or `blocked` and live execution must stay disabled.

## Validation Mapping

Provider docs should feed validation layers by producing:

- allowed model names,
- allowed output formats,
- supported modes,
- duration and character limits,
- aspect ratio or resolution limits,
- required asset types,
- webhook support indicators,
- rights and approval gates.

This keeps provider-specific changes in profile data and adapter validation instead of spreading provider assumptions across the UI or production package schemas.
