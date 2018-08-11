#!/usr/bin/env python
# -*- coding:utf-8 -*-⏎

from __future__ import print_function
import sys
import os
import time
import shutil
import datetime

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
if sys.version_info<(3,0,0):
    reload(sys)
    sys.setdefaultencoding('utf8')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def is_movie( fn ):
    if not fn: return False
    ext = os.path.splitext( fn )[1].lower()
    if ext == ".mp4": return True
    elif ext == ".avi": return True
    elif ext == ".mkv": return True

    return False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def check_filter( filter_dict, path ):
    if not filter_dict: return True
    for k, v in filter_dict.items():
        if k == "ext":
            return True
        elif k == "contain":
            for patt in v:
                if path.find( patt ) < 0: return False

    return True


class FileInfo:
    full_fn = None
    fn = None
    path = None
    base = None
    ext = None
    filetype = None
    icon = None
    cstamp = -1
    mstamp = -1
    cstr = None
    mstr = None
    size = -1

    def __init__(self, path, fn):
        full_fn = os.path.join(path, fn)
        if not os.path.isfile(full_fn):
            return

        self.full_fn = full_fn
        self.fn = fn
        self.path = path
        b,e = os.path.splitext(fn)
        if e.startswith("."):
            e = e[1:]
        self.base = b
        self.ext = e
        self.cstamp = int(os.path.getctime(full_fn))
        self.mstamp = int(os.path.getmtime(full_fn))
        self.cstr = datetime.datetime.fromtimestamp( self.cstamp ).strftime("%y.%m.%d %H:%M:%S")
        self.mstr = datetime.datetime.fromtimestamp( self.mstamp ).strftime("%y.%m.%d %H:%M:%S")
        self.size = os.path.getsize(full_fn)
        self.sizestr = "{:,}".format(self.size)
        st = os.stat(full_fn)

        return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def get_parent( root ):
    if root == "/":
        return None
    return os.path.abspath(os.path.join(root, os.pardir))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def get_file_list( root, filter_dict=None, recursive=False):
    if recursive is False:
        tmplist = list()
        for fn in os.listdir(root):
            full_fn = os.path.join(root, fn)
            if os.path.isfile(full_fn):
                tmplist.append(FileInfo(root, fn))
        return tmplist

    else:
        fn_list = list()
        for dn, dns, fns in os.walk( root ):
            for fn2 in fns:
                if check_filter( filter_dict, fn2 ):
                    fn_list.append( (os.path.join( dn, fn2 ),fn2) )
        return fn_list


class DirInfo:
    full_fn = None
    fn = None
    path = None
    base = None
    ext = None
    filetype = None
    icon = None
    cstamp = -1
    mstamp = -1
    cstr = None
    mstr = None
    size = -1

    def __init__(self, path, dn):
        full_dn = os.path.join(path, dn)
        if not os.path.isdir(full_dn):
            return

        self.full_dn = full_dn
        self.dn = dn
        self.path = path
        self.cstamp = int(os.path.getctime(full_dn))
        self.mstamp = int(os.path.getmtime(full_dn))
        self.cstr = datetime.datetime.fromtimestamp( self.cstamp ).strftime("%y.%m.%d %H:%M:%S")
        self.mstr = datetime.datetime.fromtimestamp( self.mstamp ).strftime("%y.%m.%d %H:%M:%S")
        #self.size = os.path.getsize(full_fn)
        self.size = 0

        return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def get_dir_list(root, recursive=False):
    if recursive is False:
        tmplist = list()
        for tmp in os.listdir(root):
            dn = os.path.join(root, tmp)
            if os.path.isdir(dn):
                tmplist.append(DirInfo(root, tmp))
        return tmplist

    else:
        dn_list = list()
        for dn, dns, fns in os.walk( root ):
            for dn2 in dns:
                dn_list.append( (os.path.join( dn, dn2 ), dn2) )
        return dn_list


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
def del_empty_dir( dn, verbose=False ):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
    try:
        if verbose: print( "delete %s" % (dn) )
        os.rmdir( dn )
    except:
        if verbose: print( "delete error! %s" % (dn) )
        return False
    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
def del_file( fn, verbose=1):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
    if verbose >= 1:
        print( "del_file %s" % (fn) )

    try:
        os.remove( fn )
    except Exception as e:
        print( "delete error! %s" % (fn) )
        print( e )
        return False
    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
def assert_no_file(fn, verbose=1):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
    if verbose >= 1:
        print( "assert no file %s" % (fn) )

    if os.path.isfile(fn):
        print(verbose)
        return del_file(fn, verbose=verbose)
    return True

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def move_file( src, tgt, verbose=1 ):
    try:
        if verbose >= 1:
            print( "move %s -> %s" % (src,tgt) )
        shutil.move( src, tgt )
    except Exception as e:
        print( "error!" )
        print( e )
        return False

    return True


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
def assert_dir( dn, verbose=1 ):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
    if not os.path.exists( dn ):
        if verbose>=1:
            print( "mkdir %s" % (dn) )

        os.makedirs(dn)

    """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    """
    return os.path.exists( dn )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def txtfile2dict( fn ):
    d = dict()
    with open( fn,'r') as f:
        for line in f.readlines():
            line = line.strip( "\n" )
            d[ line ] = True
    return d


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def tsvfile2dict( fn, keyid, valueid ):
    d = dict()
    with open( fn,'r') as f:
        for line in f.readlines():
            line = line.strip("\n")
            arr = line.split("\t")
            d[ arr[keyid] ] = arr[valueid]
    return d


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def test():
    if len( sys.argv ) != 3:
        print( "usage: %s fn-in fn-out" % sys.argv[0] )
        return False
    return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
if __name__ == "__main__":
    test()

