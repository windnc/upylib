from upylib.util.fs import *


def test_extract_ext():
    print("test_extract_ext")
    ext = extract_ext(fn="hello.txt")
    assert ext == "txt"
    ext = extract_ext(fn="/home/hello")
    assert ext == ""
    ext = extract_ext(fn="")
    assert ext == ""
    ext = extract_ext(fn="out.MP4")
    assert ext == "mp4"
    ext = extract_ext(fn=".bashrc")
    assert ext == ""
    ext = extract_ext(fn="out.MP4", lowcase=False)
    assert ext == "MP4"


def test_is_movie():
    print("test_is_movie")
    assert is_movie(fn="out.MP4")
    assert is_movie(fn="out.avi")
    assert not is_movie(fn="out.mp3")
    assert not is_movie(fn=".mkv")


def test_is_image():
    print("test_is_image")
    assert is_image(fn="out.jpg")
    assert is_image(fn="out.png")
    assert not is_image(fn="")
    assert not is_image(fn="out.c")


def test_is_music():
    print("test_is_music")
    assert is_music(fn="out.mp3")
    assert is_music(fn="out.wav")
    assert is_music(fn="out.mid")
    assert not is_music(fn="out.h")


def test_is_test():
    print("test_is_text")
    assert is_text(fn="out.txt")
    assert is_text(fn="out.md")
    assert is_text(fn="out.php")


def test_get_parent():
    print("test_get_parent")
    assert get_parent(root="/tmp") == "/"
    assert get_parent(root="/") == ""


def test_get_file_list():
    print("test_get_file_list")
    assert get_file_list(root="/tmp", recursive=True)


def test_get_dir_list():
    print("test_get_dir_lsit")
    assert get_dir_list(root="/tmp", recursive=True)


def test_is_file():
    print("test_is_file")
    with open("/tmp/src", "w") as fo:
        print("hi", file=fo)
    assert is_file(fn="/tmp/src")
    assert not is_file(fn="/tmp/no-file")


def test_is_empty_dir():
    print("test_is_empty_dir")
    assert_dir("/tmp/empty")
    assert is_empty_dir("/tmp/empty")


def test_del_empty_dir():
    print("test_del_empty_dir")
    assert_dir("/tmp/empty")
    assert del_empty_dir("/tmp/empty")


def test_del_file():
    print("test_del_file")
    with open("/tmp/src", "w") as fo:
        print("hi", file=fo)
    assert del_file("/tmp/src")


def test_assert_no_file():
    print("test_assert_no_file")
    assert assert_no_file("/tmp/tmpdir/aa")


def test_move_file():
    print("test_move_file")
    with open("/tmp/src", "w") as fo:
        print("hi", file=fo)
    assert move_file("/tmp/src", "/tmp/tgt")
    assert not move_file("/tmp/src", "/tmp/tgt")


def test_assert_dir():
    print("test_assert_dir")
    assert assert_dir(dn="/tmp/tmpdir")


def test_md5val():
    print("test_getmd5")
    md5val = get_md5(fn="upylib/util/__init__.py")
    assert md5val == "d41d8cd98f00b204e9800998ecf8427e"
    md5val = get_md5(fn="")
    assert md5val == ""


def test_get_filesize_str():
    assert get_filesize_str(10) == "10 B"
    assert get_filesize_str(3000000) == "2.86 MB"
    assert get_filesize_str(4000000000) == "3.73 GB"
    assert get_filesize_str(5000000000000) == "4.55 TB"
    assert get_filesize_str(6000000000000000) == "5456.97 TB"
