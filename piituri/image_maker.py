import cv2

from piituri.settings import Settings


def make_image(route_points, map_img, settings: Settings, i):
    output_name = f"{settings.output_name}_{i}.png"
    print(f"writing image {output_name}", flush=True)
    cv2.polylines(map_img, [route_points], False,
                  settings.tail_color, settings.tail_size)
    cv2.imwrite(output_name, map_img)
    print(f"{output_name} DONE", flush=True)
