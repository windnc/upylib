#!/usr/bin/env python3
# -*- coding:utf-8 -*-⏎

from __future__ import print_function

from upylib.net.net import *


def test():
    url = "http://naver.com"
    r = read_url(url, retry=1)
    if r:
        print(r)
    else:
        print("fail")

    q = "한글 문자열"
    qenc = urlenc(q)
    if qenc:
        print(qenc)
    else:
        print("fail")


if __name__ == "__main__":
    test()
