#!/usr/bin/env node

/**
 * Assemble and audit Lantern Protocol II.
 *
 * Usage from repo root:
 *   node projects/lantern-protocol/novel/scripts/assemble-and-audit-lantern-ii.mjs
 *
 * Outputs:
 *   projects/lantern-protocol/novel/book-ii/exports/lantern-ii-novel-draft.md
 *   projects/lantern-protocol/novel/book-ii/exports/lantern-protocol-ii-elevenlabs.md
 *   projects/lantern-protocol/novel/book-ii/exports/lantern-ii-novel-report.md
 *   projects/lantern-protocol/novel/book-ii/exports/lantern-ii-continuity-audit.md
 *   projects/lantern-protocol/novel/book-ii/exports/lantern-ii-chapter-status.json
 *   projects/lantern-protocol/novel/book-ii/exports/lantern-ii-processing-summary.md
 *   projects/lantern-protocol/novel/book-ii/exports/lantern-ii-release-readiness-review.md
 *   projects/lantern-protocol/novel/book-ii/reports/book-ii-guardrail-warning-review.md
 */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const repoRoot = process.cwd();
const bookRoot = path.join(repoRoot, 'projects', 'lantern-protocol', 'novel', 'book-ii');
const chaptersDir = path.join(bookRoot, 'manuscript', 'chapters');
const exportsDir = path.join(bookRoot, 'exports');
const reportsDir = path.join(bookRoot, 'reports');
const expectedChapterCount = 24;

const requiredSections = [
  '## Canon Sources',
  '## Purpose',
  '## POV',
  '## Chapter Promise',
  '## Manuscript',
  '## Continuity Notes',
  '## Revision Notes',
  '## Processing Metadata'
];

