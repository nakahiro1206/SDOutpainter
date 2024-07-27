# SDOutpainter
With stable diffusion inpaint, expand grid-tiled images

## install 手順

### OS: MacBook with M2 chip.

### conda create --name <NAME>
- maybe Python 3.12.3 is installed.

### install packages
pip install -r requirements.txt

### Launch local server with Flask
python3 main.py

curl -X POST http://127.0.0.1:2000/human-drawing -F left=@img/input.png -F up=@img/up.png -F up_left=@img/up_left.png

Like this, up_right, right, down_left, down, down_right is also available.

generated image (ByteIO) will be sent to out.png

cf) pip list in conda environment
```
Package                Version
---------------------- ---------
accelerate             0.30.1
antlr4-python3-runtime 4.9.3
Brotli                 1.0.9
certifi                2024.2.2
charset-normalizer     2.0.4
diffusers              0.27.2
filelock               3.13.1
fsspec                 2024.5.0
huggingface-hub        0.23.0
idna                   3.7
importlib_metadata     7.1.0
Jinja2                 3.1.3
MarkupSafe             2.1.3
mpmath                 1.3.0
networkx               3.1
numpy                  1.26.4
omegaconf              2.3.0
opencv-python          4.9.0.80
packaging              24.0
pillow                 10.3.0
pip                    24.0
psutil                 5.9.8
PySocks                1.7.1
PyYAML                 6.0.1
regex                  2024.5.15
requests               2.31.0
safetensors            0.4.3
scipy                  1.13.0
setuptools             69.5.1
sympy                  1.12
tokenizers             0.19.1
torch                  2.3.0
torchvision            0.18.0
tqdm                   4.66.4
transformers           4.40.2
typing_extensions      4.11.0
urllib3                2.2.1
wheel                  0.43.0
zipp                   3.18.1
```
