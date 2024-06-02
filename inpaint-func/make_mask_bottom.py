import cv2
import numpy as np

def main():
    margin = 128
    inpaint_size = 1024
    whole_size = inpaint_size + margin

    # 255: white, 0: black
    input_image = np.full((whole_size,whole_size,3), 255)
    mask_image = np.full((whole_size,whole_size,3), 255)
    upper_image = cv2.imread("./dog.png") # 1024 * 1024 size
    left_image = cv2.imread("./pale.png") # 1024 * 1024 size

    # trace input
    input_image[0:margin, margin:] = upper_image[-margin:, :]
    input_image[margin:, 0:margin] = left_image[:, -margin:]

    # fill mask
    mask_image[0:margin, margin:].fill(0)
    mask_image[margin:, 0:margin].fill(0)
    mask_image[:margin, :margin].fill(0)                

    cv2.imwrite('bottom_input.png',input_image)
    cv2.imwrite('bottom_mask.png',mask_image)

if __name__ == '__main__':
    main()
