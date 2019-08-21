"""
Hacker News API

Doc: https://github.com/HackerNews/API
"""
import json
import re
from typing import List, Optional

import requests

# Hacker News API endpoint
TOP_STORIES_ENDPOINT = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_ENDPOINT_FORMAT = "https://hacker-news.firebaseio.com/v0/item/{}.json"


class Story:
    def __init__(
        self,
        url: Optional[str],
        title: Optional[str],
        score: Optional[float]
    ) -> None:
        self.url = url
        self.title = title
        self.score = score

    def as_dict(self):
      return {
          "url": self.url,
          "title": self.title,
          "score": self.score
      }

    def normalize_title(self) -> str:
      lowercase = self.title.lower()
      # Remove non-alpha character
      normalized = re.sub(r"[^a-z]", " ", lowercase)
      return normalized

    def __str__(self):
      return json.dumps(self.as_dict())

    def __repr__(self):
      return json.dumps(self.as_dict())


# Given item_id, get the story detail. If item is not story
# then returns None
def get_story(item_id) -> Optional[Story]:
    item_endpoint = ITEM_ENDPOINT_FORMAT.format(item_id)
    resp = requests.get(item_endpoint)
    item = resp.json()
    # Check wether item is story, if not then returns None
    if item["type"] != "story":
        return None

    # Parse story
    story = Story(
        url=item.get("url", None),
        title=item.get("title", None),
        score=item.get("score", None)
    )

    return story


# Get top stories from Hacker News
def get_top_stories() -> List[Story]:
    # Get top story ids
    resp = requests.get(TOP_STORIES_ENDPOINT)
    item_ids = resp.json()
    stories = []
    for item_id in item_ids:
        story = get_story(item_id)
        # Filter out stories
        if story is None:
            continue
        if (story.url is None or story.title is None or story.score is None):
            continue
        stories.append(story)
    # Sort stories by score
    sorted_stories = sorted(stories, key=lambda story: story.score, reverse=True)
    return sorted_stories


# Returns true if given story is a python related story
def is_python_related_story(story) -> bool:
    keywords = ["python", "numpy", "flask", "django", "pytorch", "tensorflow", "scipy", "spacy"]
    for keyword in keywords:
        if keyword in story.normalize_title():
          return True
    return False


# Get top python related stories
def get_python_top_stories() -> List[Story]:
    top_stories = get_top_stories()
    # Filter out python stories
    python_stories = list(filter(is_python_related_story, top_stories))
    return python_stories


if __name__ == "__main__":
    stories = get_python_top_stories()
    print(stories)
