import logging
import json

import piexif
from PIL import Image
from PIL import ImageFile

logger = logging.getLogger()
#print(__name__)
# logger.setLevel(logging.ERROR)
# logger.setLevel(logging.DEBUG)

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.warnings.simplefilter('error', Image.DecompressionBombWarning)


def save_thumb(src_fn, dst_fn, size, rotate=True):
    logger.info("image : %s %s" % (src_fn, dst_fn))
    # open
    try:
        img = Image.open(src_fn)
    except FileNotFoundError:
        logger.error("file not found")
        return False
    except Exception as e:
        logger.error("image open fail: %s" % e)
        return False

    # rotate based on exif
    exif_bytes = None
    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])
        exif_bytes = piexif.dump(exif_dict)

        if rotate:
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
        logger.warning("convert RGB fail: %s" % e)
        pass

    # save
    try:
        img.thumbnail(size, Image.ANTIALIAS)
        if exif_bytes:
            logger.debug("save. exif ok")
            img.save(dst_fn, "JPEG", exif=exif_bytes)
        else:
            logger.debug("save. no exif: %s" % src_fn)
            img.save(dst_fn, "JPEG")
    except Exception as e:
        logger.error("save fail: %s" % e)
        return False

    return True


def get_meta(src_fn, full=False):
    try:
        img = Image.open(src_fn)
    except FileNotFoundError:
        logger.info("file not found: %s" % src_fn)
        return False
    except Exception as e:
        logger.info("image open fail: %s" % e)
        return False

    if "exif" not in img.info:
        logger.info("no exif: %s" % src_fn)
        return False

    target_tag_list = list()
    target_tag_list.append("Make")
    target_tag_list.append("Model")
    target_tag_list.append("Orientation")
    target_tag_list.append("DateTimeOriginal")
    target_tag_list.append("GPSLatitude")
    target_tag_list.append("GPSLongitude")
    target_tag_list.append("PixelXDimension")
    target_tag_list.append("PixelYDimension")
    exif_dict = piexif.load(img.info["exif"])
    exif_dict.pop("thumbnail")
    d = dict()
    for k, v in exif_dict.items():
        for k2, v2 in v.items():
            tag_name = piexif.TAGS[k][k2]["name"]
            if not full and tag_name not in target_tag_list:
                continue
            # if type(v2) == bytes:
            #    v2 = v2.decode("utf-8")
            d[tag_name] = v2
    return d
