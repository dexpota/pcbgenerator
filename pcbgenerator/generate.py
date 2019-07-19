import pcbnew
from pcbnew import BOARD
from argparse import ArgumentParser
from .utilities.dxf import traverse_dxf, ActionApplication
from .actions.placing import ComponentPlacing
from .actions.draw import DrawInLayer
from .rules.IsInstance import IsInstance
from dxfgrabber.dxfentities import LWPolyline


def main():
    parser = ArgumentParser(description="pcbgenerator is a tool to create pcb designs starting from dxf files.")
    parser.add_argument("dxf", help="Path to the dxf file.")
    parser.add_argument("--output", "-o", required=True, help="Filename of output file.")
    ns = parser.parse_args()

    dxf_filename = ns.dxf
    pcb_filename = ns.output

    board = BOARD()

    layertable = {}
    numlayers = pcbnew.PCB_LAYER_ID_COUNT
    for i in range(numlayers):
        layertable[board.GetLayerName(i)] = i

    action = ComponentPlacing(board)

    rule = IsInstance(LWPolyline)
    draw_action = DrawInLayer(board, layertable["Edge.Cuts"])

    application = ActionApplication(draw_action, [rule])

    traverse_dxf(dxf_filename, [application])
    board.Save(f"{pcb_filename}.kicad_pcb")
