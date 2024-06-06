import time
import torch
from diffusers import StableDiffusionInpaintPipeline, UniPCMultistepScheduler
from io import BytesIO
from scripts.make_mask import make_mask
from scripts.prompt import prompt_generate, negative_prompt_generate

class Outpainter:
    def __init__(self) -> None:
        """download model. """
        torch.backends.cuda.matmul.allow_tf32 = True # what does it mean
        pipeline = StableDiffusionInpaintPipeline.from_pretrained(
            "runwayml/stable-diffusion-inpainting",
            # float 32 by default
            # if necessary change to float16
            # torch_dtype=torch.float16,
            # use_safetensors=True,
        )
        pipeline.safety_checker = None
        print("start loading")
        # reduce memory usage.
        pipeline.scheduler = UniPCMultistepScheduler.from_config(pipeline.scheduler.config)
        pipeline.enable_vae_tiling()
        self.pipeline = pipeline


    def call(self, image_map = None) -> BytesIO:
        """
        image_map: FileStorage[]
        """
        start = time.time()
        if image_map is None:
            exit("image map should be list")
        if len(image_map) != 9:
            exit("image map should have 9 image path")

        input_image, mask_image = make_mask(image_map)
        # mask_image = pipeline.mask_processor.blur(mask_image, blur_factor=33)
        print("image masking complete: ")
        
        # generate image and save.
        print("generation start")

        prompt = prompt_generate()
        negative_prompt = negative_prompt_generate()
        width, height = input_image.size

        result_image = self.pipeline(
             prompt=prompt, 
             negative_prompt=negative_prompt, 
             image=input_image, 
             mask_image=mask_image, 
             height=height, 
             width=width, 
             num_inference_steps = 20
            ).images[0]

        print("image generation complete")
        # exclude not-masked area
        print("CROP HERE!!!")
        # cropped_result = result_image.crop((width-512, height-512, width, height))

        # Image from Pillow
        img_io = BytesIO() # or StryingIO
        result_image.save(img_io, 'PNG')
        result_image.save("img/out.png", 'PNG')
        img_io.seek(0)
        
        print(time.time()-start)
        return img_io
    
if __name__ == '__main__':
    pass
