import sys
from upylib.db.dbfunc import *


class USQLite:
    def __init__(self, db_fn):
        self.verbose = 1
        self.db_fn = db_fn

    def get_table_names(self):
        return db_get_table_names(self.db_fn)

    def get_column_names(self, table_name):
        return db_get_column_names(self.db_fn, table_name)

    def assert_column(self, table_name, column_name, opt):
        return db_assert_column(self.db_fn, table_name, column_name, opt)

    def is_table(self, tbl_name, verbosity=1):
        return db_is_table(self.db_fn, tbl_name, verbosity)

    def create_table(self, sql, verbosity=1):
        return db_create_table(self.db_fn, sql, verbosity)

    def drop_table(self, tbl_name, verbosity=1):
        return db_drop_table(self.db_fn, tbl_name, verbosity)

    def delete_query(self, sql, data=[], verbosity=1):
        return db_delete_query(self.db_fn, sql, data, verbosity)

    def select_query(self, sql, data=[], verbosity=1):
        return db_select_query(self.db_fn, sql, data, verbosity)

    def update_query(self, sql, data, verbosity=1):
        return db_update_query(self.db_fn, sql, data, verbosity)

    def insert_query(self, sql, data, verbosity=1):
        return db_insert_query(self.db_fn, sql, data, verbosity)

    def insert_query_many(self, sql, data_list, verbosity=1):
        return db_insert_query_many(self.db_fn, sql, data_list, verbosity)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: %s fn" % (sys.argv[0]))
        sys.exit()

    else:
        db_fn=sys.argv[1]
        udb = USQLite(db_fn)

        sql="CREATE TABLE IF NOT EXISTS tbl (id INTERGER);"
        udb.create_table(sql)
        tlist = udb.get_table_names()
        for t in tlist:
            print(t)

        sql="DELETE FROM tbl WHERE id=1"
        udb.delete_query(sql)

        sql = "INSERT INTO tbl (id) VALUES (?);"
        data = [1]
        udb.insert_query(sql, data)

        sql = "UPDATE tbl SET id=? WHERE id=?"
        data = [3, 1]
        udb.update_query(sql, data)

        sql = "INSERT INTO tbl (id) VALUES (?);"
        data = [[100],[200]]
        udb.insert_query_many(sql, data)

        sql = "SELECT * from tbl WHERE 1"
        rows = udb.select_query(sql)
        for row in rows:
            print( row )

