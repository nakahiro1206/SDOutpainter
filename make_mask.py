import cv2
import numpy as np
import sys

def main():
    margin = 128
    inpaint_size = 640 - margin
    whole_size = inpaint_size + margin
    argv = sys.argv
    top_left_path = argv[1]
    top_right_path = argv[2]
    bottom_left_path = argv[3]
    extension = top_left_path.split('.')[-1]

    # 255: white, 0: black
    input_image = np.full((whole_size,whole_size,3), 255)
    mask_image = np.full((whole_size,whole_size,3), 255)
    top_left_image = cv2.imread(top_left_path) # 512 * 512 size
    top_right_image = cv2.imread(top_right_path) # 512 * 512 size
    bottom_left_image = cv2.imread(bottom_left_path) # 512 * 512 size

    input_image[0:margin, 0:margin] = top_left_image[-margin:, -margin:]
    input_image[0:margin, margin:] = top_right_image[-margin:, :inpaint_size]
    input_image[margin:, 0:margin] = bottom_left_image[:inpaint_size, -margin:]

    # mask_image[0:margin, 0:margin].fill(0)
    # mask_image[0:margin, margin:].fill(0)
    # mask_image[margin:, 0:margin].fill(0)
    for i, r in enumerate(input_image):
        for j, p in enumerate(r):
            if sum(p) != 255*3:
                mask_image[i][j].fill(0)
                

    cv2.imwrite(top_left_path[:-len(extension)-1]+'_input.'+extension,input_image)
    cv2.imwrite(top_left_path[:-len(extension)-1]+'_mask.'+extension,mask_image)

if __name__ == '__main__':
    main()
