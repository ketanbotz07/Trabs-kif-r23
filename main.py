import os
import random
import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips
from flask import Flask, request, jsonify

app = Flask(__name__)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def random_zoom(frame, zoom_factor):
    h, w, _ = frame.shape
    nw, nh = int(w / zoom_factor), int(h / zoom_factor)
    x = random.randint(0, w - nw)
    y = random.randint(0, h - nh)
    cropped = frame[y:y+nh, x:x+nw]
    return cv2.resize(cropped, (w, h))


def transform_clip(clip):
    zoom = random.uniform(1.05, 1.25)

    def process(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = random_zoom(frame, zoom)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    return clip.fl_image(process)


@app.route("/process", methods=["POST"])
def process_video():
    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video = request.files["video"]
    input_path = os.path.join(UPLOAD_DIR, video.filename)
    output_path = os.path.join(OUTPUT_DIR, f"out_{video.filename}")

    video.save(input_path)

    clip = VideoFileClip(input_path)
    duration = clip.duration

    clips = []
    start = 0
    while start < duration:
        seg = random.uniform(1.5, 3.0)
        end = min(start + seg, duration)
        sub = clip.subclip(start, end)
        clips.append(transform_clip(sub))
        start = end

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return jsonify({"message": "Video processed", "output": output_path})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
