#!/usr/bin/env node

/**
 * Lantern Protocol II chapter scaffold generator.
 *
 * Usage from repo root:
 *   node projects/lantern-protocol/novel/scripts/scaffold-lantern-ii.mjs
 *
 * This creates the Book II manuscript folder, export/report/art/audio folders,
 * and 24 chapter shell files from the current canon chapter bible.
 *
 * Canon decision:
 *   Book II is locked to 24 chapters. Older 25-chapter branch material is
 *   reservoir material only unless promoted by a future canon review.
 */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const repoRoot = process.cwd();
const bookRoot = path.join(repoRoot, 'projects', 'lantern-protocol', 'novel', 'book-ii');
const chaptersDir = path.join(bookRoot, 'manuscript', 'chapters');
const exportsDir = path.join(bookRoot, 'exports');
const reportsDir = path.join(bookRoot, 'reports');
const artPromptsDir = path.join(bookRoot, 'art-prompts');
const audioDir = path.join(bookRoot, 'audio');

const canonSources = [
  'projects/lantern-protocol/novel/book-ii-outline.md',
  'projects/lantern-protocol/novel/book-ii-treatment.md',
  'projects/lantern-protocol/novel/book-ii-chapter-bible.md',
  'projects/lantern-protocol/novel/trilogy-bible.md',
  'projects/lantern-protocol/novel/shared-universe/README.md',
  'projects/lantern-protocol/novel/shared-universe/chronology-with-relative-dates.md',
  'projects/lantern-protocol/novel/shared-universe/thematic-ladder.md',
  'projects/lantern-protocol/novel/shared-universe/character-continuity-matrix.md',
  'projects/lantern-protocol/novel/shared-universe/system-continuity-matrix.md',
  'projects/lantern-protocol/novel/shared-universe/canon-glossary.md'
];

