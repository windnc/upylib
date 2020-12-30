import json
from upylib.idx.uidx import UIdx


def test_uidx_create():
    uidx = UIdx(conf_fn="test.json")
    uidx.reset_db()
    # uidx.dump()

    uidx.scan()
    file_list = uidx.get_file_list(path="/")
    assert file_list

    file_list = uidx.get_file_list(path="/d1", recursive=True)
    assert file_list

    for f in file_list:
        print(f["path"], f["fn"])
        f2 = uidx.get_file(path=f["path"], fn=f["fn"])
        print(f2)
        assert uidx.set_tag_int(id=f2["id"], tag="test_int", val=8)
        assert uidx.set_tag_str(id=f2["id"], tag="test_str", val="ok")


def test_uidx():
    uidx = UIdx(conf_fn="test.json")


