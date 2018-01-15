#!/usr/bin/env python
# -*- coding:utf-8 -*-⏎

from __future__ import print_function
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
def get_dir_list( root ):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
    for dn, dns, fns in os.walk( root ):
        #print( "dn of " + root );
        #print( dn )
        #print( "dns of " + root );
        #print( dns )
        #print( "fns of " + root );
        print( fns )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
def txtfile2dict( fn ):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
    d = dict()
    with open( fn,'r') as f:
        for line in f.readlines():
            line = line.strip( "\n" )
            d[ line ] = True
    return d

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
def tsvfile2dict( fn, keyid, valueid ):
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
    d = dict()
    with open( fn,'r') as f:
        for line in f.readlines():
            line = line.strip("\n")
            arr = line.split("\t")
            d[ arr[keyid] ] = arr[valueid]
    return d

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
def test():
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
    if len( sys.argv ) != 3:
        print( "usage: %s fn-in fn-out" % sys.argv[0] )
        return False
    return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
if __name__ == "__main__": test()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~⏎
