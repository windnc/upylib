#!/usr/bin/env python
# -*- coding:utf-8 -*-⏎

from __future__ import print_function
import sys
from urllib import request as urlreq


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
if sys.version_info<(3,0,0):
    reload(sys)
    sys.setdefaultencoding('utf8')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~5~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def read_url(url, retry=1):
    if not url: return False

    for _ in range(0,retry):
        try:
            c = urlreq.urlopen(url)
            return c.read()
        except Exception as e:
            print(e)
            print(url)
            continue

    return False


def urlenc(q):
    return q
