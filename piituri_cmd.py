import argparse
import piituri


def main():
    parser = argparse.ArgumentParser(prog='piituri')
    parser.add_argument("map_file_name", type=str)
    parser.add_argument("route_file_name", type=str)
    parser.add_argument("output_name", type=str)
    parser.add_argument("settings_file", nargs="?", default="settings.toml")
    parser.add_argument("-s", "--splits", nargs='+', type=int, default=[])
    parser.add_argument("-i", "--image", action='store_true')
    args = parser.parse_args()
    settings = piituri.parse_args(args)
    piituri.piituri(settings)


if __name__ == "__main__":
    main()
