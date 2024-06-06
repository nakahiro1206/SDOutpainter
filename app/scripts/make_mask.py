from PIL import Image
from scripts.noise import perlin_noise, gaussian_noise
from scripts.noise_with_module import perlin_noise2
import numpy as np

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
    
def is_all_None(image_is_None, tpl):
    for i in tpl:
        if not image_is_None[i]:
            return False
    return True
    
def make_mask(image_map):
    """
    image_map: Flask.FileStorage[]
    0: up_left   | 1: up   | 2: up_right  
    -------------+---------+--------------
    3: left      | 4: None | 5: right     
    -------------+---------+--------------
    6: down_left | 7: down | 8: down_right 
    """
    margin = 64
    inpaint_size = 512
    whole_size = inpaint_size + margin*2

    # Create blank images filled with white
    input_image = Image.new('RGB', (whole_size, whole_size), color=(255, 255, 255))
    mask_image = Image.new('RGB', (whole_size, whole_size), color=(255, 255, 255))


    """# trace input 
    # box=(left, upper, right, lower)
    # paste: box(left, upper)
    input_image.paste(upper_left_image.crop((inpaint_size-margin, inpaint_size-margin, inpaint_size, inpaint_size)), (0, 0))
    input_image.paste(upper_image.crop((0, inpaint_size-margin, inpaint_size, inpaint_size)), (margin, 0))
    input_image.paste(left_image.crop((inpaint_size-margin, 0, inpaint_size, inpaint_size)), (0, margin))

    mask_image.paste((0, 0, 0), (0, 0, margin, whole_size))
    mask_image.paste((0, 0, 0), (0, 0, whole_size, margin))"""

    image_is_None = [False] * 9

    left_up_idx = [inpaint_size-margin, 0, 0]
    right_down_idx = [inpaint_size, inpaint_size, margin]
    Left_Up_idx = [0, margin, inpaint_size + margin]
    Right_Down_idx = [margin, margin+inpaint_size, whole_size]
    for idx, image_data in enumerate(image_map):
        if image_data is None:
            image_is_None[idx] = True
            continue
        image = resize(Image.open(image_data))
        h_pos = idx//3
        w_pos = idx%3

        left = left_up_idx[w_pos]
        right = right_down_idx[w_pos]
        up = left_up_idx[h_pos]
        down = right_down_idx[h_pos]

        Left = Left_Up_idx[w_pos]
        Up = Left_Up_idx[h_pos]

        # image.paste(image.crop((left, up, right, down)), (Left, Up))
        input_image.paste(image.crop((left, up, right, down)), (Left, Up))

        Right = Right_Down_idx[w_pos]
        Down = Right_Down_idx[h_pos]

        # fill with black
        mask_image.paste((0, 0, 0), (Left, Up, Right, Down))

    # crop None area
    crop_left = 0
    crop_right = whole_size
    crop_up = 0
    crop_down = whole_size
    if is_all_None(image_is_None, (0, 3, 6)):
        crop_left += margin
    if is_all_None(image_is_None, (2, 5, 8)):
        crop_right -= margin
    if is_all_None(image_is_None, (0, 1, 2)):
       crop_up += margin
    if is_all_None(image_is_None, (6, 7, 8)):
        crop_down -= margin
    
    input_image = input_image.crop((crop_left, crop_up, crop_right, crop_down))
    mask_image = mask_image.crop((crop_left, crop_up, crop_right, crop_down))

    input_np = np.array(input_image)
    mask_np = np.array(mask_image)

    # add noise on inout and mask
    input_np_noised, mask_np_noised = perlin_noise(input_np, mask_np)
    # input_np_noised, mask_np_noised = perlin_noise2(input_np, mask_np)
    # input_np_noised, mask_np_noised = gaussian_noise(input_np, mask_np)

    input_image_noised = Image.fromarray(input_np_noised)
    mask_image_noised  = Image.fromarray(mask_np_noised)

    # save images
    input_image_noised.save("img/input_noised.png", 'PNG')
    mask_image_noised.save("img/mask_noised.png", 'PNG')

    return input_image_noised, mask_image_noised