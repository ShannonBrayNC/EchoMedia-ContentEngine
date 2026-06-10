# Silver Bullet Manuscript Audio Sync Status

## Purpose
Track whether Silver Bullet Book 1 and Book 2 are ready for ElevenReader proof-listening.

## Verified repository paths

### Book 1 current path
`projects/lantern-protocol/case-files/silver-bullet/manuscript/chapters/`

Verified examples:
- `chapter-00-before-the-bullet.md`
- `chapter-01-the-wrong-initial.md`
- `chapter-05-the-house-becomes-evidence.md`

Important note: the verified Book 1 files currently begin with `## Canon Sources`, so they may be scaffold/generated chapter packets rather than clean final prose. Run the audit script to confirm word counts and scaffold-only candidates.

### Book 2 current path
`projects/lantern-protocol/case-files/silver-bullet/book-ii/manuscript/chapters/`

Verified examples:
- `chapter-001-the-house-after-the-headline.md`
- `chapter-018-the-phone-on-the-counter.md`
- `chapter-019-black-lantern-reference.md`
- `chapter-037-celias-last-edit.md`

## Known sync issue
Book 2 Chapter 20 was drafted in chat as `NorthStar Denial`, but the expected repo file was not found at:

`projects/lantern-protocol/case-files/silver-bullet/book-ii/manuscript/chapters/chapter-020-northstar-denial.md`

This implies Book 2 is not fully synced in the repository. Chapters 20-36 were likely drafted in chat/sprint summaries but not all committed as manuscript chapter files.

## Added tooling
Run:

```powershell
pwsh .\projects\lantern-protocol\case-files\silver-bullet\tools\Invoke-SilverBulletAudioAudit.ps1 -RepoRoot C:\workspace\GitHub\EchoMedia-ContentEngine-pr112
```

The script will:
- audit Book 1 and Book 2 manuscript folders
- identify missing chapter numbers
- flag scaffold-only chapter candidates
- compile ElevenReader TXT files
- create an audit report

## Output path

`projects\lantern-protocol\case-files\silver-bullet\compiled\elevenreader\`

Expected outputs:
- `SilverBullet-Book1-ElevenReader.txt`
- `SilverBullet-Book2-ElevenReader.txt`
- `SilverBullet-Books1-2-ElevenReader.txt`
- `SilverBullet-AudioAudit.md`

## Current readiness verdict

### Book 1
Status: Exists, but needs local audit for scaffold/prose completeness.

### Book 2
Status: Not complete in repo. Confirmed missing at least Chapter 20 from the expected Book 2 manuscript path.

## Recommended next sprint
Sprint SB-AUDIO-002: Book 2 Chapter Recovery Sync

Goals:
- restore missing Book 2 chapters 020-036 from chat sprint outputs or local files
- normalize file names
- rerun audio audit
- generate ElevenReader-ready Book 1 and Book 2 proof-listening files
