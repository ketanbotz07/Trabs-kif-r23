import os, subprocess
from config import SEGMENT_TIME, TEMP_DIR


def split_video(input_video):
out_dir = f"{TEMP_DIR}/segments"
os.makedirs(out_dir, exist_ok=True)


cmd = [
"ffmpeg", "-i", input_video,
"-map", "0",
"-segment_time", str(SEGMENT_TIME),
"-f", "segment",
f"{out_dir}/seg_%03d.mp4"
]
subprocess.run(cmd, check=True)


return [f"{out_dir}/" + f for f in
