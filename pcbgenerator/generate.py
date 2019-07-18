import pcbnew
from pcbnew import BOARD
from argparse import ArgumentParser
from .utilities.dxf import traverse_dxf
from .actions.placing import ComponentPlacing


def main():
    parser = ArgumentParser(description="pcbgenerator is a tool to create pcb designs starting from dxf files.")
    parser.add_argument("dxf", help="Path to the dxf file.")
    ns = parser.parse_args()

    dxf_filename = ns.dxf

    board = BOARD()
    action = ComponentPlacing(board)
    traverse_dxf(dxf_filename)
    board.Save("filename")
