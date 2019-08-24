import unittest
import source
from source import Story


class TestStory(unittest.TestCase):
    def test_title(self):
        story = Story(url="test", title="Why: Clojure?", score=8.0)
        self.assertEqual(story.normalize_title(), "why  clojure ")


class TestSource(unittest.TestCase):
    def test_get_bigram(self) -> None:
        unigrams = ["a", "b", "c", "d"]
        bigrams = source.get_bigram(unigrams)
        self.assertEqual(bigrams, ["a b", "b c", "c d"])

    def test_is_keywords_exists(self) -> None:
        title1 = "get started with rust"
        self.assertTrue(source.is_keywords_exists(title1, keywords=["rust"]))
        title2 = "rust in a nutshell"
        self.assertTrue(source.is_keywords_exists(title2, keywords=["rust"]))
        title3 = "a rust library open source"
        self.assertTrue(source.is_keywords_exists(title3, keywords=["rust"]))
        title4 = "trust in a nutshell"
        self.assertFalse(source.is_keywords_exists(title4, keywords=["rust"]))
        title5 = "let's get started"
        self.assertTrue(source.is_keywords_exists(title5, keywords=[]))
        title5 = "let's get started with machine learning"
        self.assertTrue(
            source.is_keywords_exists(title5, keywords=["machine learning"])
        )


if __name__ == "__main__":
    unittest.main()
