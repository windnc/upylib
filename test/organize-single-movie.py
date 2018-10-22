#!/usr/bin/env python
# -*- coding:utf-8 -*-⏎

from __future__ import print_function
from upylib.util.fs import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')



def move_proc( full_dn, full_fn, just_fn, archive_root ):
    ini_fn = os.path.join( full_dn, "info.ini" )
    if os.path.exists( ini_fn ):
        print( "delete %s" % (ini_fn ) )
        del_file( ini_fn )

    target_fn = os.path.join( archive_root, just_fn )
    print( target_fn )
    if not move_file( full_fn, target_fn ):
        return False

    if len( get_file_list( full_dn ) ) == 0:
        del_empty_dir( full_dn )

    return True

#~~~~~~~~~1~~~~~~~~~2~~~~~~~~~3~~~~~~~~~4~~~~~~~~~5~~~~~~~~~6~~~~~~~~~7~~~~~~~~~
def run():
#~~~~~~~~~1~~~~~~~~~2~~~~~~~~~3~~~~~~~~~4~~~~~~~~~5~~~~~~~~~6~~~~~~~~~7~~~~~~~~~
    scan_root="/mnt/disk-op/unitf-data/archive"
    archive_root="/mnt/disk-op/_kodi_archive/Mixed"
    print( "scan: %s" % scan_root )
    print( "move: %s" % archive_root )
    assert_dir( archive_root, verbose=True )

    cnt=0
    dir_list = get_dir_list( scan_root )
    for ( full_dn, just_dn ) in dir_list:

        check = True
        movie_file_list=list()
        file_list = get_file_list( full_dn )
        for (full_fn, just_fn) in file_list:
            if just_fn == "info.ini": continue
            if is_movie( just_fn ):
                movie_file_list.append( (full_fn,just_fn) )
            else:
                check = False

        if not check: continue
        if len( movie_file_list )== 1:
            cnt+=1
            print( "%d\t%s" % (cnt,full_dn) )
            full_fn, just_fn = movie_file_list[0]
            move_proc( full_dn, full_fn, just_fn, archive_root )


#~~~~~~~~~1~~~~~~~~~2~~~~~~~~~3~~~~~~~~~4~~~~~~~~~5~~~~~~~~~6~~~~~~~~~7~~~~~~~~~
if __name__ == "__main__": run()
#~~~~~~~~~1~~~~~~~~~2~~~~~~~~~3~~~~~~~~~4~~~~~~~~~5~~~~~~~~~6~~~~~~~~~7~~~~~~~~~
