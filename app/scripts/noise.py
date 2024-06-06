# source
# https://github.com/lkwq007/stablediffusion-infinity/blob/master/utils.py
import numpy as np

##########
# https://stackoverflow.com/questions/42147776/producing-2d-perlin-noise-with-numpy/42154921#42154921
def perlin(x, y, seed=0):
    # permutation table
    seed = np.random.randint(np.iinfo(np.uint32).max)
    np.random.seed(seed)
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p, p]).flatten()

    # coordinates of the top-left
    xi, yi = x.astype(int), y.astype(int)

    # internal coordinates
    xf, yf = x - xi, y - yi

    # fade factors
    u, v = fade(xf), fade(yf)

    # noise components
    n00 = gradient(p[p[xi] + yi], xf, yf)
    n01 = gradient(p[p[xi] + yi + 1], xf, yf - 1)
    n11 = gradient(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
    n10 = gradient(p[p[xi + 1] + yi], xf - 1, yf)

    # combine noises
    x1 = lerp(n00, n10, u)
    x2 = lerp(n01, n11, u)  # FIX1: I was using n10 instead of n01
    return lerp(x1, x2, v)  # FIX2: I also had to reverse x1 and x2 here

def lerp(a, b, x):
    "linear interpolation"
    return a + x * (b - a)

def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3

def gradient(h, x, y):
    "grad converts h to the right gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y
##########

def perlin_noise(img, mask):
    lin_x = np.linspace(0, 5, mask.shape[1], endpoint=False)
    lin_y = np.linspace(0, 5, mask.shape[0], endpoint=False)
    x, y = np.meshgrid(lin_x, lin_y)

    noise = [((perlin(x, y) + 1) * 0.5 * 255).astype(np.uint8) for i in range(3)]
    # print("noise", noise.shape)
    noise = np.stack(noise, axis=-1)
    print("noise-stack", noise.shape)
    print("mask", mask.shape)
    
    # expand mask to the empty area in input image
    nmask = mask.copy()
    nmask[mask > 0] = 1
    # はみ出し.
    # 白い点（RGB全てが255）のマスクを作成
    white_points = np.all(img == [255, 255, 255], axis=-1)

    # mask のその場所を [0, 0, 0] にする
    nmask[white_points] = [1, 1, 1]
    # mask も減らす？.
    mask[white_points] = [255, 255, 255]

    img = (1 - nmask) * img + nmask * noise
    return img.astype(np.uint8), mask.astype(np.uint8)

def gaussian_noise(img, mask):
    noise = np.random.randn(mask.shape[0], mask.shape[1], 3)
    noise = (noise + 1) / 2 * 255
    noise = noise.astype(np.uint8)
    nmask = mask.copy()
    nmask[mask > 0] = 1
    img = (1 - nmask) * img + nmask * noise
    return img.astype(np.uint8), mask.astype(np.uint8)