import random
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx

def transform_video(input_path, output_path):
    clip = VideoFileClip(input_path)

    # max 2 minutes
    clip = clip.subclip(0, min(120, clip.duration))

    segments = []
    t = 0

    while t < clip.duration:
        dur = random.uniform(3, 6)
        seg = clip.subclip(t, min(t + dur, clip.duration))

        # zoom
        seg = seg.resize(random.uniform(1.03, 1.08))

        # mirror sometimes
        if random.choice([True, False]):
            seg = seg.fx(vfx.mirror_x)

        # speed change
        seg = seg.fx(vfx.speedx, random.uniform(0.95, 1.05))

        segments.append(seg)
        t += dur

    final = concatenate_videoclips(segments, method="compose")

    # blur + noise
    def frame_fx(frame):
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        noise = np.random.randint(0, 10, frame.shape, dtype="uint8")
        return cv2.add(frame, noise)

    final = final.fl_image(frame_fx)

    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=2
    )
