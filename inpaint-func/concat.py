import cv2
import numpy as np

def main():
    whole_size = 2048
    margin = 1024

    # 255: white, 0: black
    input_image = np.full((whole_size,whole_size,3), 255)

    upper_image = cv2.imread("./dog.png") # 1024 * 1024 size
    left_image = cv2.imread("./pale.png") # 1024 * 1024 size

    upper_gen = cv2.imread("./upper_result.png")
    bottom_gen = cv2.imread("./bottom_result.png")

    # trace input
    input_image[0:margin, margin:] = upper_image
    input_image[margin:, 0:margin] = left_image 

    input_image[0:margin, 0:margin] = upper_gen[0:margin, 0:margin]
    input_image[margin:, margin:] = bottom_gen[128:, 128:]

    cv2.imwrite('concat_result.png',input_image)

if __name__ == '__main__':
    main()
