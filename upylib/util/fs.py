#!/usr/bin/env python3
import os
import hashlib
import shutil
import unittest
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


def extract_ext(fn, lowcase=True):
    if not fn:
        return ""
    ext = os.path.splitext(fn)[1]
    if len(ext) > 0 and ext[0] == '.':
        ext = ext[1:]
    if lowcase:
        ext = ext.lower()
    return ext


class TestExtractExt(unittest.TestCase):
    def test_1(self):
        print("test_extract_ext")
        ext = extract_ext(fn="hello.txt")
        self.assertEqual(ext, "txt")
        ext = extract_ext(fn="/home/hello")
        self.assertEqual(ext, "")
        ext = extract_ext(fn="")
        self.assertEqual(ext, "")
        ext = extract_ext(fn="out.MP4")
        self.assertEqual(ext, "mp4")
        ext = extract_ext(fn=".bashrc")
        self.assertEqual(ext, "")
        ext = extract_ext(fn="out.MP4", lowcase=False)
        self.assertEqual(ext, "MP4")


def is_movie(fn):
    ext = extract_ext(fn)
    if not ext:
        return False
    if ext in ("mp4", "mkv", "wmv", "avi"):
        return True
    else:
        return False


class TestIsMovie(unittest.TestCase):
    def test_1(self):
        print("test_is_movie")
        self.assertTrue(is_movie(fn="out.MP4"))
        self.assertTrue(is_movie(fn="out.avi"))
        self.assertFalse(is_movie(fn="out.mp3"))
        self.assertFalse(is_movie(fn=".mkv"))


def is_image(fn):
    ext = extract_ext(fn)
    if not ext:
        return False
    if ext in ("jpg", "png", "gif", "bmp"):
        return True
    else:
        return False


class TestIsImage(unittest.TestCase):
    def test_1(self):
        print("test_is_image")
        self.assertTrue(is_image(fn="out.jpg"))
        self.assertTrue(is_image(fn="out.png"))
        self.assertFalse(is_image(fn=""))
        self.assertFalse(is_image(fn="out.c"))


def is_music(fn):
    ext = extract_ext(fn)
    if not ext:
        return False
    if ext in ("mp3", "wav", "mid", "aac", "flac"):
        return True
    else:
        return False


class TestIsMusic(unittest.TestCase):
    def test_1(self):
        print("test_is_music")
        self.assertTrue(is_music(fn="out.mp3"))
        self.assertTrue(is_music(fn="out.wav"))
        self.assertTrue(is_music(fn="out.mid"))
        self.assertFalse(is_music(fn="out.h"))


def is_text(fn):
    ext = extract_ext(fn)
    if not ext:
        return False
    if ext in ("txt", "md", "ini", "json", "c", "cpp", "php", "h", "py", "java"):
        return True
    else:
        return False


class TestIsText(unittest.TestCase):
    def test_1(self):
        print("test_is_text")
        self.assertTrue(is_text(fn="out.txt"))
        self.assertTrue(is_text(fn="out.md"))
        self.assertTrue(is_text(fn="out.php"))


def check_filter(finfo, filter_dict):
    if not filter_dict:
        return True

    if "ext" in filter_dict:
        if finfo.ext.lower() != filter_dict["ext"].lower():
            return False

    return True


def get_parent(root:str) -> str:
    if root == "/":
        return ""
    return os.path.abspath(os.path.join(root, os.pardir))


class TestGetParent(unittest.TestCase):
    def test_1(self):
        print("test_get_parent")
        self.assertEqual(get_parent(root="/tmp"), "/")
        self.assertEqual(get_parent(root="/"), "")

