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
        return True

    def load_db(self):
        os.makedirs(self.conf.dn, exist_ok=True)
        self.db = USQLite(self.conf.dn + "/uidx.db")
        sql = """
        CREATE TABLE IF NOT EXISTS file (
            id INTEGER PRIMARY KEY, 
            path TEXT NOT NULL,
            fn TEXT NOT NULL,
            ext TEXT,
            cstamp INTEGER NOT NULL,
            mstamp INTEGER NOT NULL,
            astamp INTEGER NOT NULL,
            size INTEGER NOT NULL
        );""".strip()
        self.db.create_table(sql)
        return True

    def reset_db(self):
        self.db.drop_table("file")
        self.load_db()
        return True

    def assert_tag_db_schema(self, fi_list):
        tag_list = list()
        for fi in fi_list:
            tag_val = fs.xattr_get(fi.full_fn, "uidx_tag")
            if tag_val:
                print(tag_val)
        tag_list.append("i_confirmm")
        tag_list.append("s_title")

        for tag in tag_list:
            t, tag_name = tag.split("_", 1)
            if t == "i":
                self.db.assert_column("file", tag_name, "INTEGER")
            elif t == "s":
                self.db.assert_column("file", tag_name, "TEXT")

        return True

    def scan(self):
        self.fi_list = list()
        self.reset_db()
        fi_list = fs.get_file_list(root=self.conf.root, recursive=self.conf.recursive)
        self.assert_tag_db_schema(fi_list)

        data_list = list()
        for fi in fi_list:
            rel_path = fi.path[len(self.conf.root):].strip("/")
            if rel_path:
                rel_path = "/" + rel_path + "/"
            data_list.append((rel_path, fi.fn, fi.ext, fi.cstamp, fi.mstamp, fi.astamp, fi.size))
            #print(fi)
        #print(data_list)

        if data_list:
            sql = """
            INSERT INTO file (path, fn, ext, cstamp, mstamp, astamp, size)
            VALUES (?,?,?,?,?,?,?);"""
            res = self.db.insert_query_many(sql, data_list)
            if not res:
                return False

        return True

    def get_file_list(self, path="", recursive=False):
        path = path.strip("/")
        if path:
            path = "/" + path + "/"
        if recursive:
            sql = "SELECT * FROM file WHERE path LIKE '%s%%';" % path
        else:
            sql = "SELECT * FROM file WHERE path='%s';" % path

        res = self.db.select_query(sql)
        if not res:
            return False

        file_list = list()
        for row in res:
            f = dict()
            for k in row.keys():
                f[k] = row[k]
            file_list.append(f)
        return file_list


    def get_file(self, id=None, path=None, fn=None):
        if id:
            sql = "SELECT * FROM file WHERE id='%d';" % id
        elif path and fn:
            sql = "SELECT * FROM file WHERE path='%s' AND fn='%s';" % (path, fn)
        else:
            return False

        res = self.db.select_query(sql)
        if not res or len(res) < 1:
            return False

        f = dict()
        for k in res[0].keys():
            f[k] = res[0][k]
        return f

    def get_tag_dict(self, id=None, path=None, fn=None):
        f = self.get_file(id, path, fn)
        if not f:
            return f

        tag_dict = dict()
        for k, v in f.items():
            if k.startswith("tag_"):
                tag = k[len("tag_"):]
                tag_dict[tag] = v
        return tag_dict

    def set_tag_int(self, id=None, path=None, fn=None, tag=None, val=None):
        f = self.get_file(id, path, fn)
        if not f:
            return f

        # tag file
        full_fn = self.conf.root + f["path"] + f["fn"]
        if not os.path.isfile(full_fn):
            return False

        file_tag = "uidx_i_%s" % tag
        #res = fs.xattr_set(full_fn, file_tag, val)
        res = fs.xattr_get(full_fn, file_tag, default="hi")
        print(res)
        if res:
            print("ok")


        return True



    def dump(self):
        print(self.conf)