const guardrails = [
  {
    id: 'civic-mirror-not-villain',
    label: 'Civic Mirror remains useful/humanitarian/non-villainous',
    terms: ['Civic Mirror']
  },
  {
    id: 'primary-doctrine',
    label: 'Primary doctrine appears',
    terms: ['Agreement is not consent when stacked into coercion']
  },
  {
    id: 'authority-laundering',
    label: 'Authority laundering / separate agreements tracked',
    terms: ['authority laundering', 'separate agreement', 'separate agreements']
  },
  {
    id: 'no-aegis-major-player',
    label: 'AEGIS is not introduced as a major Book II player',
    forbiddenTerms: ['AEGIS']
  }
];

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function readText(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

function extractSection(content, heading) {
  const start = content.indexOf(heading);
  if (start === -1) {
    return '';
  }

  const afterHeading = content.slice(start + heading.length);
  const nextHeadingMatch = afterHeading.match(/\n##\s+/);
  if (!nextHeadingMatch || nextHeadingMatch.index === undefined) {
    return afterHeading.trim();
  }

  return afterHeading.slice(0, nextHeadingMatch.index).trim();
}

function chapterNumberFromName(fileName) {
  const match = fileName.match(/^chapter-(\d{2})-/);
  return match ? Number.parseInt(match[1], 10) : Number.POSITIVE_INFINITY;
}

function getChapterFiles() {
  if (!fs.existsSync(chaptersDir)) {
    return [];
  }

  return fs
    .readdirSync(chaptersDir)
    .filter((name) => /^chapter-\d{2}-.+\.md$/.test(name))
    .sort((a, b) => chapterNumberFromName(a) - chapterNumberFromName(b));
}

function stripCodeFenceMarkersForNarration(markdown) {
  return markdown
    .replace(/```[a-zA-Z0-9_-]*\r?\n([\s\S]*?)```/g, (_, block) => {
      const artifact = block.trim();
      return artifact ? `Artifact:\n${artifact}` : '';
    })
    .replace(/```/g, '')
    .trim();
}

function countWords(text) {
  return text
    .replace(/```[\s\S]*?```/g, '')
    .split(/\s+/)
    .filter(Boolean).length;
}

function classifyWarning(warning) {
  if (warning.startsWith('Forbidden/controlled term present')) {
    return {
      category: 'controlled-vocabulary',
      severity: 'fix before publication',
      recommendedAction: 'Review the controlled term in context. Remove it unless canon-approved for Book II.',
      proseChangeRequired: true,
      scriptChangeRequired: false
    };
  }

  if (warning.includes('Primary doctrine appears')) {
    return {
      category: 'doctrine-signal',
      severity: 'monitor',
      recommendedAction: 'Confirm the chapter intentionally omits the exact doctrine phrase or carries the doctrine through scene/action.',
      proseChangeRequired: false,
      scriptChangeRequired: false
    };
  }

  if (warning.includes('Authority laundering')) {
    return {
      category: 'theme-signal',
      severity: 'monitor',
      recommendedAction: 'Confirm the chapter still supports the separate-agreements threat model without forcing repeated terminology.',
      proseChangeRequired: false,
      scriptChangeRequired: false
    };
  }

  if (warning.includes('Civic Mirror')) {
    return {
      category: 'civic-mirror-signal',
      severity: 'acceptable',
      recommendedAction: 'Accept if the chapter is intentionally character-, treaty-, or field-focused and does not require Civic Mirror on page.',
      proseChangeRequired: false,
      scriptChangeRequired: false
    };
  }

  return {
    category: 'uncategorized',
    severity: 'monitor',
    recommendedAction: 'Review manually during editorial pass.',
    proseChangeRequired: false,
    scriptChangeRequired: false
  };
}

function auditChapter(fileName) {
  const filePath = path.join(chaptersDir, fileName);
  const content = readText(filePath);
  const manuscript = extractSection(content, '## Manuscript');
  const missingSections = requiredSections.filter((section) => !content.includes(section));
  const isPlaceholder = /Draft placeholder|Replace this section with prose/i.test(manuscript);
  const title = content.match(/^#\s+(.+)$/m)?.[1] ?? fileName;

  const guardrailWarnings = [];
  for (const guardrail of guardrails) {
    if (guardrail.terms && !guardrail.terms.some((term) => content.includes(term))) {
      const warning = `Missing signal: ${guardrail.label}`;
      guardrailWarnings.push({ guardrailId: guardrail.id, warning, ...classifyWarning(warning) });
    }

    if (guardrail.forbiddenTerms && guardrail.forbiddenTerms.some((term) => content.includes(term))) {
      const warning = `Forbidden/controlled term present: ${guardrail.label}`;
      guardrailWarnings.push({ guardrailId: guardrail.id, warning, ...classifyWarning(warning) });
    }
  }

  return {
    number: chapterNumberFromName(fileName),
    file: path.relative(repoRoot, filePath).replaceAll('\\', '/'),
    title,
    status: isPlaceholder ? 'shell' : 'draft',
    missingSections,
    manuscriptWordCount: countWords(manuscript),
    placeholder: isPlaceholder,
    guardrailWarnings
  };
}

function warningSummaryRows(chapterAudits) {
  const rows = [];

  for (const chapter of chapterAudits) {
    for (const item of chapter.guardrailWarnings) {
      rows.push(
        `| ${chapter.number} | ${chapter.title.replace(/^Chapter \d+ — /, '')} | ${item.category} | ${item.severity} | ${item.warning.replaceAll('|', '\\|')} | ${item.recommendedAction.replaceAll('|', '\\|')} | ${item.proseChangeRequired ? 'Yes' : 'No'} | ${item.scriptChangeRequired ? 'Yes' : 'No'} |`
      );
    }
  }

  return rows.join('\n');
}

function writeFile(relativePath, content) {
  const target = path.join(repoRoot, relativePath);
  ensureDir(path.dirname(target));
  fs.writeFileSync(target, content, 'utf8');
}

ensureDir(exportsDir);
ensureDir(reportsDir);

const chapterFiles = getChapterFiles();
const chapterAudits = chapterFiles.map(auditChapter);
const placeholderCount = chapterAudits.filter((chapter) => chapter.placeholder).length;
const missingSectionCount = chapterAudits.reduce((sum, chapter) => sum + chapter.missingSections.length, 0);
const guardrailWarningCount = chapterAudits.reduce((sum, chapter) => sum + chapter.guardrailWarnings.length, 0);
const chapterCountDrift = chapterAudits.length !== expectedChapterCount;
const hasStructuralBlocker = chapterCountDrift || missingSectionCount > 0 || placeholderCount > 0;

const readerDraftPath = 'projects/lantern-protocol/novel/book-ii/exports/lantern-ii-novel-draft.md';
const elevenLabsPath = 'projects/lantern-protocol/novel/book-ii/exports/lantern-protocol-ii-elevenlabs.md';
const reportPath = 'projects/lantern-protocol/novel/book-ii/exports/lantern-ii-novel-report.md';
const continuityPath = 'projects/lantern-protocol/novel/book-ii/exports/lantern-ii-continuity-audit.md';
const statusPath = 'projects/lantern-protocol/novel/book-ii/exports/lantern-ii-chapter-status.json';
const summaryPath = 'projects/lantern-protocol/novel/book-ii/exports/lantern-ii-processing-summary.md';
const readinessPath = 'projects/lantern-protocol/novel/book-ii/exports/lantern-ii-release-readiness-review.md';
const warningReviewPath = 'projects/lantern-protocol/novel/book-ii/reports/book-ii-guardrail-warning-review.md';

const assembled = [
  '# Lantern Protocol II — The Separate Agreements',
  '',
  '> Assembled draft generated from chapter manuscript sections.',
  '',
  ...chapterAudits.flatMap((chapter, index) => {
    const content = readText(path.join(repoRoot, chapter.file));
    const manuscript = extractSection(content, '## Manuscript');
    return [
      index === 0 ? '' : '\n---',
      '',
      `# ${chapter.title}`,
      '',
      manuscript || '> Missing manuscript section.'
    ];
  })
].join('\n').trim() + '\n';

