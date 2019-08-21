import unittest
import database
import sqlite3

class TestDatabase(unittest.TestCase):

    def test_insert_item(self):
        db_conn = database.init(database_file="insert_item_test.db")
        title = "Test title"
        url = "test_url"
        category = "test_category"
        database.insert_item(db_conn, title, url, category)

        # The content should exists in the database
        c = db_conn.cursor()
        c.execute("SELECT title, url, category FROM items WHERE url='{}'".format(url))
        result = c.fetchone()

        # Make sure it's correct
        self.assertEqual(result[0], title)
        self.assertEqual(result[1], url)
        self.assertEqual(result[2], category)

    def test_insert_item_not_unique_url(self):
        db_conn = database.init(database_file="insert_item_test.db")
        title_1 = "Test title 1"
        url_1 = "test_url_1"
        category_1 = "test_category"
        database.insert_item(db_conn, title_1, url_1, category_1)

        # It should raise an integrity error
        with self.assertRaises(sqlite3.IntegrityError):
            title_2 = "Test title 1"
            category_2 = "test_category"
            database.insert_item(db_conn, title_2, url_1, category_2)

    def test_get_untweeted_python_item(self):
        db_conn = database.init(database_file="python_items_test.db")
        # Populate the database first
        c = db_conn.cursor()

        items = [
            ("first title", "first_url", "python", 1),
            ("second title", "second_url", "python", 0),
            ("third title", "third_url", "python", 0),
        ]
        c.executemany(
        """
            INSERT INTO
                items(title, url, category, is_tweeted)
            VALUES
                (?,?,?,?)
        """,
        items)
        c.close()

        # Test the function, make sure it returns the oldest
        # untweeted item
        item = database.get_untweeted_python_item(db_conn)
        self.assertEqual(item.title, "second title")
        self.assertEqual(item.url, "second_url")
        self.assertEqual(item.category, "python")


if __name__ == "__main__":
    unittest.main()
