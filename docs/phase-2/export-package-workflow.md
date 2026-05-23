# Export Package Workflow

## Purpose

The export package generator creates structured project delivery bundles.

## Example Command

```text
python services/export-packager/build_export_package.py projects/example author-review
```

## Supported Package Types

### author-review

Includes:

- manuscript
- storyboards
- reports

### screenplay-review

Includes:

- screenplay
- reports

### full-project

Includes:

- canon
- characters
- story
- manuscript
- storyboards
- screenplay
- reports

## Outputs

The generator creates:

```text
exports/packages/{package-type}/manifest.json
exports/packages/{package-type}/contents.md
```

## Future Expansion

Future versions should support:

- ZIP export
- package versioning
- release tagging
- PDF-ready exports
- automated delivery workflows
