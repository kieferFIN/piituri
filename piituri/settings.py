from dataclasses import dataclass, field


@dataclass
class Settings:
    map_file_name: str
    route_file_name: str
    output_name: str
    splits: list[int]
    make_images: bool
    fps: int = 60
    width: int = 320
    height: int = 720
    dot_color: list[int] = field(default_factory=lambda: [255, 0, 0])
    dot_size: int = 10
    tail_color: list[int] = field(default_factory=lambda: [0, 0, 255])
    tail_size: int = 4
    tail_length: int = 60


def _rgb_to_bgr(rgb) -> tuple[int, int, int]:
    return (rgb[2], rgb[1], rgb[0])


def parse_args(args) -> Settings:
    settings = Settings(args.map_file_name,
                        args.route_file_name, args.output_name, args.splits, args.image)
    if args.settings_file is not None:
        _read_settings(args.settings_file)
    if settings.make_images:
        settings.fps = 1

    settings.dot_color = _rgb_to_bgr(settings.dot_color)
    settings.tail_color = _rgb_to_bgr(settings.tail_color)

    return settings


def _read_settings(file_name):
    print(f"Settings file: {file_name}")
    print("Read settings from file is not implemented, using default values")
