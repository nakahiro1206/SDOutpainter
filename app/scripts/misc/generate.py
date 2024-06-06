from scripts.make_mask import make_mask
from scripts.outpaint import outpaint
from io import StringIO, BytesIO
from PIL import Image

def resize(image: Image):
    ok = True
    for size in image.size:
        if size != 512:
            ok = False
            break
    if ok:
        return image
    else:
        return image.resize((512, 512))

def generate(left_image_file_storage):
    # left_image: FileStorage
    # 画像を読み込む
    left_image = resize(Image.open(left_image_file_storage))

    """upper and upper left should be given by POST argument"""

    # load upper image
    upper_image = resize(Image.open("img/upper.png"))

    # load upper right image
    upper_left_image = resize(Image.open("img/upper_left.png"))

    # create input and mask
    input_image, mask_image = make_mask(upper_left_image, upper_image, left_image)

    generated_image = outpaint(input_image, mask_image)

    # Image from Pillow
    img_io = BytesIO() # or StryingIO
    generated_image.save(img_io, 'PNG', quality=95)
    generated_image.save("./out.png", 'PNG')
    img_io.seek(0)
    return img_io