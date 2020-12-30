from upylib.util.fs import get_file_list, NotExistsError


def test_get_file_list():
    print("test invlid")
    root = "a"
    print(root)
    try:
        file_list = get_file_list(root)
    except NotExistsError:
        print("fail")

    root = "../"
    print(root)
    finfo_list = get_file_list(root)
    if finfo_list:
        for i, finfo in enumerate(finfo_list):
            print(finfo)
            if i >= 3:
                break
    else:
        print("fail")

    print("test recursive")
    finfo_list = get_file_list(root, recursive=True)
    if finfo_list:
        for i, finfo in enumerate(finfo_list):
            print(finfo)
            if i >= 3:
                break
    else:
        print("fail")

    print("test recursive with ext")
    finfo_list = get_file_list(root, recursive=True, ctx={"filter": {"ext": "py"}})
    if finfo_list:
        for i, finfo in enumerate(finfo_list):
            print(finfo)
            if i >= 3:
                break
    else:
        print("fail")

    print("test sort")
    finfo_list = get_file_list(root, recursive=True, ctx={"filter": {"ext": "py"}, "sort": "size", "order": "desc"})
    if finfo_list:
        for i, finfo in enumerate(finfo_list):
            # print(finfo.toJson())
            print(finfo.full_fn, finfo.size)
            # if i >= 3:
            #    break
    else:
        print("fail")