def get_file_list(root, recursive=False, ctx=None):
    from fileinfo import FileInfo

    if not os.path.isdir(root):
        return False

    # init: get all files
    full_fn_list = list()
    if recursive is True:
        for dn, dns, fns in os.walk(root):
            for fn2 in fns:
                full_fn = os.path.join(dn, fn2)
                full_fn_list.append(full_fn)
    else:
        for fn in os.listdir(root):
            full_fn = os.path.join(root, fn)
            if os.path.isfile(full_fn):
                full_fn_list.append( full_fn )

    # filter
    fi_list = list()
    for full_fn in full_fn_list:
        finfo = FileInfo(full_fn=full_fn)
        if ctx and "filter" in ctx:
            if check_filter(finfo, ctx["filter"]):
                fi_list.append( finfo )
            else:
                # filter
                pass
        else:
            fi_list.append( finfo )

    # sort
    if ctx and "sort" in ctx:
        if ctx["sort"] == "full_fn":
            fi_list.sort(key=lambda x: x.full_fn)
        elif ctx["sort"] == "fn":
            fi_list.sort(key=lambda x: x.fn)
        elif ctx["sort"] == "cstamp":
            fi_list.sort(key=lambda x: x.cstamp)
        elif ctx["sort"] == "size":
            fi_list.sort(key=lambda x: x.size)

        if "order" in ctx and ctx["order"] == "desc":
            fi_list.reverse()


    return fi_list


class TestGetFileList(unittest.TestCase):
    def test_1(self):
        print("test_get_file_list")
        self.assertTrue(get_file_list(root="/tmp", recursive=True))



def is_file(fn):
    if os.path.isfile(fn):
        return True
    else:
        # broken symlink
        if os.path.islink(fn):
            return True
        else:
            return False


class TestIsFile(unittest.TestCase):
    def test_1(self):
        print("test_is_file")
        with open("/tmp/src", "w") as fo:
            print("hi", file=fo)
        self.assertTrue(is_file(fn="/tmp/src"))
        self.assertFalse(is_file(fn="/tmp/no-file"))


def get_dir_list(root, recursive=False, ctx=None):
    if not os.path.isdir(root):
        return False

    from fileinfo import DirInfo
    full_dn_list = list()
    if recursive is True:
        for dn, dns, fns in os.walk(root):
            for dn2 in dns:
                full_dn = os.path.join(dn, dn2)
                full_dn_list.append(full_dn)
    else:
        for dn in os.listdir(root):
            full_dn = os.path.join(root, dn)
            if os.path.isdir(full_dn):
                full_dn_list.append(full_dn)

    di_list = list()
    for full_dn in full_dn_list:
        dinfo = DirInfo(full_dn=full_dn)
        if ctx and "filter" in ctx:
            if check_filter(dinfo, ctx["filter"]):
                di_list.append(dinfo)
            else:
                # filter
                pass
        else:
            di_list.append(dinfo)

    # sort
    if ctx and "sort" in ctx:
        if ctx["sort"] == "full_dn" or ctx["sort"] == "full_fn":
            di_list.sort(key=lambda x: x.full_dn)
        elif ctx["sort"] == "dn" or ctx["sort"] == "fn":
            di_list.sort(key=lambda x: x.dn)
        elif ctx["sort"] == "cstamp":
            di_list.sort(key=lambda x: x.cstamp)
        elif ctx["sort"] == "size":
            di_list.sort(key=lambda x: x.size)

        if "order" in ctx and ctx["order"] == "desc":
            di_list.reverse()

    return di_list


class TestGetDirList(unittest.TestCase):
    def test_1(self):
        print("test_get_dir_lsit")
        self.assertTrue(get_dir_list(root="/tmp", recursive=True))


def is_empty_dir(root):
    logging.debug("is empty dir: %s" % root)

    file_list = get_file_list(root, recursive=False)
    if file_list is False:
        logging.info("file list fail: %s" % root)
        return False
    if len(file_list) > 0:
        logging.debug("more than 0 file")
        return False

    dir_list = get_dir_list(root, recursive=False)
    if dir_list is False:
        logging.info("dir list fail: %s" % root)
        return False
    if len(dir_list) > 0:
        logging.debug("more than 0 dir")
        return False

    return True


class TestIsEmptyDir(unittest.TestCase):
    def test_1(self):
        print("test_is_empty_dir")
        assert_dir("/tmp/empty")
        self.assertTrue(is_empty_dir("/tmp/empty"))


