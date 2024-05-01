from argparse import Namespace
import piituri_lib
from multiprocessing import freeze_support


def main():
    args = Namespace()
    args.map_file_name = input("map file? ")
    args.route_file_name = input("route file? ")
    args.output_name = input("output folder? ")
    while (True):
        answer = input("Videos or Images? ")
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


if __name__ == "__main__":
    freeze_support()
    main()
