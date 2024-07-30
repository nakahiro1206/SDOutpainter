from PIL import Image, ImageOps, ImageFilter
from scripts.noise import perlin_noise # , gaussian_noise
# from scripts.noise_with_module import perlin_noise2
import numpy as np
from scripts.const import get_const

def reiterate_neighbor(idx, neighbor):
    margin, inpaint_size, whole_size = get_const()

    if idx%2 == 0 or neighbor is None:
        return None
    
    new_Image = Image.new('RGB', (inpaint_size, inpaint_size))
    if idx == 1: # up
        for i in range(inpaint_size//margin):
            if i%2 == 0:
                new_Image.paste(ImageOps.flip(neighbor),(0, i*margin))
            else:
                new_Image.paste(neighbor,(0, i*margin))
    
    if idx == 3: # left
        for i in range(inpaint_size//margin):
            if i%2 == 0:
                new_Image.paste(ImageOps.mirror(neighbor),(i*margin, 0))
            else:
                new_Image.paste(neighbor,(i*margin, 0))

    if idx == 5: # right
        for i in range(inpaint_size//margin):
            if i%2 == 1:
                new_Image.paste(ImageOps.mirror(neighbor),(i*margin, 0))
            else:
                new_Image.paste(neighbor,(i*margin, 0))
    
    if idx == 7: # down
        for i in range(inpaint_size//margin):
            if i%2 == 1:
                new_Image.paste(ImageOps.flip(neighbor),(0, i*margin))
            else:
                new_Image.paste(neighbor, (0, i*margin))
    else: pass
    return np.array(new_Image)

def calc_proportion(w, h, L, key, keys):
    # L == inpaint_size
    d = {"left": w, "right": L-w, "up":h, "down": L-h}
    divided = 1 / d[key]
    divisor = sum([1 / d[k] for k in keys])

    # return (1/x)/((1/x) + (1/y))
    # return (1/x)/((1/x) + (1/(W-x)))
    # return (1/x)/((1/x) + (1/y) + (1/(H-y)))
    # return (1/x)/((1/x) + (1/y) + (1/(W-x)))
    # return (1/x)/((1/x) + (1/y) + (1/(H-y)) + (1/(W-x)))
    return divided / divisor


def apply_propotion_filter(key, neighbors_dict):
    margin, inpaint_size, whole_size = get_const()
    
    w = np.linspace(0, inpaint_size, inpaint_size+2)[1:-1]
    h = np.linspace(0, inpaint_size, inpaint_size+2)[1:-1]

    W, H = np.meshgrid(w, h)
    Z = calc_proportion(W, H, inpaint_size, key, neighbors_dict.keys())

    return neighbors_dict[key] * Z[:, :, np.newaxis]

def merge_neighbors(reiterated_neighbors, input_image):
    margin, inpaint_size, whole_size = get_const()

    merged_np = np.zeros((inpaint_size, inpaint_size, 3))

    keys = ["up","left","right","down"]
    neighbors_dict = {}
    for i in range(4):
        n = reiterated_neighbors[2*i+1]
        if n is not None:
            neighbors_dict[keys[i]] = n

    for key in neighbors_dict.keys():
        filtered_image = apply_propotion_filter(key, neighbors_dict)
        Image.fromarray(np.uint8(filtered_image)).save(f"img/{key}.png")
        merged_np += filtered_image

    merged_image = Image.fromarray(np.uint8(merged_np))
    # merged_image = merged_image.filter(ImageFilter.GaussianBlur(5))
    input_image.paste(merged_image, (margin, margin))

    return input_image
