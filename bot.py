import sqlite3

import tweepy
from apscheduler.schedulers.blocking import BlockingScheduler

import config
import database
import source

scheduler = BlockingScheduler()


@scheduler.scheduled_job("interval", minutes=20)
def collect_python_stories_from_hn():
    print("[python][hn] Collecting the python stories from hacker news ...")

    # Initialize database
    db_conn = database.init(config.DATABASE_FILE)

    # Get python stories from hacker news
    stories = source.get_python_stories_from_hn()
    for story in stories:
        # Insert story to the database
        try:
            database.insert_item(db_conn, story.title, story.url, "python")
            print("[python][hn] Item {} inserted".format(story.url))
        except sqlite3.IntegrityError:
            print("[python][hn] Item {} already exists".format(story.url))
        except Exception as e:
            print("[python][hn] Insert item {} failed {}".format(story.url, e))

    # Close the database connection
    db_conn.close()


@scheduler.scheduled_job("interval", minutes=5)
def collect_python_stories_from_lobsters():
    print("[python][lobsters] Collecting the python stories from lobsters ...")

    # Initialize database
    db_conn = database.init(config.DATABASE_FILE)

    # Get python stories from lobsters
    stories = source.get_python_stories_from_lobsters()
    for story in stories:
        # Insert story to the database
        try:
            database.insert_item(db_conn, story.title, story.url, "python")
            print("[python][lobsters] Item {} inserted".format(story.url))
        except sqlite3.IntegrityError:
            print(
                "[python][lobsters] Item {} already exists".format(story.url)
            )
        except Exception as e:
            print(
                "[python][lobsters] Insert item {} failed {}".format(
                    story.url, e
                )
            )

    # Close the database connection
    db_conn.close()


@scheduler.scheduled_job("interval", minutes=20)
def collect_ml_stories_from_hn():
    print("[ml][hn] Collecting the ml stories from hacker news ...")

    # Initialize database
    db_conn = database.init(config.DATABASE_FILE)

    # Get ml stories from hacker news
    stories = source.get_ml_stories_from_hn()
    for story in stories:
        # Insert story to the database
        try:
            database.insert_item(db_conn, story.title, story.url, "ml")
            print("[ml][hn] Item {} inserted".format(story.url))
        except sqlite3.IntegrityError:
            print("[ml][hn] Item {} already exists".format(story.url))
        except Exception as e:
            print("[ml][hn] Insert item {} failed {}".format(story.url, e))

    # Close the database connection
    db_conn.close()


@scheduler.scheduled_job("interval", minutes=5)
def collect_ml_stories_from_lobsters():
    print("[ml][lobsters] Collecting the ml stories from lobsters ...")

    # Initialize database
    db_conn = database.init(config.DATABASE_FILE)

    # Get ml stories from lobsters
    stories = source.get_ml_stories_from_lobsters()
    for story in stories:
        # Insert story to the database
        try:
            database.insert_item(db_conn, story.title, story.url, "ml")
            print("[ml][lobsters] Item {} inserted".format(story.url))
        except sqlite3.IntegrityError:
            print("[ml][lobsters] Item {} already exists".format(story.url))
        except Exception as e:
            print(
                "[ml][lobsters] Insert item {} failed {}".format(story.url, e)
            )

    # Close the database connection
    db_conn.close()


@scheduler.scheduled_job("interval", minutes=20)
def collect_rust_stories_from_hn():
    print("[rust][hn] Collecting the rust stories from hacker news ...")

    # Initialize database
    db_conn = database.init(config.DATABASE_FILE)

    # Get rust stories from hacker news
    stories = source.get_rust_stories_from_hn()
    for story in stories:
        # Insert story to the database
        try:
            database.insert_item(db_conn, story.title, story.url, "rust")
            print("[rust][hn] Item {} inserted".format(story.url))
        except sqlite3.IntegrityError:
            print("[rust][hn] Item {} already exists".format(story.url))
        except Exception as e:
            print("[rust][hn] Insert item {} failed {}".format(story.url, e))

    # Close the database connection
    db_conn.close()