const elevenLabs = [
  '# Lantern Protocol II — The Separate Agreements',
  '',
  ...chapterAudits.flatMap((chapter, index) => {
    const content = readText(path.join(repoRoot, chapter.file));
    const manuscript = stripCodeFenceMarkersForNarration(extractSection(content, '## Manuscript'));
    return [
      index === 0 ? '' : '\n',
      `# ${chapter.title}`,
      '',
      manuscript || 'Missing manuscript section.'
    ];
  })
].join('\n').trim() + '\n';

const elevenLabsHasCodeFence = /```/.test(elevenLabs);
const report = `# Lantern Protocol II — Assembly Report

## Summary

| Metric | Value |
|---|---:|
| Expected chapters | ${expectedChapterCount} |
| Found chapters | ${chapterAudits.length} |
| Placeholder chapters | ${placeholderCount} |
| Missing required sections | ${missingSectionCount} |
| Guardrail warnings | ${guardrailWarningCount} |
| Chapter count drift | ${chapterCountDrift ? 'Yes' : 'No'} |
| ElevenLabs code-fence warnings | ${elevenLabsHasCodeFence ? 'Yes' : 'No'} |

## Generated Outputs

- Reader draft: \`${readerDraftPath}\`
- ElevenLabs narration export: \`${elevenLabsPath}\`
- Assembly report: \`${reportPath}\`
- Continuity audit: \`${continuityPath}\`
- Chapter status JSON: \`${statusPath}\`
- Processing summary: \`${summaryPath}\`
- Release-readiness review: \`${readinessPath}\`
- Guardrail-warning review: \`${warningReviewPath}\`

## Chapter Status

| # | Chapter | Status | Words | Missing Sections | Guardrail Warnings |
|---:|---|---|---:|---:|---:|
${chapterAudits.map((chapter) => `| ${chapter.number} | ${chapter.title.replace(/^Chapter \d+ — /, '')} | ${chapter.status} | ${chapter.manuscriptWordCount} | ${chapter.missingSections.length} | ${chapter.guardrailWarnings.length} |`).join('\n')}
`;

const audit = `# Lantern Protocol II — Continuity Audit

## Canon Checks

- Expected chapter count: ${expectedChapterCount}
- Found chapter count: ${chapterAudits.length}
- Chapter count drift: ${chapterCountDrift ? 'YES' : 'NO'}
- Placeholder manuscript sections: ${placeholderCount}
- Missing required sections: ${missingSectionCount}
- Guardrail warnings: ${guardrailWarningCount}
- ElevenLabs code-fence warnings: ${elevenLabsHasCodeFence ? 'YES' : 'NO'}

## Chapter Findings

${chapterAudits.map((chapter) => {
  const findings = [];
  if (chapter.placeholder) findings.push('- Placeholder manuscript still present.');
  for (const section of chapter.missingSections) findings.push(`- Missing section: ${section}`);
  for (const warning of chapter.guardrailWarnings) findings.push(`- ${warning.warning}`);
  return `### ${chapter.title}\n\n${findings.length ? findings.join('\n') : '- No findings.'}`;
}).join('\n\n')}
`;

const status = {
  book: 'Lantern Protocol II: The Separate Agreements',
  expectedChapterCount,
  foundChapterCount: chapterAudits.length,
  placeholderCount,
  missingSectionCount,
  guardrailWarningCount,
  chapterCountDrift,
  elevenLabsCodeFenceWarning: elevenLabsHasCodeFence,
  generatedOutputs: {
    readerDraftPath,
    elevenLabsPath,
    reportPath,
    continuityPath,
    statusPath,
    summaryPath,
    readinessPath,
    warningReviewPath
  },
  chapters: chapterAudits
};

const summary = `# Lantern Protocol II — Processing Summary

