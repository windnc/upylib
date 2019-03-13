import os
from upylib.util.image import save_thumb
from upylib.util.fs import get_file_list
from upylib.util.fs import NotExistsError


def test_1():
    src_fn = "/tmp/image.jpg"
    dst_fn = "/tmp/image_thumb.jpg"
    size = (120, 100)
    res = save_thumb(src_fn, dst_fn, size, rotate=True)
    assert res


def test_2():
    try:
        flist = get_file_list("/tmp/tmpimg")
    except NotExistsError as e:
        print(e)
        return

    for fi in flist:
        size = (120, 100)
        res = save_thumb(fi.full_fn, os.path.join(fi.path, fi.base + "_thumb." + fi.ext), size, rotate=True)
        assert res
