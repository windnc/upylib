#!/usr/bin/env python3
import sys
from image import save_thumb
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


def test():
    logger.info("RUN TEST")
    src_fn = "/mnt/disk-op2/tv/코미디 빅리그/코미디 빅리그.E383.201108.720p-NEXT-poster.jpg"
    dst_fn = "a.thumb.jpg"
    size = (120, 100)
    if save_thumb(src_fn, dst_fn, size):
        logger.info("ok")
    else:
        logger.info("fail")

if __name__ == "__main__":
    test()
