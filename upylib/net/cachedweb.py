import os
import sqlite3
import time

import requests
from upylib.db.usqlite import USQLite
from upylib.net.url import get_url


class CachedWeb:
    def __init__(self, cache_dir="./cachedweb", rebuild=False):
        self.loaded = False
        self.db_fn = os.path.join(cache_dir, "url_content.db")

        if rebuild:
            os.remove(self.db_fn)
        self._prepare(cache_dir)

    def __del__(self):
        # if self.db:
        #     self.db.close()
        pass

    def _prepare(self, cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        if os.path.isdir(cache_dir):
            self.cache_dir = cache_dir
        else:
            return False

        sql = "CREATE TABLE IF NOT EXISTS url_content"
        sql += "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
        sql += " url TEXT UNIQUE NOT NULL, content TEXT); "
        #  print(sql)

        self.db = USQLite(self.db_fn)
        self.db.create_table(sql)
        self.loaded = True
        return True

    def insert(self, url, content):
        if not self.loaded:
            return False

        sql = "INSERT INTO url_content (url, content) VALUES (?, ?);"
        try:
            self.db.insert_query(sql, [url, content])
        except sqlite3.IntegrityError as e:
            print(e)
            return False
        except Exception as e:
            print(repr(e))
            return False

    def delete(self, url):
        if not self.loaded:
            return False

        try:
            sql = "DELETE FROM url_content WHERE url=?;"
            self.db.delete_query(sql, [url])
        except sqlite3.IntegrityError as e:
            print(e)
            return False
        except Exception as e:
            print(repr(e))
            return False
        else:
            return True

    def search(self, url):
        if not self.loaded:
            return False

        sql = "SELECT content FROM url_content WHERE url = ?;"
        res = self.db.select_query(sql, [url])
        if not res:
            return None

        row = res[0]
        return row["content"]

    def fetch_data(self):
        if not self.loaded:
            return False

        sql = "SELECT url, content FROM url_content WHERE 1;"
        res = self.db.select_query(sql)
        if not res:
            return None

        for row in res:
            yield (row[0], row[1])

    def get_count(self):
        if not self.loaded:
            return False

        sql = "SELECT count(*) FROM url_content WHERE 1;"
        res = self.db.select_query(sql)
        return res[0][0]

    def down_url(self, url, retry=3, encoding=None):
        return get_url(url, retry, encoding)

    def cached_search(self, url):
        if not self.loaded:
            return False

        r = self.search(url)
        if r is False:
            return False
        elif r is None:
            r = self.down_url(url)
            if r is False:
                self.insert(url, "failed")
                return None
            else:
                self.insert(url, r)
                return r
        else:
            return r
