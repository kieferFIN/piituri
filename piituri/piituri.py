from itertools import pairwise, repeat, count
from multiprocessing import Pool
import cv2
from os.path import isfile
from .params import Params, RotationParams, create_params_file_name, read_params, write_params
from .tail_maker import make_tail
from .image_maker import make_image
from .video_maker import make_video
from .settings import Settings
from .route_parser import parse_route
from .transformation import calculate_rot_params, create_transformation
from .route_points_creator import create_route_points


def task(route, map_img, settings: Settings, i, limits, rot_params: RotationParams):
    start = limits[0]
    end = limits[1]
    if rot_params is None:
        rot_params = calculate_rot_params(
            route[start:end+1], settings.width, settings.height)
    rot = create_transformation(
        rot_params, settings.width, settings.height)
    route_points = create_route_points(
        start, end, route, rot, settings.relative_fps)
    transformed_map = cv2.warpAffine(
        map_img, rot, (settings.width, settings.height))
    if settings.make_images:
        make_image(route_points, transformed_map, settings, i)
    else:
        make_video(route_points, make_tail(start, end+1, route,
                   settings.tail_length, rot), transformed_map, settings, i)
    return rot_params


def _get_splits(s: Settings, params: Params):

    if params.rotation_params is None:
        if len(s.splits) > 0:
            return s.splits, [(params.intervalls[i], params.intervalls[i+1]) for i in s.splits], repeat(None)
        else:
            return count(0), pairwise(params.intervalls), repeat(None)
    else:
        if len(s.splits) > 0:
            return s.splits, [(params.intervalls[i], params.intervalls[i+1]) for i in s.splits], [params.rotation_params[i] for i in s.splits]
        else:
            return count(0), pairwise(params.intervalls), params.rotation_params


def piituri(settings: Settings):
    params_file_name = create_params_file_name(settings)
    params = Params(None, None) if settings.force_new_parameters or not isfile(
        params_file_name) else read_params(params_file_name)

    route, intervalls = parse_route(settings.route_file_name)
    if params.intervalls is None:
        params = Params(intervalls, params.rotation_params)
    map_img = cv2.imread(settings.map_file_name)

    with Pool() as pool:
        data_iter = zip(repeat(route), repeat(map_img),
                        repeat(settings), *_get_splits(settings, params))
        rot_params = pool.starmap(task, data_iter)
        pool.close()
        pool.join()

        if params.rotation_params is None:
            params = Params(params.intervalls, rot_params)

        write_params(params, params_file_name)
