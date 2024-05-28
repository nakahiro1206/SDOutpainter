import time
import torch
from diffusers import StableDiffusionInpaintPipeline, UniPCMultistepScheduler
from diffusers.utils import load_image

def main(input_image, mask_image):
    s = time.time()

    print("start loading")
    # download model. 
    torch.backends.cuda.matmul.allow_tf32 = True
    pipeline = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting",
    )
    # pipeline = StableDiffusionInpaintPipeline.from_pretrained(
    #     "Sanster/anything-4.0-inpainting",
    #     use_safetensors=True,
    # )
    pipeline.safety_checker = None
    
    # reduce memory usage.
    pipeline.scheduler = UniPCMultistepScheduler.from_config(pipeline.scheduler.config)
    print("model download complete: ", time.time()-s)

    # mask_image = pipeline.mask_processor.blur(mask_image, blur_factor=33)
    width, height = input_image.size
    print("image load complete: ", time.time()-s)

    print("generation start")
    # generate image and save.
    prompt = "cute, cartoon, picture" # cartoon, picturebook, fairy tale. 
    negative_prompt = "ugly, realistic"

    pipeline.enable_vae_tiling()
    result_image = pipeline(prompt=prompt, 
                            negative_prompt=negative_prompt, 
                            image=input_image, 
                            mask_image=mask_image, 
                            height=height, 
                            width=width, 
                            num_inference_steps = 20
                            ).images[0]
    print("image generation complete: ", time.time()-s)

    return result_image.crop((width-512, height-512, width, height))

if __name__ == '__main__':
    main()
