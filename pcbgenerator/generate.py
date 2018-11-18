import pcbnew
from argparse import ArgumentParser
from .utilities.dxf import traverse_dxf


def main():
    print("Calling pcbgenerator.")

    parser = ArgumentParser()
    parser.add_argument("--dxf", type=str, required=True)
    ns = parser.parse_args()

    dxf_filename = ns.dxf

    traverse_dxf(dxf_filename)
    # board = LoadBoard("name")
