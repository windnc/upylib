#!/usr/bin/env python3
import os
import hashlib
import shutil
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


def is_movie(fn):
    ext = extract_ext(fn)
    if not ext:
        return False
    if ext in ("mp4", "mkv", "wmv", "avi"):
        return True
    else:
        return False


def is_image(fn):
    ext = extract_ext(fn)
    if not ext:
        return False
    if ext in ("jpg", "png", "gif", "bmp"):
        return True
    else:
        return False


def is_music(fn):
    ext = extract_ext(fn)
    if not ext:
        return False
    if ext in ("mp3", "wav", "mid", "aac", "flac"):
        return True
    else:
        return False


def is_text(fn):
    ext = extract_ext(fn)
    if not ext:
        return False
    if ext in ("txt", "md", "ini", "json", "c", "cpp", "php", "h", "py", "java"):
        return True
    else:
        return False


def check_filter(finfo, filter_dict):
    if not filter_dict:
        return True

    if "ext" in filter_dict:
        if finfo.ext.lower() != filter_dict["ext"].lower():
            return False

    return True


def get_parent(root: str) -> str:
    if root == "/":
        return ""
    return os.path.abspath(os.path.join(root, os.pardir))


def get_file_list(root, recursive=False, ctx=None):
    from upylib.util.fileinfo import FileInfo

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
                full_fn_list.append(full_fn)

    # filter
    fi_list = list()
    for full_fn in full_fn_list:
        finfo = FileInfo(full_fn=full_fn)
        if ctx and "filter" in ctx:
            if check_filter(finfo, ctx["filter"]):
                fi_list.append(finfo)
            else:
                # filter
                pass
        else:
            fi_list.append(finfo)

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


def is_file(fn):
    if os.path.isfile(fn):
        return True
    else:
        # broken symlink
        if os.path.islink(fn):
            return True
        else:
            return False


def get_dir_list(root, recursive=False, ctx=None):
    if not os.path.isdir(root):
        return False

    from upylib.util.fileinfo import DirInfo
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


def del_file(fn):
    logging.debug("del file %s" % fn)

    try:
        os.remove(fn)
    except Exception as e:
        logging.info("del file exception: %s" % e)
        return False

    return True


def assert_no_file(fn: str) -> bool:
    logging.debug("assert no file %s" % fn)

    if is_file(fn):
        logging.debug("del file: %s" % fn)
        if not del_file(fn):
            return False

    return True


def move_file(src, tgt):
    logging.debug("move file: %s -> %s" % (src, tgt))

    try:
        shutil.move(src, tgt)
    except Exception as e:
        logging.info("move file error: %s" % e)
        return False

    return True


def assert_dir(dn):
    logging.debug("assert_dir : %s" % dn)

    if os.path.exists(dn):
        logging.debug("already exists: %s" % dn)
        return True

    logging.debug("try to make dir: %s" % dn)
    os.makedirs(dn, exist_ok=True)

    return os.path.exists(dn)


def get_md5(fn):
    if not fn or not os.path.exists(fn):
        return ""

    hash_md5 = hashlib.md5()
    with open(fn, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


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

