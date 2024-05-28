import torch
from diffusers import StableCascadeCombinedPipeline

pipe = StableCascadeCombinedPipeline.from_pretrained("stabilityai/stable-cascade", variant="bf16", torch_dtype=torch.bfloat16)

prompt = "an image of a shiba inu, donning a spacesuit and helmet"
pipe(
    prompt=prompt,
    negative_prompt="",
    num_inference_steps=10,
    prior_num_inference_steps=20,
    prior_guidance_scale=3.0,
    width=1024,
    height=1024,
).images[0].save("cascade-combined.png")

"""
Note: You are able to define your own masks with the mask parameter or for demonstration purposes, use what we do during training to generate masks: use a tiny saliency model to predict the area of "interesting content", like an animal, a person, an object etc. This results in masks that closely mimic how humans actually inpaint, can be calculated extremely fast and with just a few lines of code. You have two parameters to control the masks threshold and outpaint. The former determines how much area will be masked and outpaint would just flip the predicted mask. Just play around with the parameters and you will get a feeling for it (theshold should be between 0.0 and 0.4). If you do wish, to load your own masks, just uncomment the mask parameter and replace it with your own.
"""

batch_size = 4
url = "https://cdn.discordapp.com/attachments/1121232062708457508/1204787053892603914/cat_dog.png?ex=65d60061&is=65c38b61&hm=37c3d179a39b1eca4b8894e3c239930cedcbb965da00ae2209cca45f883f86f4&"
images = resize_image(download_image(url)).unsqueeze(0).expand(batch_size, -1, -1, -1)

batch = {'images': images}

mask = None
# mask = torch.ones(batch_size, 1, images.size(2), images.size(3)).bool()

outpaint = False
threshold = 0.2

with torch.no_grad(), torch.cuda.amp.autocast(dtype=torch.bfloat16):
    cnet, cnet_input = core.get_cnet(batch, models, extras, mask=mask, outpaint=outpaint, threshold=threshold)
    cnet_uncond = cnet
    
show_images(batch['images'])
show_images(cnet_input)