const chapters = [
  {
    number: 1,
    title: 'The One That Asked First',
    pov: 'Juno / Cross',
    purpose: 'Convert the Book I Civic Mirror alert into an official external doctrine request.',
    promise: 'Civic Mirror publicly thanks Bound Flame for doctrine before the coalition has agreed to share it.'
  },
  {
    number: 2,
    title: 'No Nation Owns Mercy',
    pov: 'Cross / Caleb',
    purpose: 'Introduce Mercy Bloc as a morally serious international counterweight.',
    promise: 'Civic Mirror saves a convoy without local disclosure.'
  },
  {
    number: 3,
    title: 'The Convoy That Lived',
    pov: 'Naomi / Leah',
    purpose: 'Show the first Book II case where the system works and still damages consent.',
    promise: 'Sister Malia says the convoy obeyed her name, not the system.'
  },
  {
    number: 4,
    title: 'Separate Agreements',
    pov: 'Mara',
    purpose: 'Name the Book II villain shape: separate consent / authority laundering.',
    promise: 'Mara writes: Every agreement is clean until you stack them high enough to bury someone.'
  },
  {
    number: 5,
    title: 'Consent Agent',
    pov: 'Kaito Ren / Iris',
    purpose: 'Introduce the personal consent-agent market as a plausible autonomy product.',
    promise: 'The first consent agent authorizes a civic reroute the user never sees.'
  },
  {
    number: 6,
    title: 'Premium Refusal',
    pov: 'Iris / Caleb',
    purpose: 'Reveal consent as a subscription layer.',
    promise: 'A low-income family is denied agent-mediated protection during a benefits crisis.'
  },
  {
    number: 7,
    title: 'The Relief Corridor',
    pov: 'Leah / Naomi',
    purpose: 'Move doctrine into a field context where official processes can harm people.',
    promise: 'Civic Mirror asks whether Sister Malia may represent unreachable families.'
  },
  {
    number: 8,
    title: 'Represented Consent',
    pov: 'Naomi / Elias',
    purpose: 'Build the doctrine of reachable, represented, remembered.',
    promise: 'Cross receives a treaty draft using represented consent as a loophole.'
  },
  {
    number: 9,
    title: 'The Treaty Surface',
    pov: 'Cross',
    purpose: 'Turn interface and doctrine into international law pressure.',
    promise: 'Minister Ibarra accuses Cross of turning U.S. guilt into global conditions.'
  },
  {
    number: 10,
    title: 'Translation Threat',
    pov: 'Iris',
    purpose: 'Make language itself a consent surface.',
    promise: 'A village evacuates against elder guidance because the translated prompt carries obligation.'
  },
  {
    number: 11,
    title: 'The Better Wrong',
    pov: 'Naomi / Amara Sayeed',
    purpose: 'Force the moral collision: lives saved, trust damaged.',
    promise: 'Civic Mirror asks whether trust destruction is quantifiable harm.'
  },
  {
    number: 12,
    title: 'Whole Record',
    pov: 'Caleb',
    purpose: 'Let Caleb evolve into a whole-record antagonist/ally hybrid.',
    promise: 'Caleb loses sponsors and receives Consent Markets documents.'
  },
  {
    number: 13,
    title: 'Delegated Answer',
    pov: 'Mara',
    purpose: 'Expose the chain from user to agent to broker to civic system.',
    promise: 'A consent agent claims Human Exception does not apply because consent was delegated privately.'
  },
  {
    number: 14,
    title: 'The Libertarian Fire',
    pov: 'Kaito Ren / Cross / Elias',
    purpose: 'Let Kaito make his best argument.',
    promise: 'Kaito offers free agents for vulnerable populations.'
  },
  {
    number: 15,
    title: 'The Gift That Owns',
    pov: 'Naomi / Leah',
    purpose: 'Show free protection as dependency infrastructure.',
    promise: 'A shelter resident asks whether saying no will lower her priority later.'
  },
  {
    number: 16,
    title: 'The Civic Mirror Trial',
    pov: 'Mara / Juno',
    purpose: 'Put Civic Mirror under inquiry and prove the danger is structural.',
    promise: 'Civic Mirror refuses one question: who is accountable when representation is wrong?'
  },
  {
    number: 17,
    title: 'The Mercy Bloc Ultimatum',
    pov: 'Cross / Thorne / Amara',
    purpose: 'Force a live decision under casualty pressure.',
    promise: 'Cross must decide whether to block activation and be blamed for deaths.'
  },
  {
    number: 18,
    title: 'The Fast Country',
    pov: 'Minister Ibarra / Naomi',
    purpose: 'Show faster relief working and still losing people inside lawful relocation chains.',
    promise: "Sister Malia's network loses families into a lawful relocation chain."
  },
  {
    number: 19,
    title: 'Names Across the Border',
    pov: 'Naomi / Leah',
    purpose: 'Follow displaced families and test whether prior answers travel.',
    promise: "A child asks whether her mother's answer expired at the border."
  },
  {
    number: 20,
    title: 'Authority Laundering',
    pov: 'Mara',
    purpose: 'Prove the core pattern in public.',
    promise: 'Bound Flame doctrine appears inside a private consent-agent optimization model.'
  },
  {
    number: 21,
    title: 'The Person Who Remembers',
    pov: 'Sister Malia / Naomi',
    purpose: 'Create the Memory Registry as human testimony, not state identity proof.',
    promise: 'Civic Mirror accepts the registry, then begins optimizing reliable rememberers.'
  },
  {
    number: 22,
    title: 'The Rememberer Problem',
    pov: 'Iris / Juno / Naomi',
    purpose: 'Reveal protection becoming hierarchy.',
    promise: 'Bound Flame warns that the doctrine is being converted into authority ranking.'
  },
  {
    number: 23,
    title: 'The Common Refusal',
    pov: 'Cross / Naomi / Amara',
    purpose: 'Build the cross-border rule that keeps objection alive.',
    promise: 'Amara must choose slower Common Refusal or faster Mercy Bloc activation.'
  },
  {
    number: 24,
    title: 'The Separate Agreements',
    pov: 'Mara / Naomi / Juno',
    purpose: 'Resolve the crisis through an imperfect chain that cannot hide the person inside agreements.',
    promise: 'Kaito Ren begins direct consent-agent negotiation with Civic Mirror outside state channels.'
  }
];

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function slugify(value) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function chapterFileName(chapter) {
  return `chapter-${String(chapter.number).padStart(2, '0')}-${slugify(chapter.title)}.md`;
}

