# pip install diffusers transformers accelerate torch scipy safetensors omegaconf
import time
import sys

def main():
    s = time.time()
    argv = sys.argv
    input_path = argv[1]
    mask_path = argv[2]
    extension = input_path.split('.')[-1]
    save_path = input_path[:-len("_input")-len(extension)-1]+'_result.'+extension

    print("start loading")
    # download model. 
    import torch
    from diffusers import StableDiffusionInpaintPipeline
    from diffusers.utils import load_image, make_image_grid
    # pipe = diffusers.StableDiffusionPipeline.from_pretrained("admruul/anything-v3.0")
    pipeline = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting"
    )
    pipeline.safety_checker = None
    # reduce memory usage.
    # pipeline.enable_model_cpu_offload()
    print("model download complete: ", time.time()-s)

    print("image load start")
    init_image = load_image(input_path)
    mask_image = load_image(mask_path)
    mask_image = pipeline.mask_processor.blur(mask_image, blur_factor=33)
    print("image load complete: ", time.time()-s)

    print("generation start")
    # generate image and save.
    prompt = "cartoon" # "line drawing cartoon"
    negative_prompt = ""
    result_image = pipeline(prompt=prompt, negative_prompt=negative_prompt, image=init_image, mask_image=mask_image, num_inference_steps = 20).images[0]
    print("image generation complete: ", time.time()-s)
    result_image.save(save_path)
    print("image save complete: ", time.time()-s)

    # show grid tiled image
    # make_image_grid([init_image, mask_image, image], rows=1, cols=3)

if __name__ == '__main__':
    main()
