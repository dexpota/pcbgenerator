import pcbnew
from argparse import ArgumentParser


def main():
    print("Calling pcbgenerator.")

    parser = ArgumentParser()
    parser.add_argument("--name", type=str, required=False)

    parser.parse_args()
    # board = LoadBoard("name")
