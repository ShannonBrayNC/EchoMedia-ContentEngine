# Lantern Profile Creator Profiles

This directory contains selectable character/model-generation profiles for Lantern Profile Creator.

## Catalog

- `profile-catalog.json` is the runtime picker index.
- Each profile entry points to its canonical `model-generation-profile.json` file.
- Profiles must default to safe-for-work image prompt generation unless a narrower lawful tenant configuration is explicitly approved later.

## Registered Profiles

| Character ID | Display Name | Profile Type | Default Rating | Profile File |
|---|---|---|---|---|
| `valeria-cruz` | Valeria Cruz | fictional-character | safe-for-work | `valeria-cruz/model-generation-profile.json` |

## Required Runtime Gates

Every profile must declare:

- `explicitContent=false`
- `consentRequired=true`
- `minorSafety=strict-block`
- primary admin default and authenticated switching behavior
- negative prompt coverage for UI overlays, watermarks, usernames, minor-coded styling, nudity, and explicit posing
