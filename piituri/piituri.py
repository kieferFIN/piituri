from functools import partial
from itertools import pairwise
from multiprocessing import Pool
import cv2

from piituri.tail_maker import make_tail

from .image_maker import make_image
from .video_maker import make_video
from .settings import Settings
from .route_parser import parse_route
from .transformation import create_transformation
from .route_points_creator import create_route_points


def task(route, map_img, settings: Settings, i, limits):
    start = limits[0]
    end = limits[1]
    fps = settings.fps
    rot = create_transformation(
        route[start:end+1], settings.width, settings.height)
    route_points = create_route_points(start, end, route, rot, fps)
    transformed_map = cv2.warpAffine(
        map_img, rot, (settings.width, settings.height))
    if settings.make_images:
        make_image(route_points, transformed_map, settings, i)
    else:
        make_video(route_points, make_tail(start, end+1, route,
                   settings.tail_length, rot), transformed_map, settings, i)


def piituri(settings: Settings):
    route, splits = parse_route(settings.route_file_name)
    print(f"splits:{splits}")
    if len(settings.splits) > 0:
        split_iter = []
        for i in settings.splits:
            split_iter.append((i, (splits[i], splits[i+1])))
    else:
        split_iter = enumerate(pairwise(splits))
    map_img = cv2.imread(settings.map_file_name)

    with Pool() as pool:
        _task = partial(task, route, map_img, settings)
        pool.starmap(_task, split_iter)
        pool.close()
        pool.join()
