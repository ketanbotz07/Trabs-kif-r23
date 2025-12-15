import os
import uuid
from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip, vfx

app = Flask(__name__)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# In-memory job status store
JOBS = {}

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Auto Video Transform Bot LIVE",
        "endpoints": {
            "process": "/process (POST)",
            "status": "/status/<job_id> (GET)"
        }
    })

@app.route("/status/<job_id>", methods=["GET"])
def job_status(job_id):
    if job_id not in JOBS:
        return jsonify({"error": "Invalid job id"}), 404
    return jsonify(JOBS[job_id])

@app.route("/process", methods=["POST"])
def process_video():
    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "queued"}

    file = request.files["video"]
    input_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    output_path = os.path.join(OUTPUT_DIR, f"out_{job_id}.mp4")

    file.save(input_path)

    try:
        JOBS[job_id]["status"] = "processing"

        clip = VideoFileClip(input_path)
        clip = clip.subclip(0, min(120, clip.duration))

        JOBS[job_id]["status"] = "transforming"

        clip = clip.fx(vfx.crop, x_center=clip.w/2, y_center=clip.h/2,
                       width=clip.w*0.9, height=clip.h*0.9)
        clip = clip.resize(1.1)

        JOBS[job_id]["status"] = "encoding"

        clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            threads=2,
            verbose=False,
            logger=None
        )

        JOBS[job_id]["status"] = "completed"
        JOBS[job_id]["output"] = output_path

        return jsonify({
            "job_id": job_id,
            "status": "completed",
            "output": output_path
        })

    except Exception as e:
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
