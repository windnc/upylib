from upylib.util.fileinfo import FileInfo, DirInfo


def test_fileinfo():
    fi = FileInfo("test_fileinfo.py")
    assert fi.is_valid

    fi = FileInfo("nofile.ext")
    assert not fi.is_valid


def test_dirinfo():
    di = DirInfo("/var/log")
    assert di.is_valid

    di = DirInfo("/var/log/nodir")
    assert not di.is_valid
