#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from upylib.idx.uidx import UIdx, UIdxConf


def test_uidx():
    uidx = UIdx()
    #uidx.load(uidxconf)
    #uidx.dump()


def test_uidx_create():
    dn = "tmp_out"
    root = "/tmp/tmp-uidx"
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
    file_list = uidx.get_file_list(path="/")
    assert file_list

    file_list = uidx.get_file_list(path="/dir1", recursive=True)
    assert file_list

    for f in file_list:
        print(f["path"], f["fn"])
        f2 = uidx.get_file(path=f["path"], fn=f["fn"])
        print(f2)
        assert uidx.set_tag_int(id=f2["id"], tag="confirm", val=1)

    """
    f3 = uidx.get_file(id=4)
    print(f3)

    t = uidx.get_tag_dict(id=4)
    print(t)


    t = uidx.get_tag_dict(id=3)
    print(t)
    """


if __name__ == "__main__":
    test_uidx_create()
    test_uidx()
