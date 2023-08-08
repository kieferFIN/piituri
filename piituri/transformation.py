import cv2


def create_transformation(points, width: int, height: int):
    is_landscape: bool = width > height

    center_point, (dim_x, dim_y), angle = cv2.minAreaRect(
        points)
    start_point = points[0]
    end_point = points[-1]
    if start_point[0] > end_point[0]:
        angle -= 90
        dim_x, dim_y = dim_y, dim_x
        if start_point[1] < end_point[1]:
            angle -= 90
            dim_x, dim_y = dim_y, dim_x
    elif start_point[1] < end_point[1]:
        angle += 90
        dim_x, dim_y = dim_y, dim_x
    if is_landscape:
        angle -= 90
        dim_x, dim_y = dim_y, dim_x
    dim_x += 100
    dim_y += 200
    scale = min(width/dim_x, height/dim_y)

    rot = cv2.getRotationMatrix2D(center_point, angle, scale)
    rot[0, 2] -= (center_point[0] - width*0.5)
    rot[1, 2] -= (center_point[1] - height*0.5)

    return rot
