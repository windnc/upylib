import os
from upylib.util import fs
from upylib.db.usqlite import USQLite


class UIdxConf:
    def __init__(self):
        self.dn = None
        self.root = None
        self.recursive = False
        self.exclude_list = list()
        pass

    def setup(self, dn, root, recursive, exclude_list):
        self.dn = dn
        self.root = root
        self.recursive = recursive
        self.exclude_list = list(exclude_list)

    def dump(self):
        print("dn: %s" % self.dn)
        print("root: %s" % self.root)
        print("recursive: %s" % self.recursive)
        print("exclude_list: %s" % self.exclude_list)


class UIdx:
    def __init__(self):
        self.conf = None
        self.fi_list = None
        self.db = None

    def load(self, conf):
        self.conf = conf
        self.load_db()

    def load_db(self):
        os.makedirs(self.conf.dn, exist_ok=True)
        self.db = USQLite(self.conf.dn + "/uidx.db")
        sql = "CREATE TABLE IF NOT EXISTS file ( id INTEGER PRIMARY KEY, path TEXT NOT NULL );"
        self.db.create_table(sql)

    def reset_db(self):
        self.db.drop_table("file")
        self.load_db()
        return True

    def scan(self):
        self.fi_list = list()
        self.reset_db()
        fi_list = fs.get_file_list(root=self.conf.root, recursive=self.conf.recursive)

        data_list = list()
        for fi in fi_list:
            data_list.append((fi.path,))
        print(data_list)

        sql = "INSERT INTO file (path) VALUES (?);"
        res = self.db.insert_query_many(sql, data_list)
        print(res)



    def dump(self):
        print(self.conf)
