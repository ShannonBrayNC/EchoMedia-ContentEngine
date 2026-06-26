# Scene Card Template

**Sprint:** SB-005  
**Book:** Book 01 — Silver Bullet

Use this template for SB-006 manuscript drafting and any future scene-card expansion.

```yaml
- scene_id: sb1-c01-s01
  chapter: 1
  scene: 1
  act: I
  act_name: The Shot
  chapter_title: Example Chapter Title
  scene_title: Example Scene Title
  pov: Jack Mercer
  location: Specific location or setting class
  scene_purpose: One sentence explaining why the scene exists.
  plot_movement: What changes externally by the end of the scene.
  character_movement: What changes internally by the end of the scene.
  trauma_pressure: Active veteran/post-trauma pressure shaping Jack's behavior.
  antagonist_pressure: Active Evelyn/Widow Circle/social pressure, if any.
  narrative_distortion: What truth is distorted, threatened, simplified, or protected.
  evidence_witness_thread: What record, detail, memory, contradiction, testimony, or context survives.
  continuity_impact: What must carry forward into later scenes/chapters/books.
  producer_review_flags:
    - canon
    - character
    - trauma-dignity
    - fictionalization
  drafting_prompt: >-
    Specific prose instruction for drafting the scene.
```

## Technical Edit Requirements
Each scene card must satisfy:

1. Stable `scene_id` format: `sb1-c##-s##`.
2. Required fields present.
3. Act/chapter alignment matches SB-004.
4. No scene exists only for mood; each scene must change plot, character, context, or continuity.
5. Producer Review flags included.
6. Scene language remains fictionalized and non-instructional.

## Producer Review Flag Library

- `canon`
- `character`
- `timeline`
- `trauma-dignity`
- `fictionalization`
- `legal-reputation-sensitivity`
- `institutional-parallel`
- `widow-circle`
- `living-anchor-foreshadowing`
- `evidence-continuity`
- `producer-review-required`
