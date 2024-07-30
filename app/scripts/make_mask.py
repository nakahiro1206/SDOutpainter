from PIL import Image, ImageOps, ImageFilter
from scripts.noise import perlin_noise # , gaussian_noise
# from scripts.noise_with_module import perlin_noise2
import numpy as np
from scripts.prepaint import merge_neighbors, reiterate_neighbor
from scripts.const import get_const

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

def find_nearest(repeated_neighbors, h, w, inpaint_size):
    d = [["left", w], ["up",h], ["down",inpaint_size-h], ["right",inpaint_size-w]]
    d.sort(key=lambda x: x[1])
    for e in d:
        key = e[0]
        if key not in repeated_neighbors:
            continue
        return repeated_neighbors[key][h][w]
    
def make_mask(image_map):
    """
    image_map: Flask.FileStorage[]
    0: up_left   | 1: up   | 2: up_right  
    -------------+---------+--------------
    3: left      | 4: None | 5: right     
    -------------+---------+--------------
    6: down_left | 7: down | 8: down_right 
    """
    margin, inpaint_size, whole_size = get_const()

    # Create blank images filled with white
    input_image = Image.new('RGB', (whole_size, whole_size), color=(255, 255, 255))
    mask_image = Image.new('RGB', (whole_size, whole_size), color=(255, 255, 255))

    image_is_None = [False] * 9
    reiterated_neighbors = [None] * 9

    # Copy peripheral of neighboring image to input image
    # idx for source
    left_up_idx = [inpaint_size-margin, 0, 0]
    right_down_idx = [inpaint_size, inpaint_size, margin]
    # idx for destination
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
        cropped_source = image.crop((left, up, right, down))
        input_image.paste(cropped_source, (Left, Up))

        if idx%2 != 0: # idx = 1, 3, 5, 7 (up, left, right, down)
            reiterated_neighbors[idx] = reiterate_neighbor(idx, cropped_source)

        Right = Right_Down_idx[w_pos]
        Down = Right_Down_idx[h_pos]

        # fill with black
        mask_image.paste((0, 0, 0), (Left, Up, Right, Down))
    
    if not is_all_None(image_is_None, (1, 3, 5, 7)):
        input_image = merge_neighbors(reiterated_neighbors, input_image)

    else: # add perlin noise
        input_np = np.array(input_image)
        mask_np = np.array(mask_image)

        # add noise on inout and mask
        input_np_noised, mask_np_noised = perlin_noise(input_np, mask_np)
        # input_np_noised, mask_np_noised = perlin_noise2(input_np, mask_np)
        # input_np_noised, mask_np_noised = gaussian_noise(input_np, mask_np)

        input_image_noised = Image.fromarray(input_np_noised)
        # mask_image_noised  = Image.fromarray(mask_np_noised)

        input_image = input_image_noised

    # crop None area
    crop_left = 0
    crop_right = whole_size
    crop_up = 0
    crop_down = whole_size
    # area to be inpainted
    area_to_inpaint_left = margin
    area_to_inpaint_right = whole_size - margin
    area_to_inpaint_up = margin
    area_to_inpaint_down = whole_size - margin
    if is_all_None(image_is_None, (0, 3, 6)):
        crop_left += margin
        area_to_inpaint_left -= margin
        area_to_inpaint_right -= margin
    if is_all_None(image_is_None, (2, 5, 8)):
        crop_right -= margin
    if is_all_None(image_is_None, (0, 1, 2)):
       crop_up += margin
       area_to_inpaint_up -= margin
       area_to_inpaint_down -= margin
    if is_all_None(image_is_None, (6, 7, 8)):
        crop_down -= margin

    assert area_to_inpaint_down - area_to_inpaint_up == inpaint_size
    assert area_to_inpaint_right - area_to_inpaint_left == inpaint_size
    
    input_image = input_image.crop((crop_left, crop_up, crop_right, crop_down))
    mask_image = mask_image.crop((crop_left, crop_up, crop_right, crop_down))

    # save images
    input_image.save("img/input.png", 'PNG')
    mask_image.save("img/mask.png", 'PNG')

    return input_image, mask_image, area_to_inpaint_left, area_to_inpaint_up, area_to_inpaint_right, area_to_inpaint_down

def make_mask_for_boundary(input_image, mask_image, left, up, right, down):
    margin, inpaint_size, whole_size = get_const()
    # fill black generated area
    width, height = mask_image.size
    mask_image.paste(im=(0,0,0), box=(
        left if left==0 else left+margin, 
        up if up==0 else up+margin, 
        right if right==width else right-margin, 
        down if down==height else down-margin))
    
    input_np = np.array(input_image)
    mask_np = np.array(mask_image)
    not_masked_area = np.all(mask_np == [255, 255, 255], axis=-1)
    input_np[not_masked_area] = [255, 255, 255]

    # add noise on inout and mask
    input_np_noised, mask_np_noised = perlin_noise(input_np, mask_np)

    input_image_noised = Image.fromarray(input_np_noised)
    mask_image_noised  = Image.fromarray(mask_np_noised)

    # save images
    input_image_noised.save("img/input_noised_for_boundary.png", 'PNG')
    mask_image_noised.save("img/mask_noised_for_boundary.png", 'PNG')

    return input_image_noised, mask_image_noised