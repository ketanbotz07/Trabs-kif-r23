import os, random, subprocess
from config import TEMP_DIR


def transform_all(segments):
out_dir = f"{TEMP_DIR}/edited"
os.makedirs(out_dir, exist_ok=True)
outputs = []


for i, seg in enumerate(segments):
zoom = round(random.uniform(1.05, 1.15), 2)
speed = round(random.uniform(0.97, 1.05), 2)
out = f"{out_dir}/edit_{i:03d}.mp4"


cmd = [
"ffmpeg", "-i", seg,
"-vf", f"scale=1080:1920,zoompan=z={zoom}",
"-filter:a", f"atempo={speed}",
out
]
subprocess.run(cmd, check=True)
outputs.append(out)


return outputs
