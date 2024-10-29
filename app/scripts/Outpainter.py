import time
import torch
from diffusers import StableDiffusionInpaintPipeline, UniPCMultistepScheduler
from io import BytesIO
from scripts.make_mask import make_mask, make_mask_for_boundary
from scripts.select_words4prompt import gen_prompt

class Outpainter:
    def __init__(self) -> None:
        """download model. """
        torch.backends.cuda.matmul.allow_tf32 = True # what does it mean

        pipeline = StableDiffusionInpaintPipeline.from_pretrained("stabilityai/stable-diffusion-2-inpainting")
        # pipeline = StableDiffusionInpaintPipeline.from_pretrained(
        #     "runwayml/stable-diffusion-inpainting",
        #     # float 32 by default
        #     # if necessary change to float16
        #     # torch_dtype=torch.float16,
        #     # use_safetensors=True,
        # )
        pipeline.safety_checker = None
        print("start loading")

        # reduce memory usage.
        pipeline.scheduler = UniPCMultistepScheduler.from_config(pipeline.scheduler.config)
        pipeline.enable_vae_tiling()

        if torch.cuda.is_available():
            pipeline = pipeline.to("cuda")
        
        self.pipeline = pipeline


    def call(self, image_map = None) -> BytesIO:
        """
        image_map: FileStorage[] or String[]
        """
        start = time.time()
        if image_map is None:
            exit("image map should be list")
        if len(image_map) != 9:
            exit("image map should have 9 image path")

        input_image, mask_image, left, up, right, down = make_mask(image_map)
        print("image masking complete: ")
        
        # generate image and save.
        print("generation start")

        prompt = gen_prompt()
        print("prompt: " + prompt)
        negative_prompt = "ugly, deformed"
        width, height = input_image.size

        result_image = input_image
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
        result_image.save("img/uncropped.png")

        # # make another mask for seamless connection of the images
        # input_image_without_boundary, mask_image_boundary_only = make_mask_for_boundary(result_image, mask_image, left, up, right, down)
        # result_image = self.pipeline(
        #      prompt="", 
        #      negative_prompt="", 
        #      image=input_image_without_boundary, 
        #      mask_image=mask_image_boundary_only, 
        #      height=height, 
        #      width=width, 
        #      num_inference_steps = 20
        #     ).images[0]

        # exclude masked area
        cropped_result = result_image.crop((left, up, right, down))

        # Image from Pillow
        img_io = BytesIO() # or StryingIO
        cropped_result.save(img_io, 'PNG')
        cropped_result.save("img/out.png", 'PNG')
        img_io.seek(0)
        
        print(time.time()-start)
        return img_io