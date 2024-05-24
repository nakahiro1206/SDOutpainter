# pip install diffusers transformers accelerate torch scipy safetensors omegaconf
import sys
argv = sys.argv
img_size = int(argv[1])
inference = int(argv[2])
import time
s = time.time()

print("start loading")
# download model. 
import diffusers
pipe = diffusers.StableDiffusionPipeline.from_pretrained("admruul/anything-v3.0")
pipe.safety_checker = None
print("download complete: ", time.time()-s)

print("generation start")
# generate image and save.
result = pipe(prompt = "girl eating pizza", width  = img_size, height = img_size, num_inference_steps = inference)
result.images[0].save("pizza_"+str(img_size)+"_"+str(inference)+".png")
print("generation and save complete", time.time()-s)

"""
vis

from diffusers import StableDiffusionPipeline
import torch

model = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", revision="fp16", torch_dtype=torch.float16)
model = model.to("cuda")    
def callback(iter, t, latents):
    with torch.no_grad():
        latents = 1 / 0.18215 * latents
        image = model.vae.decode(latents).sample

        image = (image / 2 + 0.5).clamp(0, 1)

        image = image.cpu().permute(0, 2, 3, 1).float().numpy()

        image = model.numpy_to_pil(image)
        plt.figure()
        plt.imshow(image[0])
        plt.show()       

prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
image = model(prompt, callback=callback, callback_steps=5)
"""