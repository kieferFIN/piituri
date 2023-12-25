from dataclasses import asdict, dataclass
from piituri.settings import Settings
from cv2.typing import Point2f
import tomli_w
import tomllib


@dataclass(frozen=True)
class Params:
    intervalls: list[int]
    rotation_params: list[tuple[Point2f, float, float]]


def create_params_file_name(s: Settings) -> str:
    return f"{s.output_name}_{s.map_file_name}_{s.route_file_name}.toml"


def write_params(parmas: Params, file_name: str):
    with open(file_name, "wb") as f:
        tomli_w.dump(asdict(parmas), f)


def read_params(file_name: str):
    with open(file_name, "rb") as f:
        params = tomllib.load(f)
    intervalls_size = len(params['intervalls'])
    rot_params_size = len(params['rotation_params'])
    if (intervalls_size - rot_params_size > 1):
        raise ValueError("Not enough rotation params")
    elif (intervalls_size - rot_params_size < 1):
        raise ValueError("Too many rotation params")
    return Params(**params)
