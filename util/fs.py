#!/usr/bin/env python
# -*- coding:utf-8 -*-⏎
from __future__ import print_function
import sys
import os
import shutil

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
if sys.version_info<(3,0,0):
    reload(sys)
    sys.setdefaultencoding('utf8')


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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def get_file_list( root, filter_dict=None ):
    fn_list = list()
    for dn, dns, fns in os.walk( root ):
        for fn2 in fns:
            if check_filter( filter_dict, fn2 ):
                fn_list.append( (os.path.join( dn, fn2 ),fn2) )
    return fn_list


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def get_dir_list( root ):
    dn_list = list()
    for dn, dns, fns in os.walk( root ):
        for dn2 in dns:
            dn_list.append( (os.path.join( dn, dn2 ), dn2) )
    return dn_list


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def move_file( src, tgt, verbose ):
    try:
        if verbose: print( "move %s -> %s" % (src,tgt) )
        shutil.move( src, tgt )
    except:
        print( "error!" )
        return False

    return True


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

