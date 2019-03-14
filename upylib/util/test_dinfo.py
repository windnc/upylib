#!/usr/bin/env python
# -*- coding:utf-8 -*-⏎

from __future__ import print_function

from fs import *


def test():
    print("test dinfo")
    dinfo = DirInfo(full_dn="/home/windnc")
    print(dinfo.toJson())

    print("test dinfo")
    dinfo = DirInfo(path="/home", dn="windnc")
    print(dinfo.toJson())

    print("test get_dir_list")
    dinfo_list = get_dir_list("/home/windnc")
    for dinfo in dinfo_list:
        print(dinfo.toJson())


if __name__ == "__main__": test()
