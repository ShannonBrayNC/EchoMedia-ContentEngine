# Chapter Packet Workflow

## Purpose

The chapter packet builder creates a standardized production packet for each chapter.

## Included Artifacts

The builder creates:

- chapter brief
- manuscript chapter scaffold
- storyboard scaffold
- image prompt scaffold

## Example Command

```text
python services/chapter-engine/build_chapter_packet.py projects/example 1 "Arrival"
```

## Generated Structure

```text
manuscript/chapter-briefs/chapter-01.md
manuscript/chapters/chapter-01.md
storyboards/chapters/chapter-01-storyboard.md
visual-bible/chapter-image-prompts/chapter-01-images.md
```

## Future Expansion

Future versions should support:

- template injection
- continuity mapping
- screenplay handoff preparation
- chapter indexing
- automated image prompt expansion
- audit generation
