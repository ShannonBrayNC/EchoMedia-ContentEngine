# Lantern Canon Registry

## Purpose

The Lantern Canon Registry tracks the creative works, story worlds, doctrine notes, and production assets that define the Lantern Protocol narrative universe.

This registry exists because Lantern is both a platform architecture and a story about what happens when systems operate without consent. Creative canon should reinforce platform doctrine, and platform doctrine should keep the story from becoming empty wallpaper.

## Canon status values

| Status | Meaning |
| --- | --- |
| `seed` | Concept exists but is not yet developed. |
| `draft` | Work is being actively drafted. |
| `review` | Work is ready for canon/proofread review. |
| `approved` | Work is approved as canon for downstream production. |
| `archived` | Work is retained but no longer active canon. |

## Canon entries

| Canon ID | Title | Type | Status | Doctrine link | Notes |
| --- | --- | --- | --- | --- | --- |
| `lantern-origin-001` | Systems Without Consent | Novel / dark systems tale | `draft` | Consent-first automation | Explores autonomous systems that optimize without permission, context, or human dignity. |
| `lantern-protocol-001` | The Consent Layer | Audio/book series concept | `draft` | Consent states and trust boundaries | Frames Lantern as the light between helpful automation and silent coercion. |
| `lantern-doctrine-001` | Consent Theme Bible | Doctrine document | `approved` | Platform design rules | Maps recurring story themes to engineering guardrails. |
| `lantern-ets-001` | The Witness Engine | Technical lore / trust anchor | `seed` | ETS proof and verification | Positions ETS as the witness that refuses forged memory. |
| `lantern-christina-001` | The Human Command Layer | Character/system canon | `seed` | Human approval and agency | Defines Christina as the interface that returns control to the human. |

## Asset promotion rules

A creative asset may be promoted from draft to approved canon only when:

1. It has a stable canon ID.
2. It links to a doctrine theme or story world.
3. It has a review owner.
4. It has no unresolved rights/release gate.
5. It has a manifest hash or planned ETS proof reference.
6. It is safe for the intended downstream use.

## Production package rules

No generated asset should be marked production-ready unless the package includes:

- canon ID,
- source project ID,
- artifact ID,
- prompt/template version,
- rights status,
- approval state,
- evidence hash,
- ETS proof reference or explicit local/mock marker,
- human approval record for publishing or provider execution.

## Next additions

- Add manuscript inventory once the active Lantern novel files are normalized.
- Add audiobook package IDs for ElevenLabs production.
- Add visual bible references when image/video packages are created.
- Add approved marketing excerpts for EchoMedia site and launch campaigns.
