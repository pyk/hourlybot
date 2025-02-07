from os import environ as env

DATABASE_FILE = env.get("DATABASE_FILE", None)

PYTHON_CONSUMER_KEY = env.get("PYTHON_CONSUMER_KEY", None)
PYTHON_CONSUMER_SECRET = env.get("PYTHON_CONSUMER_SECRET", None)
PYTHON_ACCESS_TOKEN = env.get("PYTHON_ACCESS_TOKEN", None)
PYTHON_ACCESS_TOKEN_SECRET = env.get("PYTHON_ACCESS_TOKEN_SECRET", None)

RUST_CONSUMER_KEY = env.get("RUST_CONSUMER_KEY", None)
RUST_CONSUMER_SECRET = env.get("RUST_CONSUMER_SECRET", None)
RUST_ACCESS_TOKEN = env.get("RUST_ACCESS_TOKEN", None)
RUST_ACCESS_TOKEN_SECRET = env.get("RUST_ACCESS_TOKEN_SECRET", None)
