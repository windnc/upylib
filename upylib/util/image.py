from PIL import Image
from PIL import ExifTags

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~4~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~8
def save_thumb(src, dst, size, verbose=1):
    try:
        img = Image.open(src)
    except Exception as e:
        if verbose>=1:
            print(e)
        return False

    orientation = None
    for k, v in ExifTags.TAGS.items() : 
        if v == "Orientation":
            orientation = k
            break

    exif_dict = img._getexif()
    if exif_dict:
        if exif_dict[orientation] == 3 : 
            img=img.rotate(180, expand=True)
        elif exif_dict[orientation] == 6 : 
            img=img.rotate(270, expand=True)
        elif exif_dict[orientation] == 8 : 
            img=img.rotate(90, expand=True)
        else:
            pass

    try:
        img.thumbnail( size, Image.ANTIALIAS )
        img.save(dst, "JPEG")
    except Exception as e:
        if verbose>=1:
            print(e)
        return False

    return True
