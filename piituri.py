from argparse import Namespace
import piituri_lib
from multiprocessing import freeze_support
from pathlib import Path


def _find_file(pattern: str) -> Path | None:
    files = [p for p in Path('.').glob(pattern)]
    return files[0] if len(files) == 1 else None


def _ask(question: str, default: str | None = None) -> str:
    opt_default: Path | None = None
    if default is not None:
        opt_default = _find_file(default)
    real_question = f"{question} ? " if opt_default is None else f"{question} (defualt: '{opt_default}')?"
    answer = input(real_question).strip()
    if opt_default is not None and len(answer) < 1:
        answer = str(opt_default)
    return answer


def main():
    try:
        args = Namespace()

        args.map_file_name = _ask("map file", '*.png')
        args.route_file_name = _ask("route file", '*.xml')
        args.output_name = _ask("output folder")
        while (True):
            answer = _ask("Videos or Images")
            answer = answer.lower()
            if (answer[0] == 'v'):
                args.image = False
                break
            if (answer[0] == 'i'):
                args.image = True
                break
        args.settings_file = "settings.toml"
        args.splits = []
        args.force = False

        settings = piituri_lib.parse_args(args)
        piituri_lib.piituri(settings)

        input('Done.')
    except Exception as error:
        print(error)
        input("press any key to quit")


if __name__ == "__main__":
    freeze_support()
    main()