def del_empty_dir(root):
    logging.debug("del empty dir: %s" % root)

    if not is_empty_dir(root):
        return True

    try:
        os.rmdir(root)
    except Exception as e:
        logging.info("del dir exception: %s" % e)
        return False

    return True


class TestDelEmptyDir(unittest.TestCase):
    def test_1(self):
        print("test_del_empty_dir")
        assert_dir("/tmp/empty")
        self.assertTrue(del_empty_dir("/tmp/empty"))


def del_file(fn):
    logging.debug("del file %s" % fn)

    try:
        os.remove(fn)
    except Exception as e:
        logging.info("del file exception: %s" % e)
        return False

    return True


class TestDelFile(unittest.TestCase):
    def test_1(self):
        print("test_del_file")
        with open("/tmp/src", "w") as fo:
            print("hi", file=fo)
        self.assertTrue(del_file("/tmp/src"))

def assert_no_file(fn:str) -> bool:
    logging.debug("assert no file %s" % fn)

    if is_file(fn):
        logging.debug("del file: %s" % fn)
        if not del_file(fn):
            return False

    return True


class TestAssertNoFile(unittest.TestCase):
    def test_1(self):
        print("test_assert_no_file")
        self.assertTrue(assert_no_file("/tmp/tmpdir/aa"))


def move_file(src, tgt):
    logging.debug("move file: %s -> %s" % (src, tgt))

    try:
        shutil.move(src, tgt)
    except Exception as e:
        logging.info("move file error: %s" % e)
        return False

    return True


class TestMoveFile(unittest.TestCase):
    def test_1(self):
        print("test_move_file")
        with open("/tmp/src", "w") as fo:
            print("hi", file=fo)
        self.assertTrue(move_file("/tmp/src", "/tmp/tgt"))
        self.assertFalse(move_file("/tmp/src", "/tmp/tgt"))

def assert_dir(dn, verbose=1):
    logging.debug("assert_dir : %s" % dn)

    if os.path.exists(dn):
        logging.debug("already exists: %s" % dn)
        return True

    logging.debug("try to make dir: %s" % dn)
    os.makedirs(dn, exist_ok=True)

    return os.path.exists(dn)


class TestAssertDir(unittest.TestCase):
    def test_1(self):
        print("test_assert_dir")
        self.assertTrue(assert_dir(dn="/tmp/tmpdir"))


def get_md5(fn):
    if not fn or not os.path.exists(fn):
        return ""

    hash_md5 = hashlib.md5()
    with open(fn, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class TestGetMD5(unittest.TestCase):
    def test_1(self):
        print("test_getmd5")
        md5val = get_md5(fn="__init__.py")
        self.assertEqual(md5val, "d41d8cd98f00b204e9800998ecf8427e")
        md5val = get_md5(fn="")
        self.assertEqual(md5val, "")


def get_filesize_str(s):
    if s > 1024 * 1024 * 1024 * 1024:
        return "%1.2f TB" % (float(s)/1024/1024/1024/1024)
    elif s > 1024 * 1024 * 1024: 
        return "%1.2f GB" % (float(s)/1024/1024/1024)
    elif s > 1024 * 1024: 
        return "%1.2f MB" % (float(s)/1024/1024)
    elif s > 1024:
        return "%1.2f KB" % (float(s)/1024)
    else:
        return "%d B" % s


class TestGetFileSizeStr(unittest.TestCase):
    def test_1(self):
        print("test_get_filesize_str")
        self.assertEqual(get_filesize_str(10), "10 B")
        self.assertEqual(get_filesize_str(3000000), "2.86 MB")
        self.assertEqual(get_filesize_str(4000000000), "3.73 GB")
        self.assertEqual(get_filesize_str(5000000000000), "4.55 TB")
        self.assertEqual(get_filesize_str(6000000000000000), "5456.97 TB")


if __name__ == "__main__":
    unittest.main()

