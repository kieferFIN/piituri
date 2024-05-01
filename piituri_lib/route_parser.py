import xml.etree.ElementTree as ET
import numpy as np
from functools import reduce


def parse_route(file_name: str):
    root = ET.parse(file_name).getroot()
    seq = root[0]

    points = np.array([(p.attrib['imageX'], p.attrib['imageY'])
                       for p in seq], dtype=np.dtype(('float32', 2)))  # type: ignore

    def f(splits: list, p):
        if int(p.attrib['lapNumber']) != len(splits):
            splits.append(round(float(p.attrib["elapsedTimeFromStart"])))
        return splits

    intervalls: list[int] = reduce(f, seq, [])
    intervalls.append(len(seq)-1)

    return points, intervalls
