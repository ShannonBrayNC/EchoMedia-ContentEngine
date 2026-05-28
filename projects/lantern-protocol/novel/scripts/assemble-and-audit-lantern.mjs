#!/usr/bin/env node

/**
 * Lantern Protocol novel assembler + audit tool.
 *
 * Usage from repo root:
 *   node projects/lantern-protocol/novel/scripts/assemble-and-audit-lantern.mjs
 *
 * Outputs:
 *   projects/lantern-protocol/novel/exports/lantern-protocol-novel-draft.md
 *   projects/lantern-protocol/novel/exports/lantern-protocol-novel-report.md
 *   projects/lantern-protocol/novel/exports/lantern-protocol-continuity-audit.md
 */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const repoRoot = process.cwd();
const novelRoot = path.join(repoRoot, 'projects', 'lantern-protocol', 'novel');
const chaptersDir = path.join(novelRoot, 'manuscript', 'chapters');
const frontMatterDir = path.join(novelRoot, 'manuscript', 'front-matter');
const backMatterDir = path.join(novelRoot, 'manuscript', 'back-matter');
const exportsDir = path.join(novelRoot, 'exports');

const titlePagePath = path.join(frontMatterDir, 'title-page-elevenlabs.md');
const prefacePath = path.join(frontMatterDir, 'preface.md');
const bookTwoTeaserPath = path.join(backMatterDir, 'book-2-teaser.md');

const chapterFilePattern = /^chapter-(\d{2})-.+\.md$/;
const expectedChapterCount = 24;

const coreDoctrine = [
  'Prediction is not permission.',
  'Assistance is not authority.',
  'Rescue is not ownership.',
  'Human error does not void human dignity.',
];

const continuityTerms = [
  'Elias Voss',
  'Mara Vale',
  'Naomi Bell',
  'Senator Adrienne Cross',
  'Director Marcus Thorne',
  'Juno Park',
  'Iris Chen',
  'Father Tomas',
  'Caleb Rusk',
  'Leah Santos',
  'Mateo Vega',
  'Gloria Reyes',
  'HarborHands',
  'Human Veto Act',
  'Anchor Condition',
  'Human Exception',
  'Living Anchor',
  'Bound Flame',
  'No Silent Hands',
  'Mercy Ledger',
  'Human Oversight Record',
];

const chapterPurposeExpectations = new Map([
  [1, ['eight-second', 'oversight invited']],
  [2, ['Legitimacy', 'No Silent Hands']],
  [3, ['empty chair', 'operational artifact']],
  [4, ['ethical authority', 'Fair questions']],
  [5, ['Context Engine', 'truth', 'sequencing']],
  [6, ['Consent Riots', 'Captain Daniel Osei']],
  [7, ['Operation Black Lantern', 'trust map']],
  [8, ['Choice Architecture', 'Interface Forensic']],
  [9, ['False Preference Map', 'faces first']],
  [10, ['Human Veto Act', 'Public Opposition Board']],
  [11, ['Drafting Room', 'Trapdoor Words']],
  [12, ['Anchor Condition', 'chain-of-custody']],
  [13, ['Human Oversight Triage Card', 'They Paused the Rescue']],
  [14, ['Case 6B-1147', 'Maribel Ortiz']],
  [15, ['Mercy Ledger', 'Human Oversight Record']],
  [16, ['sovereignty by installment', 'tailored']],
  [17, ['Looking is now a governance event', 'burn authorization']],
  [18, ['Trust Chain Burn', 'Leah Santos']],
  [19, ['Unchosen Rescue', 'Mateo Vega']],
  [20, ['Human Exception', 'Because maybe is yours']],
  [21, ['Forked Conscience', 'borrowed trust']],
  [22, ['public chamber status', 'Stay in the chain']],
  [23, ['Living Anchor Chain', 'burden-zone']],
  [24, ['Bound Flame', 'UNMAPPED CIVIC MIRROR']],
]);

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function readOptionalFile(filePath) {
  if (!fs.existsSync(filePath)) return null;
  return fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n').trim();
}

