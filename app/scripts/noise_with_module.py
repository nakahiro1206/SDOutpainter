## make noise with perlin_noise module
from perlin_noise import PerlinNoise
from sklearn.preprocessing import minmax_scale
import numpy as np
def perlin_noise2(img, mask):  
  height = img.shape[0]
  width = img.shape[1]
  noise11 = PerlinNoise(octaves=10)
  noise12 = PerlinNoise(octaves=5)

  noise21 = PerlinNoise(octaves=10)
  noise22 = PerlinNoise(octaves=5)

  noise31 = PerlinNoise(octaves=10)
  noise32 = PerlinNoise(octaves=5)


  def noise_mult_1(i,j, xpix=height,ypix=width):
    return noise11([i/xpix, j/ypix]) + 0.5 * noise12([i/xpix, j/ypix]) 

  def noise_mult_2(i,j, xpix=height,ypix=width):
    return noise21([i/xpix, j/ypix]) + 0.5 * noise22([i/xpix, j/ypix]) 

  def noise_mult_3(i,j, xpix=height,ypix=width):
    return noise31([i/xpix, j/ypix]) + 0.5 * noise32([i/xpix, j/ypix]) 

  pic = [[[noise_mult_1(i,j), noise_mult_2(i,j), noise_mult_3(i,j) ] for j in range(width)] for i in range(height)]
  scaled_noise = minmax_scale(np.array(pic).flatten(), (0,255)).reshape((height,width, 3))

  # expand mask to the empty area in input image
  nmask = mask.copy()
  nmask[mask > 0] = 1
  img = (1 - nmask) * img + nmask * scaled_noise

  return img.astype(np.uint8), mask.astype(np.uint8)
