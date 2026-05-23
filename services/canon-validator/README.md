# Canon Validator Service

## Purpose

Validate project canon manifests before story artifacts are promoted.

## First Checks

- required manifest fields exist
- canon state is valid
- active canon files are listed
- locked fields are declared
- visual consistency keys are declared

## Output

The service should write:

```text
reports/canon-validation-report.json
```

## Exit Codes

- `0` means validation passed
- `1` means validation failed

## Future Commands

```text
python services/canon-validator/validate_canon.py projects/example/canon/canon-manifest.json
```
