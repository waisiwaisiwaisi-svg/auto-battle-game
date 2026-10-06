# SDXL-Turbo（CPU）で モンスター画像を 生成する
# 使い方: ../sd/bin/python gen.py <id> <seed から> <枚数> "<プロンプト>"
import sys, os, time, torch
from diffusers import AutoPipelineForText2Image
HERE = os.path.dirname(os.path.abspath(__file__))
torch.set_num_threads(4)
pipe = AutoPipelineForText2Image.from_pretrained('stabilityai/sdxl-turbo', torch_dtype=torch.bfloat16, variant='fp16')
pipe.set_progress_bar_config(disable=True)
STYLE = ('pixel art game sprite, 16-bit SNES style, single cute fantasy monster, full body, side view facing right, '
         'chibi proportions, whole body visible, small in frame with wide empty margin, thick dark outline, cel shading, vibrant colors, plain white background, centered')
def gen(name, seed0, n, prompt, steps=4):
    os.makedirs(os.path.join(HERE, 'raw'), exist_ok=True)
    for s in range(seed0, seed0 + n):
        t = time.time()
        g = torch.Generator().manual_seed(s)
        im = pipe(prompt=prompt + ', ' + STYLE, num_inference_steps=steps, guidance_scale=0.0, generator=g, width=512, height=512).images[0]
        p = os.path.join(HERE, 'raw', f'{name}_{s}.png'); im.save(p)
        print(p, f'{time.time() - t:.1f}s', flush=True)
if __name__ == '__main__':
    gen(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 4)
