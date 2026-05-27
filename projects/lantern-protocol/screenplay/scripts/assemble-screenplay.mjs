#!/usr/bin/env node

import { mkdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const repoRoot = process.cwd();

const sources = [
  {
    label: 'Pages 001-010',
    path: 'projects/lantern-protocol/movie/screenplay/pages-001-010.md'
  },
  {
    label: 'Pages 011-020',
    path: 'projects/lantern-protocol/movie/screenplay/pages-011-020.md'
  }
];

const outputMarkdownPath = resolve(repoRoot, 'projects/lantern-protocol/screenplay/exports/screenplay-draft.md');
const outputFountainPath = resolve(repoRoot, 'projects/lantern-protocol/screenplay/exports/screenplay-draft.fountain');
const reportPath = resolve(repoRoot, 'projects/lantern-protocol/screenplay/review/screenplay-import-status.md');

function stripScreenplayFence(markdown) {
  const match = markdown.match(/```screenplay\n([\s\S]*?)\n```/m);
  return match ? match[1].trim() : markdown.trim();
}

function readSource(source) {
  const absolutePath = resolve(repoRoot, source.path);

  if (!existsSync(absolutePath)) {
    throw new Error(`Missing screenplay source: ${source.path}`);
  }

  const raw = readFileSync(absolutePath, 'utf8');
  return {
    ...source,
    raw,
    screenplayText: stripScreenplayFence(raw)
  };
}

function buildMarkdown(sourceDocs) {
  const generatedAt = new Date().toISOString();
  const body = sourceDocs
    .map((source) => [
      `## ${source.label}`,
      '',
      `Source: \`${source.path}\``,
      '',
      '```screenplay',
      source.screenplayText,
      '```'
    ].join('\n'))
    .join('\n\n---\n\n');

  return [
    '# Lantern Protocol — Screenplay Draft',
    '',
    `Generated: ${generatedAt}`,
    '',
    'This file is assembled from committed screenplay source pages. It is intended for screenplay review and adaptation work, not ElevenReader narration upload or KDP retail publishing.',
    '',
    body,
    ''
  ].join('\n');
}

function buildFountain(sourceDocs) {
  const body = sourceDocs
    .map((source) => [
      `/* Source: ${source.path} */`,
      '',
      source.screenplayText
    ].join('\n'))
    .join('\n\n\n');

  return [
    'Title: Lantern Protocol',
    'Credit: Screenplay sample export',
    'Source: EchoMedia Content Engine',
    '',
    body,
    ''
  ].join('\n');
}

function buildReport(sourceDocs) {
  const generatedAt = new Date().toISOString();
  const labels = sourceDocs.map((source) => source.label).join(', ');

  return [
    '# Screenplay Import Status',
    '',
    `Generated: ${generatedAt}`,
    '',
    '## Status',
    '',
    `The normalized screenplay workspace is active. The current export is assembled from the committed screenplay page batches: ${labels}.`,
    '',
    '## Imported sources',
    '',
    ...sourceDocs.map((source) => `- ${source.label}: \`${source.path}\``),
    '',
    '## Known gap',
    '',
    'Pages 001-020 are currently available as committed screenplay pages. Pages 021+ still need to be drafted or imported.',
    '',
    '## Next writing target',
    '',
    'Continue from the preliminary inquiry into:',
    '',
    '- Agency claims that Lantern remained advisory',
    '- Marcus Thorne presenting the honest speed argument',
    '- Naomi refusing to let Mateo become only a symbol',
    '- Public chants splitting into LET IT SAVE US and NAME THE HAND',
    '',
    '## Validation',
    '',
    '- Markdown export generated: `projects/lantern-protocol/screenplay/exports/screenplay-draft.md`',
    '- Fountain export generated: `projects/lantern-protocol/screenplay/exports/screenplay-draft.fountain`',
    ''
  ].join('\n');
}

const sourceDocs = sources.map(readSource);

mkdirSync(dirname(outputMarkdownPath), { recursive: true });
mkdirSync(dirname(outputFountainPath), { recursive: true });
mkdirSync(dirname(reportPath), { recursive: true });

writeFileSync(outputMarkdownPath, buildMarkdown(sourceDocs), 'utf8');
writeFileSync(outputFountainPath, buildFountain(sourceDocs), 'utf8');
writeFileSync(reportPath, buildReport(sourceDocs), 'utf8');

console.log(`Assembled ${sourceDocs.length} screenplay source file(s).`);
console.log(`Wrote ${outputMarkdownPath}`);
console.log(`Wrote ${outputFountainPath}`);
console.log(`Wrote ${reportPath}`);
