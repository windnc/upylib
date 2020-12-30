from upylib.util.fs import get_dir_list, NotExistsError
from upylib.util.fileinfo import DirInfo


def test_dirinfo():
    print("test dinfo")
    dinfo = DirInfo(full_dn=".")
    print(dinfo)
    assert dinfo