@scheduler.scheduled_job("interval", minutes=5)
def collect_rust_stories_from_lobsters():
    print("[rust][lobsters] Collecting the rust stories from lobsters ...")

    # Initialize database
    db_conn = database.init(config.DATABASE_FILE)

    # Get rust stories from lobsters
    stories = source.get_rust_stories_from_lobsters()
    for story in stories:
        # Insert story to the database
        try:
            database.insert_item(db_conn, story.title, story.url, "rust")
            print("[rust][lobsters] Item {} inserted".format(story.url))
        except sqlite3.IntegrityError:
            print("[rust][lobsters] Item {} already exists".format(story.url))
        except Exception as e:
            print(
                "[rust][lobsters] Insert item {} failed {}".format(
                    story.url, e
                )
            )

    # Close the database connection
    db_conn.close()


@scheduler.scheduled_job("cron", hour="*")
def tweet_python():
    print("[python] Tweeting ...")
    # Initialize database
    db_conn = database.init(config.DATABASE_FILE)

    # Initialize twitter client
    auth = tweepy.OAuthHandler(
        config.PYTHON_CONSUMER_KEY, config.PYTHON_CONSUMER_SECRET
    )
    auth.set_access_token(
        config.PYTHON_ACCESS_TOKEN, config.PYTHON_ACCESS_TOKEN_SECRET
    )
    twitter = tweepy.API(auth)

    # Get the tweet data
    print("[python] Get the tweet data")
    item = database.get_untweeted_item(db_conn, "python")
    if item is None:
        print("[python] The tweet data is None")
        db_conn.close()
        return

    # Tweet the status
    status = "{} {} #python".format(item.title, item.url)
    twitter.update_status(status=status)

    # Mark item as tweeted
    database.mark_item_as_tweeted(db_conn, item.id)
    print("[python] Tweeted {}".format(item.url))

    # Close database conn
    db_conn.close()


@scheduler.scheduled_job("cron", hour="*")
def tweet_rust():
    print("[rust] Tweeting ...")
    # Initialize database
    db_conn = database.init(config.DATABASE_FILE)

    # Initialize twitter client
    auth = tweepy.OAuthHandler(
        config.RUST_CONSUMER_KEY, config.RUST_CONSUMER_SECRET
    )
    auth.set_access_token(
        config.RUST_ACCESS_TOKEN, config.RUST_ACCESS_TOKEN_SECRET
    )
    twitter = tweepy.API(auth)

    # Get the tweet data
    print("[rust] Get the tweet data")
    item = database.get_untweeted_item(db_conn, "rust")
    if item is None:
        print("[rust] The tweet data is None")
        db_conn.close()
        return

    # Tweet the status
    status = "{} {} #rustlang".format(item.title, item.url)
    twitter.update_status(status=status)

    # Mark item as tweeted
    database.mark_item_as_tweeted(db_conn, item.id)
    print("[rust] Tweeted {}".format(item.url))

    # Close database conn
    db_conn.close()


if __name__ == "__main__":
    # Double check config
    if (
        config.PYTHON_ACCESS_TOKEN is None
        or config.PYTHON_ACCESS_TOKEN_SECRET is None
        or config.PYTHON_CONSUMER_KEY is None
        or config.PYTHON_CONSUMER_SECRET is None
        or config.DATABASE_FILE is None
        or config.RUST_ACCESS_TOKEN is None
        or config.RUST_ACCESS_TOKEN_SECRET is None
        or config.RUST_CONSUMER_KEY is None
        or config.RUST_CONSUMER_SECRET is None
    ):
        raise ValueError("Configuration should be set")

    # Start the scheduler
    print("Bot started ...")
    scheduler.start()