Generated by \`projects/lantern-protocol/novel/scripts/assemble-and-audit-lantern-ii.mjs\`.

## Result

${hasStructuralBlocker ? 'Review required before release packaging.' : 'Book II is structurally complete. Required-section, placeholder, and chapter-count checks passed.'}

## Current Counts

| Metric | Value |
|---|---:|
| Expected chapters | ${expectedChapterCount} |
| Found chapters | ${chapterAudits.length} |
| Placeholder chapters | ${placeholderCount} |
| Missing required sections | ${missingSectionCount} |
| Guardrail warnings | ${guardrailWarningCount} |
| Chapter count drift | ${chapterCountDrift ? 'Yes' : 'No'} |
| ElevenLabs code-fence warnings | ${elevenLabsHasCodeFence ? 'Yes' : 'No'} |

## Next Actions

1. Review guardrail warnings as editorial prompts, not automatic failures.
2. Validate \`${readerDraftPath}\` for reader-facing markdown.
3. Validate \`${elevenLabsPath}\` for narration upload formatting.
4. Keep chapter-count drift as a canon review item before merge.
`;

const readiness = `# Lantern Protocol II: Release-Readiness Review

Issue: #142

Purpose: Add a human editorial interpretation layer for the automated Book II assembly and continuity audit.

## Source Outputs Reviewed

- \`${readerDraftPath}\`
- \`${elevenLabsPath}\`
- \`${reportPath}\`
- \`${continuityPath}\`
- \`${statusPath}\`
- \`${summaryPath}\`
- \`${warningReviewPath}\`

## Audit Summary

| Check | Result | Interpretation |
|---|---:|---|
| Expected chapters | ${expectedChapterCount} | Pass. Matches canon lock. |
| Found chapters | ${chapterAudits.length} | ${chapterAudits.length === expectedChapterCount ? 'Pass. No missing chapter shell.' : 'Review. Chapter count differs from canon lock.'} |
| Chapter count drift | ${chapterCountDrift ? 'Yes' : 'No'} | ${chapterCountDrift ? 'Canon review required.' : 'Pass. No canon escalation required.'} |
| Missing required sections | ${missingSectionCount} | ${missingSectionCount === 0 ? 'Pass. Every chapter has required sections.' : 'Review. Required section gaps remain.'} |
| Placeholder chapters | ${placeholderCount} | ${placeholderCount === 0 ? 'Pass. No placeholder manuscript sections remain.' : 'Release blocker until drafted.'} |
| Guardrail warnings | ${guardrailWarningCount} | Editorial review prompts, not automatic failures. |
| ElevenLabs code-fence warnings | ${elevenLabsHasCodeFence ? 'Yes' : 'No'} | ${elevenLabsHasCodeFence ? 'Review narration export before upload.' : 'Pass. Narration export contains no code-fence markers.'} |

## Current Release Status

**${hasStructuralBlocker ? 'Editorial review required before reader release.' : 'Structurally complete and ready for editorial polish.'}**

Book II is structurally complete when all 24 chapters are present, no placeholder manuscript sections remain, and no required manuscript sections are missing. The manuscript is ready for reader-facing export validation, guardrail-warning review, and final editorial polish.

## Placeholder Interpretation

Current state:

- Placeholder manuscript sections: ${placeholderCount}
- Old placeholder status: resolved when this value is 0.

The prior placeholder-era warning that Chapters 5-24 were shells is no longer valid when this review is generated from the completed draft audit.

## Guardrail Warning Interpretation

The guardrail warnings are editorial review prompts. They do not indicate chapter-count drift or missing required sections. They should stay visible until final editorial review confirms whether each warning is acceptable, requires prose polish, or should become a script false positive.

## Passed Gates

- [${chapterAudits.length === expectedChapterCount ? 'x' : ' '}] Chapter count remains 24.
- [${!chapterCountDrift ? 'x' : ' '}] No chapter-count drift.
- [${missingSectionCount === 0 ? 'x' : ' '}] No missing required sections.
- [${placeholderCount === 0 ? 'x' : ' '}] Placeholder manuscript count is 0.
- [x] Chapter status JSON exists.
- [x] Assembly report exists.
- [x] Continuity audit exists.
- [x] Processing summary exists.

## Not Yet Passed

- [ ] Guardrail warnings have been reviewed after every drafting sprint.
- [ ] Final reader-facing export has been spot-checked.
- [ ] ElevenLabs narration export has been spot-checked.
- [ ] Title and chapter headings have been reviewed for final bold/heading formatting.

## Editorial Risk Register

| Risk | Severity | Current Status | Required Action |
|---|---|---|---|
| Chapter count drift | High | ${chapterCountDrift ? 'Present' : 'Not present'} | Keep canon lock active. |
| Placeholder chapters | High for release | ${placeholderCount > 0 ? `${placeholderCount} present` : 'Resolved'} | Re-run audit after each prose sprint. |
| Controlled vocabulary drift | Medium | Internal warning only | Review guardrail-warning report. |
| Civic Mirror simplification | Medium | Monitor | Preserve useful and morally difficult posture. |
| Authority-laundering dilution | High | Monitor | Keep separate-agreement stack as Book II threat shape. |
| Book III overtake | Medium | Monitor | Keep delegated-consent handoff secondary. |

## Closure Statement

The Book II continuity audit and release-readiness pass is current as of the latest script run. Book II may proceed with editorial polish and media-prep planning, provided the audit is re-run after each drafting sprint and before reader-facing or ElevenLabs upload.
`;

