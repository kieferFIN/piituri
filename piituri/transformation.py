import cv2
import numpy as np
from cv2.typing import Point2f, MatLike

from piituri.params import RotationParams


def calculate_rot_params(points, width: int, height: int) -> RotationParams:
    is_landscape: bool = width > height
    center_point, (dim_x, dim_y), angle = cv2.minAreaRect(
        points)
    start_point = points[0]
    end_point = points[-1]
    if dim_x > dim_y:
        angle -= 90
        dim_x, dim_y = dim_y, dim_x
    tmp_rot = cv2.getRotationMatrix2D(center_point, angle, 1)
    tmp_points = cv2.transform(
        np.array([[start_point, end_point]]), tmp_rot)[0]
    if tmp_points[0, 1] < tmp_points[1, 1]:
        angle += 180
    if is_landscape:
        angle -= 90
        dim_x, dim_y = dim_y, dim_x
    dim_x += 100
    dim_y += 200
    scale = min(width/dim_x, height/dim_y)
    return RotationParams(center_point, angle, scale)


def create_transformation(params: RotationParams, width: int, height: int) -> MatLike:
    rot = cv2.getRotationMatrix2D(
        params.center_point, params.angle, params.scale)
    rot[0, 2] -= (params.center_point[0] - width*0.5)
    rot[1, 2] -= (params.center_point[1] - height*0.5)

    return rot
