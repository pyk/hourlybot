import sqlite3

import tweepy
from apscheduler.schedulers.blocking import BlockingScheduler

import config
import database
import hacker_news

scheduler = BlockingScheduler()

@scheduler.scheduled_job("interval", minutes=5)
def collect_python_stories():
    print("[python] Collecting the python stories ...")

    # Initialize database
    db_conn = database.init(config.DATABASE_FILE)

    # Get python stories from hacker news
    hn_python_stories = hacker_news.get_python_top_stories()
    for story in hn_python_stories:
        # Insert story to the database
        try:
            database.insert_item(db_conn, story.title, story.url, story.category)
            print("[python] Item {} inserted".format(item.url))
        except sqlite3.IntegrityError:
            print("[python] Item {} already exists".format(story.url))
        except Exception as e:
            print("[python] Insert item {} failed {}".format(story.url, e))

    # Close the database connection
    db_conn.close()

@scheduler.scheduled_job("cron", hour="*")
def tweet_python():
    print("[python] Tweeting ...")
    # Initialize database
    db_conn = database.init(config.DATABASE_FILE)

    # Initialize twitter client
    auth = tweepy.OAuthHandler(
        config.PYTHON_CONSUMER_KEY,
        config.PYTHON_CONSUMER_SECRET
    )
    auth.set_access_token(
        config.PYTHON_ACCESS_TOKEN,
        config.PYTHON_ACCESS_TOKEN_SECRET
    )
    twitter = tweepy.API(auth)

    # Get the tweet data
    print("[python] Get the tweet data")
    item = database.get_untweeted_python_item(db_conn)
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


if __name__ == "__main__":
    # Double check config
    if (config.PYTHON_ACCESS_TOKEN is None
        or config.PYTHON_ACCESS_TOKEN_SECRET is None
        or config.PYTHON_CONSUMER_KEY is None
        or config.PYTHON_CONSUMER_SECRET is None
        or config.DATABASE_FILE is None):
        raise ValueError("Configuration should be set")

    # Start the scheduler
    print("Bot started ...")
    scheduler.start()
