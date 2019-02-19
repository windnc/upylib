import os
import unittest
from PIL import Image
from PIL import ImageFile
from PIL import ExifTags
import logging
import piexif
logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)
# logger.setLevel(logging.DEBUG)

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.warnings.simplefilter('error', Image.DecompressionBombWarning)


def save_thumb(src_fn, dst_fn, size):
    # open
    try:
        img = Image.open(src_fn)
    except FileNotFoundError:
        logger.info("file not found")
        return False
    except Exception as e:
        logger.info("image open fail: %s" % e)
        return False

    # rotate based on exif
    exif_bytes = None
    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])

        if piexif.ImageIFD.Orientation in exif_dict["0th"]:
            orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
            exif_bytes = piexif.dump(exif_dict)

            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90, expand=True)

    # prevent alpha channel warning
    try:
        img = img.convert("RGB")
    except Exception as e:
        logger.info("convert RGB fail: %s" % e)
        pass

    # save
    try:
        img.thumbnail(size, Image.ANTIALIAS)
        if exif_bytes:
            logger.debug("save. exif ok")
            img.save(dst_fn, "JPEG", exif=exif_bytes)
        else:
            logger.debug("no save due to no exif: %s" % e)
            #img.save(dst_fn, "JPEG")
            return False
    except Exception as e:
        logger.info("save fail: %s" % e)
        return False

    return True


class TestSaveThumb(unittest.TestCase):
    def test_1(self):
        src_fn = "/tmp/image.jpg"
        dst_fn = "/tmp/image_thumb.jpg"
        size = (120, 100)
        res = save_thumb(src_fn, dst_fn, size)
        self.assertTrue(res)

    def test_2(self):
        from fs import get_file_list
        flist = get_file_list("/tmp/tmpimg")
        for fi in flist:
            size = (120, 100)
            res = save_thumb(fi.full_fn, os.path.join(fi.path, fi.base+"_thumb."+fi.ext), size)
            self.assertTrue(res)

if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    unittest.main()
