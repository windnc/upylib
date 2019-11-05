from upylib.util.fs import *
import os


def test_xattr():
    print("test_xattr")
    fn = "test.txt"

    if os.path.isfile(fn):
        os.remove(fn)

    with open(fn, "w"):
        pass

    print("test get")
    res = xattr_get(fn, "key1")
    #print(res)
    assert not res

    print("test set")
    res = xattr_set(fn, "id", "3")
    res = xattr_set(fn, "언어", "한글")
    res = xattr_set(fn, "test", "aa bb c")
    #print(res)
    assert res

    print("test remove")
    res = xattr_remove(fn, "언어")
    print(res)
    assert(res)

    print("test key_list")
    res = xattr_key_list(fn)
    assert res

    for  k in res:
        v = xattr_get(fn, k)
        print("%s: %s" %(k, v))


if __name__ == "__main__":
    test_xattr()
