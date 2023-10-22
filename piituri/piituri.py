from itertools import pairwise, repeat, count
from multiprocessing import Pool
import cv2

from .tail_maker import make_tail
from .image_maker import make_image
from .video_maker import make_video
from .settings import Settings
from .route_parser import parse_route
from .transformation import create_transformation
from .route_points_creator import create_route_points


def task(route, map_img, settings: Settings, i, limits):
    start = limits[0]
    end = limits[1]
    rot = create_transformation(
        route[start:end+1], settings.width, settings.height)
    route_points = create_route_points(
        start, end, route, rot, settings.relative_fps)
    transformed_map = cv2.warpAffine(
        map_img, rot, (settings.width, settings.height))
    if settings.make_images:
        make_image(route_points, transformed_map, settings, i)
    else:
        make_video(route_points, make_tail(start, end+1, route,
                   settings.tail_length, rot), transformed_map, settings, i)


def _get_splits(s: Settings, splits):
    if len(s.splits) > 0:
        return s.splits, [(splits[i], splits[i+1]) for i in s.splits]
    else:
        return count(0), pairwise(splits)


def piituri(settings: Settings):
    route, splits = parse_route(settings.route_file_name)
    print(f"splits:{splits}")
    map_img = cv2.imread(settings.map_file_name)

    with Pool() as pool:
        # _task = partial(task, route, map_img, settings)
        data_iter = zip(repeat(route), repeat(map_img),
                        repeat(settings), *_get_splits(settings, splits))
        pool.starmap(task, data_iter)
        pool.close()
        pool.join()
