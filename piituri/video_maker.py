import cv2
import numpy as np

from piituri.settings import Settings


def make_video(route_points, tail, map_img, settings: Settings, i: int):
    output_name = f"{output_name}_{i}.mp4"
    print(f"writing video {output_name}", flush=True)
    video = cv2.VideoWriter(
        output_name, cv2.VideoWriter_fourcc(*'mp4v'), settings.fps, (settings.width, settings.height), isColor=True)
    for i, p in enumerate(route_points):
        if i % settings.fps == 0:
            t = next(tail)
            tail_points = np.array(t)
        bg = map_img.copy()
        x = (p[0, 0])
        y = (p[0, 1])
        cv2.polylines(bg, [tail_points], False,
                      settings.tail_color, settings.tail_size)
        cv2.circle(bg, (x, y), settings.dot_size,
                   settings.dot_color, thickness=-1)
        video.write(bg)
    video.release()
    print(f"{output_name} DONE", flush=True)
