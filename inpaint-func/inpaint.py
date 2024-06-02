# pip install diffusers transformers accelerate torch scipy safetensors omegaconf
import time
import sys
import torch
from diffusers import StableDiffusionInpaintPipeline, UniPCMultistepScheduler
from diffusers.utils import load_image

def main():
    s = time.time()
    argv = sys.argv
    input_path = argv[1]
    mask_path = argv[2]
    extension = input_path.split('.')[-1]
    save_path = input_path[:-len("_input")-len(extension)-1]+'_result.'+extension

    def callback(iter, t, latents):
        with torch.no_grad():
            latents = 1 / 0.18215 * latents
            image = pipeline.vae.decode(latents).sample

            image = (image / 2 + 0.5).clamp(0, 1)

            image = image.cpu().permute(0, 2, 3, 1).float().numpy()

            image = pipeline.numpy_to_pil(image)

            image[0].save(input_path[:-len("_input")-len(extension)-1]+str(iter//10)+str(iter%10)+".png")

    print("start loading")
    # download model. 
    torch.backends.cuda.matmul.allow_tf32 = True
    pipeline = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting",
    )
    pipeline.safety_checker = None
    # reduce memory usage.
    pipeline.scheduler = UniPCMultistepScheduler.from_config(pipeline.scheduler.config)
    print("model download complete: ", time.time()-s)

    print("image load start")
    init_image = load_image(input_path)
    mask_image = load_image(mask_path)
    # mask_image = pipeline.mask_processor.blur(mask_image, blur_factor=33)
    height = init_image.size[0]
    width = init_image.size[1]
    print("image load complete: ", time.time()-s)

    print("generation start")
    # generate image and save.
    prompt = "cute, beautiful, 4k, high-quality" # "line drawing cartoon"
    negative_prompt = "ugly, cartoon"

    pipeline.enable_vae_tiling()
    result_image = pipeline(prompt=prompt, 
                            negative_prompt=negative_prompt, 
                            image=init_image, 
                            callback=callback, callback_steps=1,
                            mask_image = mask_image,
                            height=height, 
                            width=width, 
                            num_inference_steps = 20,
                            ).images[0]
    print("image generation complete: ", time.time()-s)
    result_image.save(save_path)
    print("image save complete: ", time.time()-s)

if __name__ == '__main__':
    main()
