from PIL import Image

def make_mask(upper_left_image: Image, upper_image: Image, left_image: Image):
    margin = 64
    inpaint_size = 512
    whole_size = inpaint_size + margin

    # Create blank images filled with white
    input_image = Image.new('RGB', (whole_size, whole_size), color=(255, 255, 255))
    mask_image = Image.new('RGB', (whole_size, whole_size), color=(255, 255, 255))

    # trace input 
    # box=(left, upper, right, lower)
    # paste: box(left, upper)
    input_image.paste(upper_left_image.crop((inpaint_size-margin, inpaint_size-margin, inpaint_size, inpaint_size)), (0, 0))
    input_image.paste(upper_image.crop((0, inpaint_size-margin, inpaint_size, inpaint_size)), (margin, 0))
    input_image.paste(left_image.crop((inpaint_size-margin, 0, inpaint_size, inpaint_size)), (0, margin))

    mask_image.paste((0, 0, 0), (0, 0, margin, whole_size))
    mask_image.paste((0, 0, 0), (0, 0, whole_size, margin))

    return input_image, mask_image