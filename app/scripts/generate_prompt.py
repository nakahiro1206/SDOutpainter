## section 1.
import torch
from transformers import GenerationConfig, GPT2LMHeadModel, GPT2Tokenizer, LogitsProcessor, LogitsProcessorList
from diffusers import StableDiffusionXLPipeline

def find_and_order_pairs(s):
    pairs = ["highly detailed", "high quality", "enhanced quality", "perfect composition", "dynamic light"]
    # if pairs = ["highly detailed", ]
    words = s.split()
    found_pairs = []
    for pair in pairs: # pair = "hightly detailed"
        pair_words = pair.split() # pair_words = ["highly", "detailed"]
        if pair_words[0] in words and pair_words[1] in words: # words has "highly" and "detailed"
            found_pairs.append(pair) # add "hightly detailed"
            words.remove(pair_words[0])
            words.remove(pair_words[1])

    for word in words[:]:
        for pair in pairs:
            if word in pair.split():
                words.remove(word)
                break

    ordered_pairs = ", ".join(found_pairs)
    remaining_s = ", ".join(words)
    return ordered_pairs, remaining_s

## section 3.
class CustomLogitsProcessor(LogitsProcessor):
    def __init__(self, bias):
        super().__init__()
        self.bias = bias

    def __call__(self, input_ids, scores):
        if len(input_ids.shape) == 2:
            last_token_id = input_ids[0, -1]
            self.bias[last_token_id] = -1e10
        return scores + self.bias
    
def format_prompt(prompt, style):
    styles = {
        "cinematic": "cinematic film still of {prompt}, highly detailed, high budget hollywood movie, cinemascope, moody, epic, gorgeous, film grain",
        "anime": "anime artwork of {prompt}, anime style, key visual, vibrant, studio anime, highly detailed",
        "photographic": "cinematic photo of {prompt}, 35mm photograph, film, professional, 4k, highly detailed",
        "comic": "comic of {prompt}, graphic illustration, comic art, graphic novel art, vibrant, highly detailed",
        "lineart": "line art drawing {prompt}, professional, sleek, modern, minimalist, graphic, line art, vector graphics",
        "pixelart": " pixel-art {prompt}, low-res, blocky, pixel art style, 8-bit graphics",
    }
    ## section 4.　generate prompt. 
    res = styles[style].format(prompt=prompt)
    print(res)
    "cinematic film still of a cat basking in the sun on a roof in Turkey, highly detailed, high budget hollywood movie, cinemascope, moody, epic, gorgeous, film grain"
    return res

def setup_processor_list(tokenizer):
    words = [
        "aesthetic", "astonishing", "beautiful", "breathtaking", "composition", "contrasted", "epic", "moody", "enhanced",
        "exceptional", "fascinating", "flawless", "glamorous", "glorious", "illumination", "impressive", "improved",
        "inspirational", "magnificent", "majestic", "hyperrealistic", "smooth", "sharp", "focus", "stunning", "detailed",
        "intricate", "dramatic", "high", "quality", "perfect", "light", "ultra", "highly", "radiant", "satisfying",
        "soothing", "sophisticated", "stylish", "sublime", "terrific", "touching", "timeless", "wonderful", "unbelievable",
        "elegant", "awesome", "amazing", "dynamic", "trendy",
    ]
    word_ids = [tokenizer.encode(word, add_prefix_space=True)[0] for word in words]

    bias = torch.full((tokenizer.vocab_size,), -float("Inf"))
    if torch.cuda.is_available():
        bias = bias.to("cuda")
    bias[word_ids] = 0

    processor = CustomLogitsProcessor(bias)
    processor_list = LogitsProcessorList([processor])
    return processor_list
    
def main():
    # setup format.
    

    prompt = format_prompt(prompt = "hanged girl on the tree", style = "cinematic")

    ## section 2.

    tokenizer = GPT2Tokenizer.from_pretrained("Gustavosta/MagicPrompt-Stable-Diffusion")

    processor_list = setup_processor_list(tokenizer)

    ## section 5.
    model = GPT2LMHeadModel.from_pretrained("Gustavosta/MagicPrompt-Stable-Diffusion", torch_dtype=torch.float16)
    if torch.cuda.is_available():
        model = model.to("cuda")
    model.eval()

    inputs = tokenizer(prompt, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = inputs.to("cuda")

    token_count = inputs["input_ids"].shape[1]
    max_new_tokens = 50 - token_count

    generation_config = GenerationConfig(
        penalty_alpha=0.7,
        top_k=50,
        eos_token_id=model.config.eos_token_id,
        pad_token_id=model.config.eos_token_id,
        pad_token=model.config.pad_token_id,
        do_sample=True,
    )

    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=max_new_tokens,
            generation_config=generation_config,
            logits_processor=processor_list,
        )

    ## section 6. enhance prompt.
    output_tokens = [tokenizer.decode(generated_id, skip_special_tokens=True) for generated_id in generated_ids]
    input_part, generated_part = output_tokens[0][: len(prompt)], output_tokens[0][len(prompt) :]
    print(input_part)
    print(generated_part)

    # order keywords for style
    pairs, words = find_and_order_pairs(generated_part)
    formatted_generated_part = pairs + ", " + words

    enhanced_prompt = input_part + ", " + formatted_generated_part
    print(enhanced_prompt)
    ["cinematic film still of a cat basking in the sun on a roof in Turkey, highly detailed, high budget hollywood movie, cinemascope, moody, epic, gorgeous, film grain quality sharp focus beautiful detailed intricate stunning amazing epic"]

if __name__ == '__main__':
    main()

exit()
## section 7. generate image.
pipeline = StableDiffusionXLPipeline.from_pretrained(
    "RunDiffusion/Juggernaut-XL-v9", torch_dtype=torch.float16, variant="fp16"
).to("cuda")

pipeline.load_lora_weights(
    "stabilityai/stable-diffusion-xl-base-1.0",
    weight_name="sd_xl_offset_example-lora_1.0.safetensors",
    adapter_name="offset",
)
pipeline.set_adapters(["offset"], adapter_weights=[0.2])

"""image = pipeline(
    enhanced_prompt,
    width=1152,
    height=896,
    guidance_scale=7.5,
    num_inference_steps=25,
).images[0]"""

# https://qiita.com/taka_yayoi/items/17be2b5f7136c4af86e9
