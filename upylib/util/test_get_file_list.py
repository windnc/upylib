#!/usr/bin/env python
# -*- coding:utf-8 -*-⏎

from __future__ import print_function

from fs import *


def test():
    print("test invlid")
    root = "a"
    print(root)
    file_list = get_file_list(root)
    if file_list:
        print(file_list)
    else:
        print("fail")

    root = "../"
    print(root)
    finfo_list = get_file_list(root)
    if finfo_list:
        for i, finfo in enumerate(finfo_list):
            print(finfo.toJson())
            if i >= 3:
                break
    else:
        print("fail")

    print("test recursive")
    finfo_list = get_file_list(root, recursive=True)
    if finfo_list:
        for i, finfo in enumerate(finfo_list):
            print(finfo.toJson())
            if i >= 3:
                break
    else:
        print("fail")

    print("test recursive with ext")
    finfo_list = get_file_list(root, recursive=True, ctx={"filter": {"ext": "py"}})
    if finfo_list:
        for i, finfo in enumerate(finfo_list):
            print(finfo.toJson())
            if i >= 3:
                break
    else:
        print("fail")

    print("test sort")
    finfo_list = get_file_list(root, recursive=True, ctx={"filter": {"ext": "py"}, "sort": "size", "order": "desc"})
    if finfo_list:
        for i, finfo in enumerate(finfo_list):
            # print(finfo.toJson())
            print(finfo.full_fn, finfo.size)
            # if i >= 3:
            #    break
    else:
        print("fail")


if __name__ == "__main__":
    test()
