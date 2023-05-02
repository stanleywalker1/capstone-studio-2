# stablediffusion-infinity-creative-sandbox

Infitnite/space is an interactive space for people to come together and collaborate on growning an image. The foundation of this project is based on this repo [stablediffusion-infinity by lkwq007](https://github.com/lkwq007/stablediffusion-infinity) and the concept is inspired by the Reddit project r/place - with the goal to foster creatvity and collaboration among people with generative AI. 

next steps:
- rearchitecture tool bar into styled css buttons/minimalistic design
- intergrate liveblocks.io
- redesign ui/ux
- configure host



![outpaint](infinite-place-hackathon-demo.jpeg)



https://user-images.githubusercontent.com/1665437/197244111-51884b3b-dffe-4dcf-a82a-fa5117c79934.mp4

## Status

Powered by Stable Diffusion inpainting model, this project now works well. However, the quality of results is still not guaranteed.
You may need to do prompt engineering, change the size of the selection, reduce the size of the outpainting region to get better outpainting results. 

The project now becomes a web app based on PyScript and Gradio. For Jupyter Notebook version, please check out the [ipycanvas](https://github.com/lkwq007/stablediffusion-infinity/tree/ipycanvas) branch. 

Pull requests are welcome for better UI control, ideas to achieve better results, or any other improvements.

Update: the project add photometric correction to suppress seams, to use this feature, you need to install [fpie](https://github.com/Trinkle23897/Fast-Poisson-Image-Editing): `pip install fpie` (Linux/MacOS only)

## Docs

### Get Started

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lkwq007/stablediffusion-infinity/blob/master/stablediffusion_infinity_colab.ipynb)
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/lnyan/stablediffusion-infinity)
[![Setup Locally](https://img.shields.io/badge/%F0%9F%96%A5%EF%B8%8F%20Setup-Locally-blue)](https://github.com/lkwq007/stablediffusion-infinity/blob/master/docs/setup_guide.md)

- Setup for Windows: [setup_guide](./docs/setup_guide.md#windows)
- Setup for Linux: [setup_guide](./docs/setup_guide.md#linux)
- Setup for MacOS: [setup_guide](./docs/setup_guide.md#macos)
- Running with Docker on Windows or Linux with NVIDIA GPU: [run_with_docker](./docs/run_with_docker.md)
- Usages: [usage](./docs/usage.md)

### FAQs

- The result is a black square: 
  - False positive rate of safety checker is relatively high, you may disable the safety_checker
  - Some GPUs might not work with `fp16`: `python app.py --fp32 --lowvram`
- What is the init_mode
  - init_mode indicates how to fill the empty/masked region, usually `patch_match` is better than others
- Why not use `postMessage` for iframe interaction
  - The iframe and the gradio are in the same origin. For `postMessage` version, check out [gradio-space](https://github.com/lkwq007/stablediffusion-infinity/tree/gradio-space) version

### Known issues

- The canvas is implemented with `NumPy` + `PyScript` (the project was originally implemented with `ipycanvas` inside a jupyter notebook), which is relatively inefficient compared with pure frontend solutions. 
- By design, the canvas is infinite. However, the canvas size is **finite** in practice. Your RAM and browser limit the canvas size. The canvas might crash or behave strangely when zoomed out by a certain scale. 
- The canvas requires internet: You can deploy and serve PyScript, Pyodide, and other JS/CSS assets with a local HTTP server and modify `index.html` accordingly. 
- Photometric correction might not work (`taichi` does not support the multithreading environment). A dirty hack (quite unreliable) is implemented to move related computation inside a subprocess. 
- Stable Diffusion inpainting model is much slower when selection size is larger than 512x512

## Credit

The code of `perlin2d.py` is from https://stackoverflow.com/questions/42147776/producing-2d-perlin-noise-with-numpy/42154921#42154921 and is **not** included in the scope of LICENSE used in this repo.

The submodule `glid_3_xl_stable` is based on https://github.com/Jack000/glid-3-xl-stable 

The submodule `PyPatchMatch` is based on https://github.com/vacancy/PyPatchMatch

The code of `postprocess.py` and `process.py` is modified based on https://github.com/Trinkle23897/Fast-Poisson-Image-Editing

The code of `convert_checkpoint.py` is modified based on https://github.com/huggingface/diffusers/blob/main/scripts/convert_original_stable_diffusion_to_diffusers.py

The submodule `sd_grpcserver` and `handleImageAdjustment()` in `utils.py` are based on https://github.com/hafriedlander/stable-diffusion-grpcserver and https://github.com/parlance-zz/g-diffuser-bot

`w2ui.min.js` and `w2ui.min.css` is from https://github.com/vitmalina/w2ui. `fabric.min.js` is a custom build of https://github.com/fabricjs/fabric.js

`interrogate.py` is based on https://github.com/pharmapsychotic/clip-interrogator v1, the submodule `blip_model` is based on https://github.com/salesforce/BLIP 
