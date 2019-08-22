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


# Get specified stories based on the keywords from Hacker News
# https://news.ycombinator.com/newest
def get_stories_from_hn(keywords=None, min_score=2) -> List[Story]:
    # Check wether the story is OK to append the list
    def is_ok(story):
        # If keywords is None or empty, returns True for all story
        if keywords is None or len(keywords) == 0:
            return True
        for keyword in keywords:
            if keyword in story.normalize_title():
                return True
        return False

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
        if is_ok(story):
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
def get_stories_from_lobsters(keywords=None, min_score=2) -> List[Story]:
    # Check wether the story is OK to append the list
    def is_ok(story):
        # If keywords is None or empty, returns True for all story
        if keywords is None or len(keywords) == 0:
            return True
        for keyword in keywords:
            if keyword in story.normalize_title():
                return True
        return False

    # Get stories
    resp = requests.get("https://lobste.rs/newest.json")
    stories = resp.json()
    stories = []
    for raw_story in stories:
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
        if is_ok(story):
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
