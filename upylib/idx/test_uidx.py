#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from upylib.idx.uidx import UIdx


def test_uidx():
    uidx = UIdx(conf_fn="test.json")


def test_uidx_create():
    uidx = UIdx(conf_fn="test.json")
    uidx.reset_db()
    # uidx.dump()

    uidx.scan()
    return True
    file_list = uidx.get_file_list(path="/")
    assert file_list
    return True

    file_list = uidx.get_file_list(path="/d1", recursive=True)
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
