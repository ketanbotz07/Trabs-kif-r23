import subprocess


def get_duration(path):
result = subprocess.run([
"ffprobe", "-v", "error",
"-show_entries", "format=duration",
"-of", "default=noprint_wrappers=1:nokey=1",
path
], stdout=subprocess.PIPE)
return float(result.stdout)
