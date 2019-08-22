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

    # Everything that must be cut off the PCB
    lwpolyline_rule = IsInstance(LWPolyline)
    inlayer_rule = InLayer("outline")
    draw_action = DrawInLayer(board, layertable["Edge.Cuts"])
    application = ActionApplication(draw_action, [lwpolyline_rule, inlayer_rule])

    c_footprint = pcbnew.FootprintLoad("/usr/share/kicad/modules/Capacitor_SMD.pretty", "C_1206_3216Metric_Pad1.42x1.75mm_HandSolder")
    c_inlayer = InLayer("capacitors")
    c_action = ActionApplication(ComponentPlacing(board, c_footprint), [c_inlayer])

    # Mounting holes for securing the PCB
    footprint = pcbnew.FootprintLoad("/usr/share/kicad/modules/MountingHole.pretty", "MountingHole_2mm")
    inlayer_rule_mounting_holes = InLayer("mounting_holes")
    placing = ComponentPlacing(board, footprint)
    application2 = ActionApplication(placing, [inlayer_rule_mounting_holes])

    # Bridge between two PCBs
    b_footprint = pcbnew.FootprintLoad("/home/fabrizio/developing/github/kicad-libraries/connectors.pretty", "BridgeSolderPad_3xinline")
    b_action = ActionApplication(ComponentPlacing(board, b_footprint), [InLayer("bridge")])

    # PinHeader Board-Board connectors
    h_footprint = pcbnew.FootprintLoad("/usr/share/kicad/modules/Connector_PinHeader_2.54mm.pretty", "PinHeader_1x03_P2.54mm_Vertical")
    h_action = ActionApplication(ComponentPlacing(board, h_footprint), [InLayer("connectors")])

    # LED
    led_footprint = pcbnew.FootprintLoad("/home/fabrizio/developing/github/kicad-libraries/leds.pretty", "SK6412_BIG_PAD")
    inlayer_rule_led = InLayer("leds")
    placing2 = ComponentPlacing(board, led_footprint)
    application3 = ActionApplication(placing2, [inlayer_rule_led])

    traverse_dxf(dxf_filename, [application, application2, application3, c_action, b_action, h_action])
    board.Save(f"output/{pcb_filename}.kicad_pcb")
