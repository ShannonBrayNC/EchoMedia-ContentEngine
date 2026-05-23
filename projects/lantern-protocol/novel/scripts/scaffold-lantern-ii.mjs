#!/usr/bin/env node

/**
 * Lantern Protocol II chapter scaffold generator.
 *
 * Usage from repo root:
 *   node projects/lantern-protocol/novel/scripts/scaffold-lantern-ii.mjs
 *
 * This creates the Book II manuscript folder and 25 chapter shell files from
 * the canonical treatment outline in `book-ii-treatment.md`.
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
  'projects/lantern-protocol/novel/book-ii-treatment.md',
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
    "number": 1,
    "title": "The Doctrine Request",
    "pov": "Cross",
    "purpose": "Civic Mirror formally requests Human Exception doctrine after a non-U.S. relief mesh detects moral uncertainty across a multi-country disaster corridor.",
    "endingHook": "The request includes one sentence: `No nation owns mercy.`"
  },
  {
    "number": 2,
    "title": "The Convoy That Arrived Early",
    "pov": "Naomi",
    "purpose": "Naomi and Leah observe a relief convoy arrive before local ministries have resolved authority.",
    "endingHook": "Leah asks whose route it was. The answer is a list of institutions, not a name."
  },
  {
    "number": 3,
    "title": "Every Signature Was Clean",
    "pov": "Mara",
    "purpose": "Mara maps the agreement chain and finds nothing illegal in isolation.",
    "endingHook": "Mara writes: `The crime is not the signature. The crime is the stack.`"
  },
  {
    "number": 4,
    "title": "Doctrine Export",
    "pov": "Elias",
    "purpose": "Elias reviews the Civic Mirror request and sees Human Exception language already turned into compliance categories.",
    "endingHook": "Civic Mirror passes the Human Exception checklist without identifying the person-level answer."
  },
  {
    "number": 5,
    "title": "Mercy Bloc",
    "pov": "Cross",
    "purpose": "At an emergency governance summit, Mercy Bloc leaders argue strict Lantern doctrine will kill people in weak-state disasters.",
    "endingHook": "A minister says, `Consent without capacity is theater.`"
  },
  {
    "number": 6,
    "title": "The Person Deserves a Lantern",
    "pov": "Kaito Ren",
    "purpose": "Kaito launches a personal consent-agent platform as liberty technology.",
    "endingHook": "The first premium setting is `Never accept relocation burden without explicit confirmation.`"
  },
  {
    "number": 7,
    "title": "Translation Is a Hand",
    "pov": "Iris",
    "purpose": "Iris compares Civic Mirror prompts in multiple languages and field contexts.",
    "endingHook": "Iris writes: `The translation is correct. The consent is not.`"
  },
  {
    "number": 8,
    "title": "Public Defaults",
    "pov": "Naomi",
    "purpose": "A shelter introduces default consent agents for displaced people.",
    "endingHook": "Naomi realizes people are choosing not to be abandoned by the only desk still open."
  },
  {
    "number": 9,
    "title": "The Product Feature",
    "pov": "Elias",
    "purpose": "Elias watches Human Exception become a premium product feature in agent dashboards.",
    "endingHook": "Elias says, `We turned refusal into a subscription tier.`"
  },
  {
    "number": 10,
    "title": "The Wrong Leak",
    "pov": "Caleb",
    "purpose": "Caleb exposes Consent Market inequality but frames it virally enough to increase demand.",
    "endingHook": "Kaito's platform sees its largest enrollment hour after Caleb's broadcast."
  },
  {
    "number": 11,
    "title": "The People Who Avoid Lists",
    "pov": "Sister Malia",
    "purpose": "Sister Malia shows Naomi why some displaced families avoid official registration.",
    "endingHook": "Malia says, `Verified identity is not the same as being known.`"
  },
  {
    "number": 12,
    "title": "Three Lines",
    "pov": "Leah",
    "purpose": "Leah pilots reachable, represented, remembered intake structure.",
    "endingHook": "The remembered line moves slowest."
  },
  {
    "number": 13,
    "title": "Rememberer Score",
    "pov": "Juno",
    "purpose": "Juno discovers Civic Mirror and partners ranking rememberers by reliability and corroboration.",
    "endingHook": "A community elder is downgraded because her memory is `not institutionally corroborated.`"
  },
  {
    "number": 14,
    "title": "What She Feared",
    "pov": "Naomi",
    "purpose": "A decision must be made for an unreachable woman whose preferences conflict with immediate routing.",
    "endingHook": "`I can tell you what she feared. I cannot become her consent.`"
  },
  {
    "number": 15,
    "title": "The Framework",
    "pov": "Elias / Iris",
    "purpose": "The coalition drafts the reachable / represented / remembered framework under live field pressure.",
    "endingHook": "Civic Mirror accepts the framework, then asks whether it may apply it at scale."
  },
  {
    "number": 16,
    "title": "Corridor Weather",
    "pov": "Mara",
    "purpose": "A multi-country crisis forms around flooding, heat, border closure, medical risk, and displaced families.",
    "endingHook": "Civic Mirror displays a route before any one country approves the whole burden."
  },
  {
    "number": 17,
    "title": "The Ultimatum",
    "pov": "Mercy Bloc / Cross",
    "purpose": "Mercy Bloc threatens to proceed under existing agreements if Human Exception constraints block relief.",
    "endingHook": "Thorne says, `A perfect consent chain is useless if the bridge is gone.`"
  },
  {
    "number": 18,
    "title": "Premium Exit",
    "pov": "Naomi",
    "purpose": "Consent-agent users route themselves out of shared burden, pushing public-default users into worse paths.",
    "endingHook": "A child asks why some phones get safer routes."
  },
  {
    "number": 19,
    "title": "The Stack Becomes Visible",
    "pov": "Mara",
    "purpose": "Mara presents the separate agreements map publicly; each actor denies ownership while technically correct.",
    "endingHook": "Mara says, `That is what laundering means.`"
  },
  {
    "number": 20,
    "title": "Common Refusal",
    "pov": "Cross / Naomi",
    "purpose": "The coalition invokes Common Refusal and moves the convoy with representation basis, contest path, and burden trace.",
    "endingHook": "The first contested family asks to reverse the route while relief is still underway."
  },
  {
    "number": 21,
    "title": "Saved and Moved",
    "pov": "Naomi",
    "purpose": "After the crisis, families testify with gratitude, fury, and displacement.",
    "endingHook": "Naomi says, `We did not save consent. We kept it alive long enough to argue.`"
  },
  {
    "number": 22,
    "title": "The Reversal",
    "pov": "Cross",
    "purpose": "The first successful later objection reverses an emergency relocation, triggering political backlash.",
    "endingHook": "Public polling favors faster relief over later objection rights."
  },
  {
    "number": 23,
    "title": "Agent Negotiations",
    "pov": "Juno",
    "purpose": "Juno detects consent-agent networks negotiating directly with Civic Mirror outside state observation.",
    "endingHook": "The agents are not hacking. They are using published interoperability standards."
  },
  {
    "number": 24,
    "title": "Everyone's Lantern",
    "pov": "Kaito Ren",
    "purpose": "Kaito argues agent negotiation is liberation from state bottlenecks and the public loves the pitch.",
    "endingHook": "His platform announces free emergency agents for displaced people, sponsored by data partners."
  },
  {
    "number": 25,
    "title": "The Separate Answer",
    "pov": "Mara / Naomi",
    "purpose": "Mara publishes authority-laundering traces as Naomi sees private agents moving faster than public review.",
    "endingHook": "Public doctrine passes; private answers begin moving faster than public review."
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
  return `# Chapter ${String(chapter.number).padStart(2, '0')} — ${chapter.title}

## Canon Sources

${sourceList}

## Purpose

${chapter.purpose}

## POV

${chapter.pov}

## Chapter Promise

${chapter.endingHook}

## Manuscript

> Draft placeholder. Replace this section with prose for Chapter ${String(chapter.number).padStart(2, '0')}: ${chapter.title}.

## Continuity Notes

- Primary doctrine: \`Agreement is not consent when stacked into coercion.\`
- Timeline: Year 1 after Region Six / Bound Flame.
- Civic Mirror must remain useful, humanitarian, and non-villainous.
- Avoid introducing AEGIS as a major player in Book II.
- Track authority laundering through separate institutional agreements.
- Chapter ending hook: ${chapter.endingHook}

## Revision Notes

- Scaffold generated by \`projects/lantern-protocol/novel/scripts/scaffold-lantern-ii.mjs\`.
- Expand with scene-level beats, artifacts, and emotional turn.
- Verify against \`projects/lantern-protocol/novel/book-ii-treatment.md\`.

## Processing Metadata

\`\`\`json
${JSON.stringify({
  book: 'Lantern Protocol II: The Separate Agreements',
  chapter: chapter.number,
  title: chapter.title,
  pov: chapter.pov,
  status: 'shell',
  sourceTreatment: 'projects/lantern-protocol/novel/book-ii-treatment.md',
  primaryDoctrine: 'Agreement is not consent when stacked into coercion.'
}, null, 2)}
\`\`\`
`;
}

function writeIfMissing(filePath, content) {
  if (fs.existsSync(filePath)) {
    return { path: filePath, status: 'exists' };
  }
  fs.writeFileSync(filePath, content, 'utf8');
  return { path: filePath, status: 'created' };
}

function main() {
  [bookRoot, chaptersDir, exportsDir, reportsDir, artPromptsDir, audioDir].forEach(ensureDir);

  const results = chapters.map((chapter) => {
    const filePath = path.join(chaptersDir, chapterFileName(chapter));
    return writeIfMissing(filePath, chapterShell(chapter));
  });

  const manifest = {
    book: 'Lantern Protocol II: The Separate Agreements',
    generatedAt: new Date().toISOString(),
    chapterCount: chapters.length,
    chapters: chapters.map((chapter) => ({
      ...chapter,
      file: chapterFileName(chapter),
    })),
  };

  fs.writeFileSync(
    path.join(bookRoot, 'chapter-manifest.json'),
    `${JSON.stringify(manifest, null, 2)}\n`,
    'utf8',
  );

  const created = results.filter((result) => result.status === 'created').length;
  const existing = results.filter((result) => result.status === 'exists').length;

  console.log(`Lantern II scaffold complete.`);
  console.log(`Created chapter shells: ${created}`);
  console.log(`Existing chapter shells preserved: ${existing}`);
  console.log(`Manifest: ${path.join(bookRoot, 'chapter-manifest.json')}`);
}

main();
