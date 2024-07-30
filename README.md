# SDOutpainter
Outpaint with stable diffusion inpainting model.
This repository is image generation part of a collaborative drawing application with AI agent.
See [front end](https://github.com/hrm1810884/works-hai-frontend) and [back end](https://github.com/hrm1810884/works-hai-backend) from here.

## Notable functions
SDOutpainter does require prompt and the rims of images that should be the neighbors.
It creates seamlessly connected image with the limited information.

### Demonstration
Input source is 1/8 areas of left image(girl eating pizza) and right image(nurses in hospital) and prompt: *"A surreal dreamscape with floating islands, cascading waterfalls into the void, and fantastical creatures soaring through a colorful, ethereal sky."*

![demo](https://github.com/nakahiro1206/SDOutpainter/blob/main/assets/Screenshot%202024-07-31%20at%200.59.20.png)

### Challenges I tackled

#### How to enable seamless inpainting?
Different from usual inpainting, SDOutpainter draws much larger pictures than input image sources.
You cannot expect good performance if you simply create input and mask and execute stable diffusion pipeline.

To enable seamless inpainting, it pre-paint the area to be inpainted.
Workflow is like this.

* Reiterate the periphrals of neighboring images\
Inpainting on empty space does not perform well. So I need to convey the texture of input images. To keep continuity, the arangement of copied images is {original, flipped, original,,,} vertically or horizontally.

* Merge neighbors\
In case neighboring images have different texture, I need to carefully merge the reiterated images to retain each texture even after merged.

I adopted a function to calculate blend proportion.
```math
\displaylines{
P_{i}(h, w) = \frac{D_i}{\sum_{available\ j} D_j}\\
\begin{cases}
\ D_{left} = \frac{1}{w}\\
D_{right} = \frac{1}{W-w}\\
D_{up} = \frac{1}{h}\\
D_{down} = \frac{1}{H-h}
\end{cases}
}

```

Note that unavailable input sources because they are not passed as arguments should be dismissed.

Here is 3D plot of proportion of left image when left and right are available. Check out that P ~= 1 when x = 0 (it means w = 0, left side), and P ~= 0 when y = 0 (it means h = 0, right side), and average P ~= 0.5(merged in balance)

![3d_plot](https://github.com/nakahiro1206/SDOutpainter/blob/main/assets/Screenshot%202024-07-31%20at%201.59.35.png)

Here are the reiterated images to which the proportion filter is applied. Above is the left image and below is the right image used in demo section.

![left](https://github.com/nakahiro1206/SDOutpainter/blob/main/assets/left.png)
![right](https://github.com/nakahiro1206/SDOutpainter/blob/main/assets/right.png)

And here is the merged result. This image have texture of all the input images and the continuity on the edges. Pre-painting will be very helpful for AI's inpainting.

![pre-painted](https://github.com/nakahiro1206/SDOutpainter/blob/main/assets/input.png)

#### Prompt engineering(I'm still working on.)
SDOutpainter uses "runwayml/stable-diffusion-inpainting", which requires prompt engineering to perform better.
Temporary implementation is to manually type the ChatGPT-generated prompt or create random word arrangement. The latter method did not perform well.
I'm going to adopt [prompt enhancement with LLM](https://huggingface.co/docs/diffusers/en/using-diffusers/weighted_prompts)

## Tutorial

### Environment
OS: M2 chip MacBookAir.\
conda: Python 3.10.10
```
conda create --name <ENV_NAME>
conda activate <ENV_NAME>
```

### Install required packages
```
pip install diffusers transformers accelerate torch scipy safetensors omegaconf flask flask_cors Pillow
```

### Launch local server
```
cd SDOutpainter/app
python3 main.py
```

### Send a request
Open a new terminal window.
Move to input image folder and send a post request like this.
```
curl -X POST http://127.0.0.1:2000/human-drawing -F left=@path_to_image -F up=@ipath_to_image -F --output out.png
```
Available arguments to describe image positions are:
* up
* left
* right
* down
* up_left
* up_right
* down_left
* down_right

If you don't give any argument, Perlin noise is applied to the area to be inpainted instead.

Generated image (ByteIO) will be sent to out.png