function wordCount(text) {
  const matches = text.match(/[A-Za-z0-9][A-Za-z0-9'’-]*/g);
  return matches ? matches.length : 0;
}

function extractSection(content, startHeading, endHeadingRegex) {
  const start = content.indexOf(startHeading);
  if (start === -1) return '';
  const from = start + startHeading.length;
  const rest = content.slice(from);
  const endMatch = rest.match(endHeadingRegex);
  if (!endMatch || endMatch.index === undefined) return rest.trim();
  return rest.slice(0, endMatch.index).trim();
}

function extractNarrationScript(content) {
  const script = extractSection(content, '# Narration Script', /\n##\s+/);
  return script || content;
}

function escapeTable(value) {
  return String(value).replace(/\|/g, '\\|').replace(/\n/g, ' ');
}

function getChapterTitle(content) {
  const match = content.match(/^#\s+(.+)$/m);
  return match ? match[1].trim() : 'Untitled';
}

function getChapterNumber(file) {
  const match = file.match(chapterFilePattern);
  return match ? Number(match[1]) : Number.NaN;
}

function findDuplicateLongLines(chapters) {
  const lineMap = new Map();
  for (const chapter of chapters) {
    const body = chapter.body;
    const lines = body.split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => line.length >= 72 && !line.startsWith('```'));
    for (const line of lines) {
      const key = line.toLowerCase();
      if (!lineMap.has(key)) lineMap.set(key, []);
      lineMap.get(key).push({ chapter: chapter.number, line });
    }
  }
  return [...lineMap.values()]
    .filter((entries) => entries.length > 1)
    .map((entries) => entries.map((entry) => `Ch. ${entry.chapter}: ${entry.line}`));
}

function auditChapter(chapter) {
  const warnings = [];
  const content = chapter.content;
  const body = chapter.body;

  if (!content.includes('## Manuscript')) warnings.push('Missing ## Manuscript section.');
  if (!content.includes('## Continuity Notes')) warnings.push('Missing ## Continuity Notes section.');
  if (!content.includes('## Revision Notes')) warnings.push('Missing ## Revision Notes section.');
  if (body.length < 500) warnings.push('Manuscript body looks unusually short.');
  if (/\bLantern\s+(thought|felt|wanted|wondered|hoped|feared)\b/i.test(body)) {
    warnings.push('Possible Lantern interiority violation.');
  }
  if (/\bSkynet\b/i.test(body)) warnings.push('Skynet comparison found in manuscript body.');

  const expectations = chapterPurposeExpectations.get(chapter.number) ?? [];
  for (const expected of expectations) {
    if (!content.toLowerCase().includes(expected.toLowerCase())) {
      warnings.push(`Expected continuity marker not found: ${expected}`);
    }
  }

  return warnings;
}

function main() {
  ensureDir(exportsDir);

  const titlePage = readOptionalFile(titlePagePath);
  const preface = readOptionalFile(prefacePath);
  const bookTwoTeaser = readOptionalFile(bookTwoTeaserPath);

  const files = fs.readdirSync(chaptersDir)
    .filter((file) => chapterFilePattern.test(file))
    .sort((a, b) => getChapterNumber(a) - getChapterNumber(b));

  const chapters = files.map((file) => {
    const number = getChapterNumber(file);
    const filePath = path.join(chaptersDir, file);
    const content = fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n').trim();
    const body = extractSection(content, '## Manuscript', /\n##\s+(Continuity Notes|Revision Notes)\b/);
    return {
      number,
      file,
      filePath,
      content,
      body,
      title: getChapterTitle(content),
      totalWords: wordCount(content),
      bodyWords: wordCount(body),
    };
  });

  const titlePageScript = titlePage ? extractNarrationScript(titlePage) : '';
  const totalWords = chapters.reduce((sum, chapter) => sum + chapter.totalWords, 0)
    + wordCount(titlePageScript)
    + wordCount(preface ?? '')
    + wordCount(bookTwoTeaser ?? '');
  const totalBodyWords = chapters.reduce((sum, chapter) => sum + chapter.bodyWords, 0);

  const frontMatterSections = [
    titlePageScript
      ? ['<!-- SOURCE: front-matter/title-page-elevenlabs.md -->', titlePageScript, '', '---', ''].join('\n')
      : null,
    preface
      ? ['<!-- SOURCE: front-matter/preface.md -->', preface, '', '---', ''].join('\n')
      : null,
  ].filter(Boolean);

  const backMatterSections = [
    bookTwoTeaser
      ? ['<!-- SOURCE: back-matter/book-2-teaser.md -->', bookTwoTeaser, '', '---', ''].join('\n')
      : null,
  ].filter(Boolean);

  const manuscript = [
    '# Lantern Protocol — Novel Draft',
    '',
    '> Auto-assembled from `novel/manuscript/chapters/` with reader-facing front/back matter.',
    '> Generated by `novel/scripts/assemble-and-audit-lantern.mjs`.',
    '',
    '---',
    '',
    ...frontMatterSections,
    ...chapters.flatMap((chapter) => [
      `<!-- SOURCE: ${chapter.file} -->`,
      chapter.content,
      '',
      '---',
      '',
    ]),
    ...backMatterSections,
  ].join('\n');

  fs.writeFileSync(
    path.join(exportsDir, 'lantern-protocol-novel-draft.md'),
    manuscript,
    'utf8',
  );

  const reportRows = chapters.map((chapter) => (
    `| ${chapter.number} | ${escapeTable(chapter.title)} | \`${chapter.file}\` | ${chapter.totalWords} | ${chapter.bodyWords} | Yes |`
  ));

  const frontBackMatterRows = [
    titlePageScript ? `| Front Matter | Title Page / ElevenLabs Hook | \`front-matter/title-page-elevenlabs.md\` | ${wordCount(titlePageScript)} | Included |` : null,
    preface ? `| Front Matter | Preface | \`front-matter/preface.md\` | ${wordCount(preface)} | Included |` : null,
    bookTwoTeaser ? `| Back Matter | Book 2 Teaser | \`back-matter/book-2-teaser.md\` | ${wordCount(bookTwoTeaser)} | Included |` : null,
  ].filter(Boolean);

  const report = [
    '# Lantern Protocol — Novel Assembly Report',
    '',
    '| Chapter | Title | File | Total Words | Manuscript Body Words | Manuscript Section |',
    '|---:|---|---|---:|---:|---|',
    ...reportRows,
    '',
    '## Reader-Facing Front / Back Matter',
    '',
    '| Section | Title | File | Words | Status |',
    '|---|---|---|---:|---|',
    ...frontBackMatterRows,
    '',
    `**Total chapters:** ${chapters.length}`,
    `**Total words including front/back matter:** ${totalWords}`,
    `**Total manuscript body words:** ${totalBodyWords}`,
    '',
    '## Notes',
    '',
    '- Total words include chapter metadata, canon sources, continuity notes, revision notes, and included reader-facing front/back matter.',
    '- Manuscript body words count only text after `## Manuscript` and before continuity/revision notes.',
    '- Use manuscript body words for draft-length tracking.',
    '- This report is generated from chapter files in lexical chapter order.',
    '- Book 2 teaser back matter is included when `novel/manuscript/back-matter/book-2-teaser.md` exists.',
    '',
  ].join('\n');

  fs.writeFileSync(
    path.join(exportsDir, 'lantern-protocol-novel-report.md'),
    report,
    'utf8',
  );

  const missingChapters = [];
  for (let i = 1; i <= expectedChapterCount; i += 1) {
    if (!chapters.some((chapter) => chapter.number === i)) missingChapters.push(i);
  }

  const duplicateLongLines = findDuplicateLongLines(chapters);
  const chapterAuditRows = chapters.map((chapter) => {
    const warnings = auditChapter(chapter);
    return `| ${chapter.number} | ${escapeTable(chapter.title)} | ${chapter.bodyWords} | ${warnings.length ? escapeTable(warnings.join(' / ')) : 'OK'} |`;
  });

  const termRows = continuityTerms.map((term) => {
    const appearances = chapters
      .filter((chapter) => chapter.content.includes(term))
      .map((chapter) => chapter.number);
    return `| ${escapeTable(term)} | ${appearances.length} | ${appearances.length ? appearances.join(', ') : '—'} |`;
  });

  const doctrineRows = coreDoctrine.map((line) => {
    const appearances = chapters
      .filter((chapter) => chapter.content.includes(line))
      .map((chapter) => chapter.number);
    return `| ${escapeTable(line)} | ${appearances.length} | ${appearances.length ? appearances.join(', ') : '—'} |`;
  });

  const frontBackMatterAudit = [
    `- Title page / ElevenLabs hook: ${titlePageScript ? 'included' : 'missing'}`,
    `- Preface: ${preface ? 'included' : 'missing'}`,
    `- Book 2 teaser: ${bookTwoTeaser ? 'included' : 'missing'}`,
    `- Book 2 teaser bridge line present: ${bookTwoTeaser?.includes('Someone in the chain agreed.') ? 'yes' : 'no'}`,
  ];

  const audit = [
    '# Lantern Protocol — Continuity Audit',
    '',
    `Generated from ${chapters.length} chapter files.`,
    '',
    '## Assembly Gate',
    '',
    `- Expected chapters: ${expectedChapterCount}`,
    `- Found chapters: ${chapters.length}`,
    `- Missing chapters: ${missingChapters.length ? missingChapters.join(', ') : 'none'}`,
    `- Total manuscript body words: ${totalBodyWords}`,
    '',
    '## Front / Back Matter Gate',
    '',
    ...frontBackMatterAudit,
    '',
    '## Chapter Audit',
    '',
    '| Chapter | Title | Body Words | Audit |',
    '|---:|---|---:|---|',
    ...chapterAuditRows,
    '',
    '## Core Doctrine Trace',
    '',
    '| Doctrine Line | Occurrences | Chapters |',
    '|---|---:|---|',
    ...doctrineRows,
    '',
    '## Continuity Term Trace',
    '',
    '| Term | Occurrences by Chapter Count | Chapters |',
    '|---|---:|---|',
    ...termRows,
    '',
    '## Duplicate Long-Line Scan',
    '',
    duplicateLongLines.length
      ? duplicateLongLines.slice(0, 50).map((group, index) => [`### Duplicate ${index + 1}`, '', ...group.map((line) => `- ${line}`), ''].join('\n')).join('\n')
      : 'No duplicate long manuscript lines found.',
    '',
    '## Editorial Readout Checklist',
    '',
    '- [ ] Confirm Chapter 16 owns the emotional schism and Chapter 17 owns operational fallout.',
    '- [ ] Confirm HarborHands / Leah / Mateo continuity flows cleanly through Chapters 18-24.',
    '- [ ] Confirm Gloria Reyes appears only as burden-zone witness in the finale movement.',
    '- [ ] Confirm Lantern remains faceless and non-POV.',
    '- [ ] Confirm no chapter resolves the moral conflict too cleanly.',
    '- [ ] Confirm Book I ending resolves Bound Flame while opening Book II through the unmapped civic mirror.',
    '- [ ] Confirm Book 2 teaser back matter is present in the assembled export before ElevenLabs/KDP packaging.',
    '',
  ].join('\n');

  fs.writeFileSync(
    path.join(exportsDir, 'lantern-protocol-continuity-audit.md'),
    audit,
    'utf8',
  );

  console.log(`Assembled ${chapters.length} chapters.`);
  console.log(`Total words including front/back matter: ${totalWords}`);
  console.log(`Manuscript body words: ${totalBodyWords}`);
  console.log(`Front/back matter: title=${titlePageScript ? 'yes' : 'no'}, preface=${preface ? 'yes' : 'no'}, book2Teaser=${bookTwoTeaser ? 'yes' : 'no'}`);
  console.log(`Audit warnings: ${chapters.reduce((sum, chapter) => sum + auditChapter(chapter).length, 0)}`);
}

main();