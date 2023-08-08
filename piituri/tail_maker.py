import cv2
import numpy as np


def make_tail(start, end, points, length, rot):
    s = max(start - length, 0)
    p = cv2.transform(np.array([points[s:end]]), rot)[0].astype('int32')
    i = len(p) - (end - start)+1
    while i < len(p):
        j = max(i - length, 0)
        yield p[j:i]
        i += 1
