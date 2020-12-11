import sys
import os
import sqlite3
import time
import requests
import urllib.request
import urllib.parse


def read_url(url, retry=1, encoding="utf-8", verbose=1):
    if not url:
        if verbose >= 1:
            print("no url")
        return False

    for _ in range(0, retry):
        try:
            c = urllib.request.urlopen(url)
            content = c.read()
            if encoding:
                content = content.decode(encoding)
            return content

        except Exception as e:
            if verbose >= 1:
                print(e)
            continue

    return False


def get_url(url, retry=1, encoding="utf-8", verbose=1):
    return read_url(url, retry, encoding, verbose)


def post_url(url, retry=1, data_byte=None, data_dict=None, encoding="utf-8", verbose=1):
    if not url:
        if verbose >= 1:
            print("no url")
        return False

    for _ in range(0, retry):
        try:
            if data_byte:
                data = data_byte
            elif data_dict:
                data = urllib.parse.urlencode(data_dict).encode("ascii")
            else:
                data = None

            c = urllib.request.urlopen(url=url, data=data)
            content = c.read()
            if encoding:
                content = content.decode(encoding)
            return content

        except Exception as e:
            if verbose >= 1:
                print(e)
            continue

    return False


def urlenc(q):
    return urllib.parse.quote_plus(q)



class CachedWeb:
    def __init__(self, cache_dir="./.cachedweb", rebuild=False):
        self.loaded = False
        self.db_fn = os.path.join(cache_dir, "url_content.db")

        if rebuild:
            os.remove(self.db_fn)

        self._prepare(cache_dir)

    def __del__(self):
        if self.db:
            self.db.close()

    def _prepare(self, cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        if os.path.isdir(cache_dir):
            self.cache_dir = cache_dir
        else:
            return False

        self.db = sqlite3.connect(self.db_fn)
        if self.db:
            self.db.text_factory = str
            self.db.row_factory = sqlite3.Row
        else:
            return False

        sql = "CREATE TABLE IF NOT EXISTS url_content"
        sql += "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
        sql += " url TEXT UNIQUE NOT NULL, content TEXT); "
        cur = self.db.cursor()
        cur.execute(sql)
        self.db.commit()

        #  print(sql)
        # ok
        self.loaded = True
        return True

    def insert(self, url, content):
        if not self.loaded:
            return False

        sql = "INSERT INTO url_content (url, content) VALUES (?, ?);"
        try:
            cur = self.db.cursor()
            cur.execute(sql, [url, content])
            self.db.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(e)
            return False
        except Exception as e:
            print(repr(e))
            return False

    def search(self, url):
        if not self.loaded:
            return False

        sql = "SELECT content FROM url_content WHERE url = ?;"
        cur = self.db.cursor()
        cur.execute(sql, [url])
        res = cur.fetchall()
        if not res:
            return False

        row = res[0]
        return row["content"]

    def down_url(self, url, retry=3):
        for _ in range(retry):
            try:
                resp = requests.get(url)
                # resp.raise_for_status()
                if resp.status_code == 200:
                    return resp.content
                else:
                    return False
            except requests.ConnectionError:
                # print(e)
                time.sleep(1)
            except requests.Timeout:
                # print(e)
                time.sleep(1)
        return False

    def cached_search(self, url):
        if not self.loaded:
            return False

        r = self.search(url)
        if r is not False:
            return r

        # miss
        r = self.down_url(url)
        if r is False:
            self.insert(url, None)
            return None
        else:
            self.insert(url, r)
            return r

