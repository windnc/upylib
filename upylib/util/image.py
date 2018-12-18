from PIL import Image
from PIL import ExifTags

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def save_thumb(src_fn, dst_fn, size, verbose=1):
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
    # open
    try:
        img = Image.open(src_fn)
    except Exception as e:
        if verbose>=1:
            print(e)
        return False

    # rotate based on exif
    try:
        exif_dict = img._getexif()
        if exif_dict:
            orientation = None
            for k, v in ExifTags.TAGS.items() : 
                if v == "Orientation":
                    orientation = k
                    break
            if orientation:
                if exif_dict[orientation] == 3 : 
                    img=img.rotate(180, expand=True)
                elif exif_dict[orientation] == 6 : 
                    img=img.rotate(270, expand=True)
                elif exif_dict[orientation] == 8 : 
                    img=img.rotate(90, expand=True)
                else:
                    pass
    except Exception as e:
        if verbose>=1:
            print(e)
        pass

    # prevent alpha channel warning
    img = img.convert("RGB")

    # save
    try:
        img.thumbnail( size, Image.ANTIALIAS )
        img.save(dst_fn, "JPEG")
    except Exception as e:
        if verbose>=1:
            print("Save fail: %s" % e)
        return False

    return True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def test_save_thumb():
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
    src_fn = "/tmp/image.jpg"
    dst_fn = "/tmp/image_thumb.jpg"
    size = (120, 100)
    if save_thumb(src_fn, dst_fn, size, verbose=1):
        print("ok")
    else:
        print("fail")


test_save_thumb()
