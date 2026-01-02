import subprocess, os
from config import TEMP_DIR


def merge_all(videos):
list_file = f"{TEMP_DIR}/list.txt"
with open(list_file, "w") as f:
for v in videos:
f.write(f"file '{v}'
")


output = f"{TEMP_DIR}/final.mp4"
subprocess.run([
"ffmpeg", "-f", "concat", "-safe", "0",
"-i", list_file, "-c", "copy", output
], check=True)


return output