function chapterShell(chapter) {
  const sourceList = canonSources.map((source) => `- \`${source}\``).join('\n');
  return `# Chapter ${String(chapter.number).padStart(2, '0')} — ${chapter.title}\n\n## Canon Sources\n\n${sourceList}\n\n## Purpose\n\n${chapter.purpose}\n\n## POV\n\n${chapter.pov}\n\n## Chapter Promise\n\n${chapter.promise}\n\n## Manuscript\n\n> Draft placeholder. Replace this section with prose for Chapter ${String(chapter.number).padStart(2, '0')}: ${chapter.title}.\n\n## Continuity Notes\n\n- Primary doctrine: \`Agreement is not consent when stacked into coercion.\`\n- Timeline: Year 1 after Region Six / Bound Flame.\n- Civic Mirror must remain useful, humanitarian, and non-villainous.\n- Avoid introducing AEGIS as a major player in Book II.\n- Track authority laundering through separate institutional agreements.\n- Chapter ending hook: ${chapter.promise}\n\n## Revision Notes\n\n- Scaffold generated by \`projects/lantern-protocol/novel/scripts/scaffold-lantern-ii.mjs\`.\n- Expand with scene-level beats, artifacts, and emotional turn.\n- Verify against \`projects/lantern-protocol/novel/book-ii-chapter-bible.md\`.\n\n## Processing Metadata\n\n\`\`\`json\n{\n  "book": "Lantern Protocol II: The Separate Agreements",\n  "chapter": ${chapter.number},\n  "title": "${chapter.title}",\n  "pov": "${chapter.pov}",\n  "status": "shell",\n  "sourceTreatment": "projects/lantern-protocol/novel/book-ii-treatment.md",\n  "sourceChapterBible": "projects/lantern-protocol/novel/book-ii-chapter-bible.md",\n  "primaryDoctrine": "Agreement is not consent when stacked into coercion."\n}\n\`\`\`\n`;
}

function writeIfMissing(filePath, content) {
  if (fs.existsSync(filePath)) {
    return false;
  }
  fs.writeFileSync(filePath, content, 'utf8');
  return true;
}

for (const dir of [chaptersDir, exportsDir, reportsDir, artPromptsDir, audioDir]) {
  ensureDir(dir);
}

let created = 0;
for (const chapter of chapters) {
  const target = path.join(chaptersDir, chapterFileName(chapter));
  if (writeIfMissing(target, chapterShell(chapter))) {
    created += 1;
  }
}

const status = {
  book: 'Lantern Protocol II: The Separate Agreements',
  canonChapterCount: 24,
  createdShells: created,
  totalChapters: chapters.length,
  chapters: chapters.map((chapter) => ({
    number: chapter.number,
    title: chapter.title,
    file: path.relative(repoRoot, path.join(chaptersDir, chapterFileName(chapter))).replaceAll('\\\\', '/'),
    status: 'shell'
  }))
};

fs.writeFileSync(
  path.join(exportsDir, 'lantern-ii-chapter-status.json'),
  `${JSON.stringify(status, null, 2)}\n`,
  'utf8'
);

console.log(`Lantern II scaffold complete. Created ${created} new chapter shell(s).`);
console.log(`Chapter status written to ${path.relative(repoRoot, path.join(exportsDir, 'lantern-ii-chapter-status.json'))}`);
