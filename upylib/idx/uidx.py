import os
import json
from upylib.util import fs
from upylib.util import regex
from upylib.db.usqlite import USQLite


class UIdx:
    def __init__(self, conf_fn):
        self.conf_fn = conf_fn
        self.load()

    def load(self):
        if not os.path.isfile(self.conf_fn):
            return False

        with open(self.conf_fn, "r") as f:
            self.conf = json.load(f)

        if not self.load_db():
            return False

        return True

    def load_db(self):
        os.makedirs(self.conf["dn"], exist_ok=True)
        self.db = USQLite(self.conf["dn"] + "/uidx.db")
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

        for column in self.conf["column_list"]:
            self.db.assert_column("file", column["name"], column["type"])
            #print(column)

        return True

    def reset_db(self):
        self.db.drop_table("file")
        self.load_db()
        return True

    def assert_tag_db_column(self, fi_list):
        tag_list = list()
        for fi in fi_list:
            tag_val = fs.xattr_get(fi.full_fn, "uidx_tag")
            if tag_val:
                print(tag_val)
        tag_list.append("udix_i_confirmm")
        tag_list.append("uidx_s_title")

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
        fi_list = fs.get_file_list(root=self.conf["root"], recursive=self.conf["recursive"])
        self.assert_tag_db_column(fi_list)


        vlist = list()
        clist = list()
        vlist.append("path")
        clist.append("?")
        vlist.append("fn")
        clist.append("?")
        vlist.append("ext")
        clist.append("?")
        vlist.append("cstamp")
        clist.append("?")
        vlist.append("mstamp")
        clist.append("?")
        vlist.append("astamp")
        clist.append("?")
        vlist.append("size")
        clist.append("?")
        for column in self.conf["column_list"]:
            vlist.append(column["name"])
            clist.append("?")

        data_list = list()
        for fi in fi_list:
            rel_path = fi.path[len(self.conf["root"]):].strip("/")
            if rel_path:
                rel_path = "/" + rel_path + "/"


            data = list()
            data.append(rel_path)
            data.append(fi.fn)
            data.append(fi.ext)
            data.append(fi.cstamp)
            data.append(fi.mstamp)
            data.append(fi.astamp)
            data.append(fi.size)


            for column in self.conf["column_list"]:
                #print(column["name"])
                found = False
                for parse in column["parse_list"]:
                    #print("\t", parse)
                    if parse["field"] == "fn":
                        src = fi.fn
                    elif parse["field"] == "path":
                        src = rel_path
                    else:
                        src = None

                    if regex.regex_match(src, parse["patt"]):
                        rep = regex.regex_replace(src, parse["patt"], parse["rep"])
                        #print(rep)
                        data.append(rep)
                        #print("match")
                        found = True
                        break

                if not found:
                    data.append(column["default"])

            data_list.append(data)
        #print(vlist)
        #print(data_list)

        if data_list:
            sql = "INSERT INTO file (%s) VALUES (%s);" % (",".join(vlist), ",".join(clist))
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

    def search(self, where_sql, order_sql, limit_sql):
        if not where_sql:
            return False

        sql = "SELECT * FROM file WHERE %s" % where_sql
        if order_sql:
            sql = sql + " " + order_sql
        if limit_sql:
            sql = sql + " " + limit_sql

        res = self.db.select_query(sql)
        if not res:
            return False

        file_list = list()
        for row in res:
            f = dict()
            for k in row.keys():
                f[k] = row[k]
            f["full_fn"] = self.conf.root + f["path"] + f["fn"]
            file_list.append(f)
        return file_list

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
        #print("set")
        full_fn = self.conf["root"]
        if f["path"]:
            full_fn = self.conf["root"] + f["path"]
        full_fn = full_fn + f["fn"]
        #print("full: %s" % full_fn)
        if not os.path.isfile(full_fn):
            return False

        file_tag = "uidx"
        prev = fs.xattr_get(full_fn, file_tag, default="")
        if prev:
            tag_dict = json.loads(prev)
        else:
            tag_dict = dict()
        tag_dict[tag] = {'t': 'i', 'v': val}

        res = fs.xattr_set(full_fn, file_tag, json.dumps(tag_dict))
        if not res:
            return False

        column_name = "uidx_i_%s" % tag
        #print(column_name)
        if not self.db.assert_column("file", column_name, "INTEGER"):
            return False

        sql = "UPDATE file SET %s = ? WHERE id = ?;" % column_name
        data = (val, f["id"])
        res = self.db.update_query(sql, data)
        if not res:
            return False

        return True

    def set_tag_str(self, id=None, path=None, fn=None, tag=None, val=None):
        f = self.get_file(id, path, fn)
        if not f:
            return f

        # tag file
        #print("set")
        full_fn = self.conf["root"]
        if f["path"]:
            full_fn = self.conf["root"] + f["path"]
        full_fn = full_fn + f["fn"]
        #print("full: %s" % full_fn)
        if not os.path.isfile(full_fn):
            return False

        file_tag = "uidx"
        prev = fs.xattr_get(full_fn, file_tag, default="")
        print("prev: %s" % prev)
        if prev:
            tag_dict = json.loads(prev)
        else:
            tag_dict = dict()
        tag_dict[tag] = {'t': 's', 'v': val}
        print("next: %s" % json.dumps(tag_dict))

        res = fs.xattr_set(full_fn, file_tag, json.dumps(tag_dict))
        if not res:
            return False

        column_name = "uidx_s_%s" % tag
        #print(column_name)
        if not self.db.assert_column("file", column_name, "TEXT"):
            return False

        sql = "UPDATE file SET %s = ? WHERE id = ?;" % column_name
        data = (val, f["id"])
        res = self.db.update_query(sql, data)
        if not res:
            return False

        return True

    def dump(self):
        print(json.dumps(self.conf, ensure_ascii=False, indent=2))