const warningReview = `# Book II Guardrail Warning Review

Issue: #143

## Summary

| Metric | Value |
|---|---:|
| Total guardrail warnings | ${guardrailWarningCount} |
| Chapter count drift | ${chapterCountDrift ? 'Yes' : 'No'} |
| Missing required sections | ${missingSectionCount} |
| Placeholder chapters | ${placeholderCount} |

## Interpretation

Guardrail warnings are editorial review prompts, not automatic release failures. They do not indicate chapter-count drift or missing-section failures.

## Severity Definitions

| Severity | Meaning |
|---|---|
| blocker | Must be resolved before publication packaging. |
| fix before publication | Should be resolved or explicitly waived before publication. |
| monitor | Review during editorial pass. |
| acceptable | Likely acceptable if intentional in context. |
| script false positive | Adjust the audit script rather than prose. |

## Warning Table

| Chapter | Title | Category | Severity | Warning | Recommended Action | Prose Change Required | Script Change Required |
|---:|---|---|---|---|---|---|---|
${warningSummaryRows(chapterAudits) || '| - | - | - | - | No guardrail warnings. | No action required. | No | No |'}

## Recommended Editorial Action

1. Treat missing exact doctrine or theme signals as context checks, not automatic prose edits.
2. Preserve anchor phrases where they are strongest rather than forcing them into every chapter.
3. Review any controlled-vocabulary warning before publication.
4. Keep Civic Mirror useful, humanitarian, and morally difficult.
5. Keep the separate-agreements / authority-laundering threat visible across the manuscript without turning the language into repeated lecture.
`;

writeFile(readerDraftPath, assembled);
writeFile(elevenLabsPath, elevenLabs);
writeFile(reportPath, report);
writeFile(continuityPath, audit);
writeFile(statusPath, `${JSON.stringify(status, null, 2)}\n`);
writeFile(summaryPath, summary);
writeFile(readinessPath, readiness);
writeFile(warningReviewPath, warningReview);

console.log(`Lantern II assembly complete. Found ${chapterAudits.length}/${expectedChapterCount} chapter file(s).`);
console.log(`Placeholder chapters: ${placeholderCount}.`);
console.log(`Missing required sections: ${missingSectionCount}.`);
console.log(`Guardrail warnings: ${guardrailWarningCount}.`);
console.log(`ElevenLabs code-fence warnings: ${elevenLabsHasCodeFence ? 'Yes' : 'No'}.`);
