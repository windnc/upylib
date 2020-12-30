from upylib.util.fs import get_dir_list


def test_fs():
    root = "../"
    print(root)
    dinfo_list = get_dir_list(root)
    if dinfo_list:
        for i, dinfo in enumerate(dinfo_list):
            # print(dinfo.toJson())
            print(dinfo)
            if i >= 3:
                break
    else:
        print("fail")

    print("test recursive")
    root = "../../"
    dinfo_list = get_dir_list(root, recursive=True)
    if dinfo_list:
        for i, dinfo in enumerate(dinfo_list):
            print(dinfo)
            if i >= 10:
                break
    else:
        print("fail")

    print("test sort")
    dinfo_list = get_dir_list(root, recursive=True, ctx={"sort": "dn", "order": "asc"})
    if dinfo_list:
        for i, dinfo in enumerate(dinfo_list):
            print(dinfo.full_dn)
            if i >= 10:
                break
    else:
        print("fail")
