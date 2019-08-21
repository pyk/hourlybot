import requests

# If the title of the link contains the one of the
# following keywords then insert the link to the database
WHITELIST_KEYWORDS = [
    "python",
    "numpy",
    "flask",
    "django",
    "pytorch",
    "tensorflow",
    "scipy",
    "spacy"
]

# If the tags of the link contains the one of the
# following keywords then do not insert the link to
# the database
BLACKLIST_TAGS = [
    "c",
    "javascript",
    "lua",
    "julia",
    "lisp"
]

class LobsterLink:
    def __init__(self, short_id, url):
        self.short_id = short_id
        self.url = url

# Collect the most recent link from https://lobste.rs/t/python.json
def get_recent_link() -> LobsterLink:
    # Perform HTTP request
    resp = requests.get("https://lobste.rs/t/python.json")
    data = resp.json()

    # Get recent link
    raw_lobster_link = data[0]
    lobster_link = LobsterLink(
        short_id=raw_lobster_link["short_id"],
        url=raw_lobster_link["url`"],
        upvotes=
        # TODO: continue here
    )
    pass


