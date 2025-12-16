from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from video_processor import process_video
import uuid, os, time, threading


app = FastAPI()


progress = {}


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)


uid = str(uuid.uuid4())
input_path = f"input/{uid}.mp4"
output_path = f"output/{uid}_final.mp4"


with open(input_path, "wb") as f:
f.write(await file.read())


progress[uid] = 0


def run_process():
process_video(input_path, output_path, uid, progress)
progress[uid] = 100


threading.Thread(target=run_process).start()


return {"task_id": uid, "status": "processing"}


@app.get("/progress/{task_id}")
async def get_progress(task_id: str):
return {"progress": progress.get(task_id, 0)}
