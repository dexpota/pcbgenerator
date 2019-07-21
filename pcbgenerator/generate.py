import pcbnew
from pcbnew import BOARD
from argparse import ArgumentParser
from .utilities.dxf import traverse_dxf, ActionApplication
from .actions.placing import ComponentPlacing
from .actions.draw import DrawInLayer
from .rules.IsInstance import IsInstance
from .rules.InLayer import InLayer
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

    lwpolyline_rule = IsInstance(LWPolyline)
    inlayer_rule = InLayer("outline")

    draw_action = DrawInLayer(board, layertable["Edge.Cuts"])
    application = ActionApplication(draw_action, [lwpolyline_rule, inlayer_rule])

    footprint = pcbnew.FootprintLoad("/usr/share/kicad/modules/MountingHole.pretty", "MountingHole_3.2mm_M3")
    inlayer_rule_mounting_holes = InLayer("mounting_holes")
    placing = ComponentPlacing(board, footprint)
    application2 = ActionApplication(placing, [inlayer_rule_mounting_holes])

    led_footprint = pcbnew.FootprintLoad("/home/fabrizio/.config/kicad/footprints/kicad-libraries/leds.pretty", "SK6412_BIG_PAD")
    inlayer_rule_led = InLayer("footprint")
    placing2 = ComponentPlacing(board, led_footprint)
    application3 = ActionApplication(placing2, [inlayer_rule_led])

    traverse_dxf(dxf_filename, [application, application2, application3])
    board.Save(f"output/{pcb_filename}.kicad_pcb")
