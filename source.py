"""
Hacker News API

Doc: https://github.com/HackerNews/API
"""
import json
import re
from typing import List, Optional

import requests

# A list of python related keywords
PYTHON_KEYWORDS = [
    "python",
    "numpy",
    "flask",
    "django",
    "pytorch",
    "tensorflow",
    "scipy",
    "spacy",
    "cpython",
    "pycon",
]

# A list of machine learning related keywords
ML_KEYWORDS = [
    "machine learning",
    "deep learning",
    "neural network",
    "nlp",
    "cnn",
    "lstm",
    "tensorflow",
    "pytorch",
    "rnn",
    "adversarial training",
    "keras",
    "torch",
    "theano",
    "chainer",
]

# A list of rust related keywords
RUST_KEYWORDS = ["rust"]

# A list of rust related keywords
JS_KEYWORDS = ["javascript", "react", "typescript"]


class Story:
    def __init__(
        self, url: Optional[str], title: Optional[str], score: Optional[float]
    ) -> None:
        self.url = url
        self.title = title
        self.score = score

    def as_dict(self):
        return {"url": self.url, "title": self.title, "score": self.score}

    def normalize_title(self) -> str:
        if self.title is None:
            return ""
        lowercase = self.title.lower()
        # Remove non-alpha character
        normalized = re.sub(r"[^a-z]", " ", lowercase)
        return normalized

    def __str__(self):
        return json.dumps(self.as_dict())

    def __repr__(self):
        return json.dumps(self.as_dict())


# Given item_id, get the story detail from hacker news API.
# If item is not story then returns None
def get_story_from_hn(item_id) -> Optional[Story]:
    item_endpoint = (
        "https://hacker-news.firebaseio.com/v0/item/{}.json"
    ).format(item_id)
    resp = requests.get(item_endpoint)
    item = resp.json()
    if item is None:
        return None

    # Check wether item is story, if not then returns None
    if item.get("type", None) != "story":
        return None

    # Parse story
    story = Story(
        url=item.get("url", None),
        title=item.get("title", None),
        score=item.get("score", None),
    )

    return story


# Generate bigrams from list of unigrams
def get_bigram(unigrams: List[str]) -> List[str]:
    unigram_size = len(unigrams)
    current_i = 0
    next_i = current_i + 1
    bigrams = []
    while next_i < unigram_size:
        bigram = "{} {}".format(unigrams[current_i], unigrams[next_i])
        current_i += 1
        next_i = current_i + 1
        bigrams.append(bigram)
    return bigrams


def is_keywords_exists(text: str, keywords: List[str]) -> bool:
    # If keywords is empty, returns True for all story
    if len(keywords) == 0:
        return True

    unigrams = text.strip().split()
    bigrams = get_bigram(unigrams)
    unigrams_set = set(unigrams)
    bigrams_set = set(bigrams)
    for keyword in keywords:
        # Check the keyword
        if keyword in unigrams_set or keyword in bigrams_set:
            return True
    return False


# Get specified stories based on the keywords from Hacker News
# https://news.ycombinator.com/newest
def get_stories_from_hn(keywords: List[str], min_score=2) -> List[Story]:
    # Get new story ids
    resp = requests.get(
        "https://hacker-news.firebaseio.com/v0/newstories.json"
    )
    item_ids = resp.json()
    if item_ids is None:
        return []
    stories = []
    for item_id in item_ids:
        story = get_story_from_hn(item_id)
        # Filter out stories
        if story is None:
            continue
        if story.url is None or story.title is None or story.score is None:
            continue
        # Skip story if below minimal score
        if story.score < min_score:
            continue
        # Replace Show HN: if any
        story.title = story.title.replace("Show HN: ", "")
        if is_keywords_exists(story.normalize_title(), keywords=keywords):
            stories.append(story)
        else:
            continue

    # Sort stories by score
    sorted_stories = sorted(
        stories, key=lambda story: story.score, reverse=True
    )
    return sorted_stories


# Get specified stories based on the keywords from Lobsters
# https://lobste.rs/newest
def get_stories_from_lobsters(keywords: List[str], min_score=2) -> List[Story]:

    # Get stories
    resp = requests.get("https://lobste.rs/newest.json")
    raw_stories = resp.json()
    stories = []
    for raw_story in raw_stories:
        story = Story(
            url=raw_story.get("url", None),
            title=raw_story.get("title", None),
            score=raw_story.get("score", None),
        )
        # Skip if required field is None
        if story.url is None or story.title is None or story.score is None:
            continue
        # Skip story if below minimal score
        if story.score < min_score:
            continue
        if is_keywords_exists(story.normalize_title(), keywords=keywords):
            stories.append(story)
        else:
            continue
    # Sort stories by score
    sorted_stories = sorted(
        stories, key=lambda story: story.score, reverse=True
    )
    return sorted_stories


def get_python_stories_from_hn() -> List[Story]:
    return get_stories_from_hn(keywords=PYTHON_KEYWORDS)


def get_python_stories_from_lobsters() -> List[Story]:
    return get_stories_from_lobsters(keywords=PYTHON_KEYWORDS)


def get_ml_stories_from_hn() -> List[Story]:
    return get_stories_from_hn(keywords=ML_KEYWORDS)


def get_ml_stories_from_lobsters() -> List[Story]:
    return get_stories_from_lobsters(keywords=ML_KEYWORDS)


def get_rust_stories_from_hn() -> List[Story]:
    return get_stories_from_hn(keywords=RUST_KEYWORDS)


def get_rust_stories_from_lobsters() -> List[Story]:
    return get_stories_from_lobsters(keywords=RUST_KEYWORDS)
