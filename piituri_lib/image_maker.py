import cv2
from os import path
from piituri_lib.settings import Settings
from pathlib import Path


def make_image(route_points, map_img, settings: Settings, i):
    output_name = Path(f"{settings.output_name}/{i}.png").absolute()
    print(f"writing image {output_name.name}", flush=True)
    cv2.polylines(map_img, [route_points], False,
                  settings.tail_color, settings.tail_size)
    cv2.imwrite(str(output_name), map_img)
    print(f"{output_name.name} DONE", flush=True)
