#!/usr/bin/env node

/**
 * Assemble and audit Lantern Protocol II.
 *
 * Usage from repo root:
 *   node projects/lantern-protocol/novel/scripts/assemble-and-audit-lantern-ii.mjs
 *
 * Outputs:
 *   projects/lantern-protocol/novel/book-ii/exports/lantern-ii-novel-draft.md
 *   projects/lantern-protocol/novel/book-ii/exports/lantern-ii-novel-report.md
 *   projects/lantern-protocol/novel/book-ii/exports/lantern-ii-continuity-audit.md
 *   projects/lantern-protocol/novel/book-ii/exports/lantern-ii-chapter-status.json
 *   projects/lantern-protocol/novel/book-ii/exports/lantern-ii-processing-summary.md
 */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const repoRoot = process.cwd();
const bookRoot = path.join(repoRoot, 'projects', 'lantern-protocol', 'novel', 'book-ii');
const chaptersDir = path.join(bookRoot, 'manuscript', 'chapters');
const exportsDir = path.join(bookRoot, 'exports');
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
      guardrailWarnings.push(`Missing signal: ${guardrail.label}`);
    }

    if (guardrail.forbiddenTerms && guardrail.forbiddenTerms.some((term) => content.includes(term))) {
      guardrailWarnings.push(`Forbidden/controlled term present: ${guardrail.label}`);
    }
  }

  return {
    number: chapterNumberFromName(fileName),
    file: path.relative(repoRoot, filePath).replaceAll('\\\\', '/'),
    title,
    status: isPlaceholder ? 'shell' : 'draft',
    missingSections,
    manuscriptWordCount: manuscript
      .replace(/```[\s\S]*?```/g, '')
      .split(/\s+/)
      .filter(Boolean).length,
    placeholder: isPlaceholder,
    guardrailWarnings
  };
}

function writeFile(relativePath, content) {
  const target = path.join(repoRoot, relativePath);
  ensureDir(path.dirname(target));
  fs.writeFileSync(target, content, 'utf8');
}

ensureDir(exportsDir);

const chapterFiles = getChapterFiles();
const chapterAudits = chapterFiles.map(auditChapter);
const placeholderCount = chapterAudits.filter((chapter) => chapter.placeholder).length;
const missingSectionCount = chapterAudits.reduce((sum, chapter) => sum + chapter.missingSections.length, 0);
const guardrailWarningCount = chapterAudits.reduce((sum, chapter) => sum + chapter.guardrailWarnings.length, 0);
const chapterCountDrift = chapterAudits.length !== expectedChapterCount;

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

const report = `# Lantern Protocol II — Assembly Report\n\n## Summary\n\n| Metric | Value |\n|---|---:|\n| Expected chapters | ${expectedChapterCount} |\n| Found chapters | ${chapterAudits.length} |\n| Placeholder chapters | ${placeholderCount} |\n| Missing required sections | ${missingSectionCount} |\n| Guardrail warnings | ${guardrailWarningCount} |\n| Chapter count drift | ${chapterCountDrift ? 'Yes' : 'No'} |\n\n## Chapter Status\n\n| # | Chapter | Status | Words | Missing Sections | Guardrail Warnings |\n|---:|---|---|---:|---:|---:|\n${chapterAudits.map((chapter) => `| ${chapter.number} | ${chapter.title.replace(/^Chapter \d+ — /, '')} | ${chapter.status} | ${chapter.manuscriptWordCount} | ${chapter.missingSections.length} | ${chapter.guardrailWarnings.length} |`).join('\n')}\n`;

const audit = `# Lantern Protocol II — Continuity Audit\n\n## Canon Checks\n\n- Expected chapter count: ${expectedChapterCount}\n- Found chapter count: ${chapterAudits.length}\n- Chapter count drift: ${chapterCountDrift ? 'YES' : 'NO'}\n- Placeholder manuscript sections: ${placeholderCount}\n- Missing required sections: ${missingSectionCount}\n- Guardrail warnings: ${guardrailWarningCount}\n\n## Chapter Findings\n\n${chapterAudits.map((chapter) => {
  const findings = [];
  if (chapter.placeholder) findings.push('- Placeholder manuscript still present.');
  for (const section of chapter.missingSections) findings.push(`- Missing section: ${section}`);
  for (const warning of chapter.guardrailWarnings) findings.push(`- ${warning}`);
  return `### ${chapter.title}\n\n${findings.length ? findings.join('\n') : '- No findings.'}`;
}).join('\n\n')}\n`;

const status = {
  book: 'Lantern Protocol II: The Separate Agreements',
  expectedChapterCount,
  foundChapterCount: chapterAudits.length,
  placeholderCount,
  missingSectionCount,
  guardrailWarningCount,
  chapterCountDrift,
  chapters: chapterAudits
};

const summary = `# Lantern Protocol II — Processing Summary\n\nGenerated by \`projects/lantern-protocol/novel/scripts/assemble-and-audit-lantern-ii.mjs\`.\n\n## Result\n\n${chapterCountDrift || missingSectionCount > 0 ? 'Review required before release packaging.' : 'Structure passed required-section and chapter-count checks.'}\n\n## Next Actions\n\n1. Replace placeholder manuscript sections with prose.\n2. Re-run this script after each drafting pass.\n3. Treat any chapter-count drift as a canon review item before merge.\n4. Use guardrail warnings as editorial review prompts, not automatic failures.\n`;

writeFile('projects/lantern-protocol/novel/book-ii/exports/lantern-ii-novel-draft.md', assembled);
writeFile('projects/lantern-protocol/novel/book-ii/exports/lantern-ii-novel-report.md', report);
writeFile('projects/lantern-protocol/novel/book-ii/exports/lantern-ii-continuity-audit.md', audit);
writeFile('projects/lantern-protocol/novel/book-ii/exports/lantern-ii-chapter-status.json', `${JSON.stringify(status, null, 2)}\n`);
writeFile('projects/lantern-protocol/novel/book-ii/exports/lantern-ii-processing-summary.md', summary);

console.log(`Lantern II assembly complete. Found ${chapterAudits.length}/${expectedChapterCount} chapter file(s).`);
console.log(`Placeholder chapters: ${placeholderCount}.`);
console.log(`Missing required sections: ${missingSectionCount}.`);
console.log(`Guardrail warnings: ${guardrailWarningCount}.`);
