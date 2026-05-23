# Export Packager

## Purpose

Create reproducible project export packages for author review, screenplay review, visual review, and production planning.

## Planned Package Types

- author review package
- manuscript package
- screenplay package
- visual bible package
- production planning package
- full project package

## Command

```text
python services/export-packager/build_export_package.py projects/example author-review
```

## Outputs

```text
exports/packages/{package-name}/manifest.json
exports/packages/{package-name}/contents.md
```

## Future Expansion

- ZIP packaging
- PDF-ready markdown packaging
- release artifact upload
- package checksums
- package versioning
