import unittest
from scripts.generate_content_artifacts import (
    DEFAULT_BRANCH_ORDER,
    SourceFile,
    classify_role,
    is_candidate_text_file,
    slugify,
    sort_source_files,
)


class GeneratorUnitTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify('Chapter 01: The Test!'), 'chapter-01-the-test')

    def test_classify_role(self):
        self.assertEqual(classify_role('projects/lantern-protocol/visual-bible/character-image-prompts.md'), 'character_prompts')
        self.assertEqual(classify_role('projects/lantern-protocol/pitch/pitch-deck.md'), 'pitch')
        self.assertEqual(classify_role('projects/lantern-protocol/storyboards/chapters/ch1.md'), 'storyboard')

    def test_candidate_filter(self):
        self.assertTrue(is_candidate_text_file('projects/lantern-protocol/pitch/pitch-deck.md', include_archive=False))
        self.assertFalse(is_candidate_text_file('projects/lantern-protocol/_generated/artifact-index.md', include_archive=False))
        self.assertFalse(is_candidate_text_file('projects/lantern-protocol/pitch/pitch-deck.png', include_archive=False))
        self.assertFalse(is_candidate_text_file('_archive/lantern-protocol-v0-novel/05-artifacts/a.md', include_archive=False))
        self.assertTrue(is_candidate_text_file('_archive/lantern-protocol-v0-novel/05-artifacts/a.md', include_archive=True))

    def test_sort_source_files(self):
        items = [
            SourceFile('b', 'main', 'x.md', 'chapter', '2', 1),
            SourceFile('a', 'work', 'y.md', 'chapter', '1', 1),
        ]
        sorted_items = sort_source_files(items)
        self.assertEqual([x.logical_id for x in sorted_items], ['a', 'b'])

    def test_branch_order_priority(self):
        branches = ['work', 'main', 'cleanup/lantern-canon-freeze-v2']
        ordered = [b for b in DEFAULT_BRANCH_ORDER if b in branches] + [b for b in branches if b not in DEFAULT_BRANCH_ORDER]
        self.assertEqual(ordered[0], 'cleanup/lantern-canon-freeze-v2')


if __name__ == '__main__':
    unittest.main()
