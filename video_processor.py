import random
from moviepy.editor import *
import cv2
import numpy as np

def transform_video(input_path, output_path):
    clip = VideoFileClip(input_path)

    clip = clip.subclip(0, min(120, clip.duration))

    segments = []
    t = 0

    while t < clip.duration:
        dur = random.uniform(3, 6)
        seg = clip.subclip(t, min(t + dur, clip.duration))

        seg = seg.resize(random.uniform(1.03, 1.08))

        if random.choice([True, False]):
            seg = seg.fx(vfx.mirror_x)

        seg = seg.fx(vfx.speedx, random.uniform(0.95, 1.05))

        segments.append(seg)
        t += dur

    final = concatenate_videoclips(segments, method="compose")

    def frame_fx(frame):
        frame = cv2.GaussianBlur(frame, (5,5), 0)
        noise = np.random.randint(0, 12, frame.shape, dtype='uint8')
        return cv2.add(frame, noise)

    final = final.fl_image(frame_fx)

    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=2
    )
  
