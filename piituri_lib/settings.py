from dataclasses import dataclass, field, replace
import tomllib


@dataclass(frozen=True)
class Settings:
    map_file_name: str
    route_file_name: str
    output_name: str
    splits: list[int]
    make_images: bool
    force_new_parameters: bool
    fps: int = 60
    speed_up: float = 1.0
    width: int = 320
    height: int = 720
    dot_color: tuple[int, int, int] = field(
        default_factory=lambda: (255, 0, 0))
    dot_size: int = 10
    tail_color: tuple[int, int, int] = field(
        default_factory=lambda: (0, 0, 255))
    tail_size: int = 4
    tail_length: int = 60
    fourcc: str = 'mp4v'

    @property
    def relative_fps(self) -> int:
        return round(self.fps / self.speed_up)


def _rgb_to_bgr(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    return (rgb[2], rgb[1], rgb[0])


def parse_args(args) -> Settings:
    file_params = {}
    if args.settings_file is not None:
        file_params = _read_settings(args.settings_file)
    if args.image:
        file_params['fps'] = 1
        file_params['speed_up'] = 1.0
    settings = Settings(args.map_file_name,
                        args.route_file_name,
                        args.output_name,
                        args.splits,
                        args.image,
                        args.force,
                        **file_params)

    settings = replace(settings,
                       dot_color=_rgb_to_bgr(settings.dot_color),
                       tail_color=_rgb_to_bgr(settings.tail_color))

    return settings


def _read_settings(file_name):
    print(f"Settings file: {file_name}")
    with open(file_name, 'rb') as f:
        return tomllib.load(f)
