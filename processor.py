import os, random, math, subprocess
from .config import *
from .utils import get_duration


os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)




def process_video(input_path, output_path):
duration = get_duration(input_path)
segments = math.ceil(duration / SEGMENT_TIME)
files = []


for i in range(segments):
start = i * SEGMENT_TIME
zoom = random.choice([1.18, 1.19, 1.20])
speed = random.choice([0.97, 1.03])
x = random.randint(-8, 8)
y = random.randint(-6, 6)


seg = f"{TEMP_DIR}/seg_{i}.mp4"
files.append(seg)


subprocess.run([
"ffmpeg", "-y",
"-ss", str(start), "-t", str(SEGMENT_TIME),
"-i", input_path,
"-vf", f"scale=iw*{zoom}:ih*{zoom},crop=iw:ih:{x}:{y}",
"-filter:v", f"setpts=PTS/{speed}",
"-preset", "veryfast",
"-crf", "23",
seg
])


with open(f"{TEMP_DIR}/list.txt", "w") as f:
for s in files:
f.write(f"file '{os.path.abspath(s)}'\n")


subprocess.run([
"ffmpeg", "-y",
"-f", "concat", "-safe", "0",
"-i", f"{TEMP_DIR}/list.txt",
"-vf", f"scale={TARGET_WIDTH}:{TARGET_HEIGHT}",
"-preset", "veryfast",
"-crf", "23",
output_path
])
