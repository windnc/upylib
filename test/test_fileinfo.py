#!/usr/bin/env python3
# -*- coding:utf-8 -*-⏎
from upylib.util.fileinfo import FileInfo, DirInfo


def test_fileinfo():
    fi = FileInfo("README.md")
    assert fi.is_valid

    fi = FileInfo("nofile.ext")
    assert not fi.is_valid


def test_dirinfo():
    di = DirInfo("/var/log")
    assert di.is_valid

    di = DirInfo("/var/log/nodir")
    assert not di.is_valid


"""
def del_empty_dir( root ):
    dir_list = get_dir_list( root )
    for (dn, just_dn) in dir_list:
        fn_list = get_file_list( dn )
        if len( fn_list  ) == 1:
            fn, just_fn = fn_list[0]
            print( "delete %s" % (fn) )
            os.remove( fn )
            os.rmdir( dn )

def run():
    root="/mnt/disk-media/unitf-data/archive"
    f_dict=dict()
    f_dict["contain"] = list()
    f_dict["contain"].append( "탑기어" )

    tgt_dn = "/mnt/disk-media/_kodi_entry/2.TV/ko/17.탑기어 코리아"
    fn_list = get_file_list( root, filter_dict=f_dict)
    for (fn, just_fn) in fn_list:
        new_fn = os.path.join( tgt_dn, just_fn )
        move_file( fn, new_fn, verbose=True )

    del_empty_dir( root )


if __name__ == "__main__": run()
"""
