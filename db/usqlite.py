#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function

import os
import sys
import sqlite3
reload(sys)
sys.setdefaultencoding("utf-8")

class USQLite:
    sqlite_conn = None
    verbose = 1

    ##############################################################
    def __init__( self, sqlite_fn ):
        self.load_db( sqlite_fn )


    ##############################################################
    def load_db( self, sqlite_fn ):
        if self.verbose >= 1:
            print( "load_db: " + sqlite_fn )
        self.sqlite_conn = sqlite3.connect( sqlite_fn )
        self.sqlite_conn.text_factory = str
        self.sqlite_conn.row_factory = sqlite3.Row

        return True

    ##############################################################
    def get_table_names(self ):
        q = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        res = self.run_select_query( q )
        tlist = list()
        for row in res:
            tlist.append( row[0] )
        return tlist


    ##############################################################
    def create_table(self, tname ):
        q = "CREATE TABLE IF NOT EXISTS %s ( id integer PRIMARY KEY, key text UNIQUE NOT NULL, value text NOT NULL );" % tname
        return self.run_query( q )


    ##############################################################
    def putss(self, tname, k, v ):
        item = ( k, v )
        q = "INSERT OR IGNORE INTO %s (key, value) VALUES(?, ?); " % ( tname )
        return self.run_insert_query( q, item )


    ##############################################################
    def getss(self, tname, k ):
        q = "SELECT * FROM %s WHERE key = '%s';" % ( tname, k )
        res = self.run_select_query( q )
        for row in res:
            print( row )


    ##############################################################
    def run_query(self, query, debugmsg=False ):
        cur = self.sqlite_conn.cursor()

        try:
            cur.execute( query )

        except sqlite3.Error as err:
            if debugmsg:
                print( "ERROR run_query: %s" % query )
                print( err.message )
            return False

        return True


    ##############################################################
    def run_delete_query( self, query ):
        cur = self.sqlite_conn.cursor()

        try:
            cur.execute( query )
            self.sqlite_conn.commit()

        except sqlite3.Error as err:
            print( query )
            print( err.message )
            return False

        return True


    ##############################################################
    def run_select_query(self, query ):
        cur = self.sqlite_conn.cursor()

        try:
            cur.execute( query )
        except sqlite3.Error as err:
            print( query )
            print( err.message )
            return False

        res = cur.fetchall()
        return res

    ##############################################################
    def run_update_query(self, query ):
        cur = self.sqlite_conn.cursor()

        try:
            cur.execute( query )
        except sqlite3.Error as err:
            print( query )
            print( err.message )
            return False

        res = cur.fetchall()
        return res

    ##############################################################
    def run_insert_query( self, query, data ):
        cur = self.sqlite_conn.cursor()

        try:
            cur.execute( query, data )
            self.sqlite_conn.commit()

        except sqlite3.Error as err:
            print( query )
            print( err.message )
            return False

        return True

    ##############################################################
    def run_insert_query_many( self, query, data_list ):
        cur = self.sqlite_conn.cursor()

        try:
            cur.executemany( query, data_list )
            self.sqlite_conn.commit()

        except sqlite3.Error as err:
            print( feat_name )
            print( query )
            print( err.message )
            return False

        return True


##############################################################
if __name__ == '__main__':
    if len( sys.argv ) != 2:
        print( "usage: %s sqlite_fn" % (sys.argv[0]) )
        sys.exit()
    else:
        dbh = USQLite( sys.argv[1] )
        dbh.create_table( "hi" )
        tlist = dbh.get_table_names()
        for t in tlist:
            print( t )
        dbh.putss( "hi", "hello", "description" )
        dbh.getss( "hi", "hello" )


