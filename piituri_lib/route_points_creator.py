import math
import cv2
import numpy as np


def create_route_points(start, end, points, rot, fps):
    def get_point(frame_index: int):
        t = frame_index/fps
        i = math.floor(t)
        td = t-i
        p1 = points[i]
        p2 = points[math.ceil(t)]
        return p1*(1-td)+p2*td
    return cv2.transform(np.array([[get_point(i)] for i in range(start*fps, end*fps)]), rot).astype('int32')
