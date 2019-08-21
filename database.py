import sqlite3

# Represent one row in items table
class Item:
    def __init__(self, title, url, category, is_tweeted = False, id = None):
        self.id = id
        self.title = title
        self.url = url
        self.category = category
        self.is_tweeted = is_tweeted

# Setup and initialize database connection
def init(database_file = "items.db"):
    db_conn = sqlite3.connect(database_file)
    # Create table if not exists
    c = db_conn.cursor()
    c.execute(
    """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            inserted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            is_tweeted BOOLEAN DEFAULT FALSE,
            tweeted_at DATETIME
        )
    """
    )
    db_conn.commit()
    c.close()
    return db_conn


# It will raise sqlite3.IntegrityError if url is already exists
def insert_item(db_conn, title, url, category) -> None:
    # Insert new link to the database
    c = db_conn.cursor()
    c.execute(
    """
        INSERT INTO items(title, url, category)
        VALUES ('{}', '{}', '{}')
    """.format(title, url, category)
    )
    db_conn.commit()
    c.close()

# Get untweeted python story
def get_untweeted_python_item(db_conn) -> Item:
    c = db_conn.cursor()
    c.execute(
    """
        SELECT
            id, title, url, category
        FROM
            items
        WHERE
            category='python' AND is_tweeted=0
        ORDER BY
            inserted_at ASC
    """
    )
    result = c.fetchone()
    c.close()

    item = Item(
        id=result[0],
        title=result[1],
        url=result[2],
        category=result[3]
    )

    return item

