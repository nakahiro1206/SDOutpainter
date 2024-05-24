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

# cache location
# ~/.cache/huggingface/hub/models--admruul--anything-v3.0