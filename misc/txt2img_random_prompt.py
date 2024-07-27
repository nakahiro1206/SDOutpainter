# pip install diffusers transformers accelerate torch scipy safetensors omegaconf
import time
import random
import sys

args = sys.argv
# assert len(args) == 2

img_size = 512
inference = 20
s = time.time()

print("start loading")
# download model. 
import diffusers
pipe = diffusers.StableDiffusionPipeline.from_pretrained("admruul/anything-v3.0")
pipe.safety_checker = None
print("download complete: ", time.time()-s)

word_file = 'nouns.txt'
words = open(word_file).read().splitlines()
length = len(words)
prompt = ""
tokens = 0
for _ in range(40):
    idx = random.randint(0, length - 1)
    prompt += f"{words[idx]};"

prompt = args[1]

"""
# 2. Forward embeddings and negative embeddings through text encoder
prompt = 25 * "a photo of an astronaut riding a horse on mars"
max_length = pipe.tokenizer.model_max_length

input_ids = pipe.tokenizer(prompt, return_tensors="pt").input_ids
input_ids = input_ids.to("cuda")

negative_ids = pipe.tokenizer("", truncation=False, padding="max_length", max_length=input_ids.shape[-1], return_tensors="pt").input_ids                                                                                                     
negative_ids = negative_ids.to("cuda")

concat_embeds = []
neg_embeds = []
for i in range(0, input_ids.shape[-1], max_length):
    concat_embeds.append(pipe.text_encoder(input_ids[:, i: i + max_length])[0])
    neg_embeds.append(pipe.text_encoder(negative_ids[:, i: i + max_length])[0])

prompt_embeds = torch.cat(concat_embeds, dim=1)
negative_prompt_embeds = torch.cat(neg_embeds, dim=1)
"""


print(prompt)

print("generation start")
# generate image and save.
result = pipe(prompt = prompt, width  = img_size, height = img_size, num_inference_steps = inference)
result.images[0].save(f"{str(time.time())}.png")
print("generation and save complete", time.time()-s)

# cache location
# ~/.cache/huggingface/hub/models--admruul--anything-v3.0