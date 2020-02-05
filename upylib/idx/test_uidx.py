#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from upylib.idx.uidx import UIdx, UIdxConf


def test_uidx():
    uidx = UIdx()
    #uidx.load(uidxconf)
    #uidx.dump()


def test_uidx_create():
    dn = "tmp_out"
    root = "/home/windnc/data/test"
    recursive = True
    exclude_list = list()
    exclude_list.append("*.o")

    uidxconf = UIdxConf()
    uidxconf.setup(dn=dn, root=root, recursive=True, exclude_list=exclude_list)
    uidxconf.dump()

    uidx = UIdx()
    uidx.load(uidxconf)
    uidx.dump()

    uidx.scan()


if __name__ == "__main__":
    test_uidx_create()
    test_uidx()
