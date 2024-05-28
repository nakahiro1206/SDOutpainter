from static.make_mask import make_mask
from static.inpaint import main
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
    upper_image = resize(Image.open("static/pizza_1024_30.png"))

    # load upper right image
    upper_left_image = resize(Image.open("static/pizza.png"))

    # create input and mask
    input_image, mask_image = make_mask(upper_left_image, upper_image, left_image)

    generated_image = main(input_image, mask_image)

    # Image from Pillow
    img_io = BytesIO() # or StryingIO
    generated_image.save(img_io, 'PNG', quality=95)
    img_io.seek(0)
    return img_io