import datetime
import json
import os

from upylib.util.fs import is_image, is_text, is_music, is_movie


class FileInfo:
    full_fn = None
    fn = None
    path = None
    base = None
    ext = None
    filetype = None
    icon = None
    cstamp = None
    mstamp = None
    cstr = None
    mstr = None
    size = None
    is_valid = False

    def __init__(self, full_fn=None, path=None, fn=None):
        if full_fn:
            self.full_fn = full_fn
            self.path = os.path.dirname(full_fn)
            self.fn = os.path.basename(full_fn)

        else:
            self.full_fn = os.path.join(path, fn)
            self.path = path
            self.fn = fn

        if not os.path.isfile(self.full_fn):
            return

        b, e = os.path.splitext(self.fn)
        if e.startswith("."):
            e = e[1:]
        self.base = b
        self.ext = e

        self.cstamp = int(os.path.getctime(full_fn))
        self.mstamp = int(os.path.getmtime(full_fn))
        self.astamp = int(os.path.getatime(full_fn))
        self.cstr = datetime.datetime.fromtimestamp(self.cstamp).strftime("%y.%m.%d %H:%M:%S")
        self.mstr = datetime.datetime.fromtimestamp(self.mstamp).strftime("%y.%m.%d %H:%M:%S")
        self.astr = datetime.datetime.fromtimestamp(self.astamp).strftime("%y.%m.%d %H:%M:%S")
        self.size = os.path.getsize(full_fn)
        from upylib.util.fs import get_filesize_str
        self.size_str = get_filesize_str(self.size)
        self.is_valid = True

        return

    def setmatime(self, mstamp):
        os.utime(self.full_fn, (mstamp, mstamp))

    def is_image(self):
        return is_image(self.fn)

    def is_movie(self):
        return is_movie(self.fn)

    def is_music(self):
        return is_music(self.fn)

    def is_text(self):
        return is_text(self.fn)

    def jsonify(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __repr__(self):
        return self.jsonify()


class DirInfo:
    abs_dn = None
    full_dn = None
    dn = None
    path = None
    icon = None
    cstamp = None
    mstamp = None
    cstr = None
    mstr = None
    size = None
    is_valid = False

    def __init__(self, full_dn=None, path=None, dn=None):
        if full_dn:
            self.full_dn = full_dn
            self.path = os.path.dirname(full_dn)
            self.dn = os.path.basename(full_dn)
        else:
            self.full_dn = os.path.join(path, dn)
            self.path = path
            self.dn = dn

        if not os.path.isdir(self.full_dn):
            raise NotEx

        self.abs_dn = os.path.abspath(self.full_dn)
        self.cstamp = int(os.path.getctime(self.full_dn))
        self.mstamp = int(os.path.getmtime(self.full_dn))
        self.cstr = datetime.datetime.fromtimestamp(self.cstamp).strftime("%y.%m.%d %H:%M:%S")
        self.mstr = datetime.datetime.fromtimestamp(self.mstamp).strftime("%y.%m.%d %H:%M:%S")
        self.is_valid = True

        return

    def setmatime(self, mstamp):
        os.utime(self.full_dn, (mstamp, mstamp))

    def jsonify(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __repr__(self):
        return self.jsonify()
