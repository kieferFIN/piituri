import argparse
import piituri_lib


def main():
    parser = argparse.ArgumentParser(prog='piituri')
    parser.add_argument("map_file_name", type=str)
    parser.add_argument("route_file_name", type=str)
    parser.add_argument("output_name", type=str)
    parser.add_argument("settings_file", nargs="?", default="settings.toml")
    parser.add_argument("-s", "--splits", nargs='+', type=int, default=[])
    parser.add_argument("-i", "--image", action='store_true')
    parser.add_argument("-f", "--force", action='store_true')
    args = parser.parse_args()
    settings = piituri_lib.parse_args(args)
    piituri_lib.piituri(settings)


if __name__ == "__main__":
    main()
