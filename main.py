import os
import random
import cv2
from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip, concatenate_videoclips

app = Flask(__name__)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Auto Video Transformer API is live",
        "endpoint": "/process",
        "method": "POST"
    })


def random_zoom(frame, zoom_factor):
    h, w, _ = frame.shape
    nw, nh = int(w / zoom_factor), int(h / zoom_factor)
    x = random.randint(0, w - nw)
    y = random.randint(0, h - nh)
    frame = frame[y:y + nh, x:x + nw]
    return cv2.resize(frame, (w, h))


def transform_clip(clip):
    zoom = random.uniform(1.05, 1.2)

    def process(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = random_zoom(frame, zoom)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    return clip.fl_image(process)


@app.route("/process", methods=["POST"])
def process_video():
    if "video" not in request.files:
        return jsonify({"error": "video file missing"}), 400

    file = request.files["video"]
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    output_path = os.path.join(OUTPUT_DIR, f"out_{file.filename}")
    file.save(input_path)

    clip = VideoFileClip(input_path)
    duration = clip.duration

    clips = []
    start = 0
    while start < duration:
        seg = random.uniform(1.5, 3.0)
        end = min(start + seg, duration)
        clips.append(transform_clip(clip.subclip(start, end)))
        start = end

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        threads=2
    )

    return jsonify({
        "status": "done",
        "output_file": output_path
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
