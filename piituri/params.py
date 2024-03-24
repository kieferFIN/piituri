from dataclasses import asdict, dataclass
from piituri.settings import Settings
from cv2.typing import Point2f
import json
import dacite
from pathlib import Path


@dataclass(frozen=True)
class RotationParams:
    center_point: Point2f
    angle: float
    scale: float


@dataclass(frozen=True)
class Params:
    intervalls: list[int]
    rotation_params: list[RotationParams]


def create_params_file_name(s: Settings) -> Path:
    return Path(f"{s.output_name}/{s.map_file_name}_{s.route_file_name}.json")


def write_params(params: Params, file_name: Path):
    with file_name.open("w") as f:
        json.dump(asdict(params), f,  indent=2)


def read_params(file_name: Path):
    with file_name.open("r") as f:
        params = json.load(f)
    intervalls_size = len(params['intervalls'])
    rot_params_size = len(params['rotation_params'])
    if (intervalls_size - rot_params_size > 1):
        raise ValueError("Not enough rotation params")
    elif (intervalls_size - rot_params_size < 1):
        raise ValueError("Too many rotation params")
    return dacite.from_dict(data_class=Params, data=params)
