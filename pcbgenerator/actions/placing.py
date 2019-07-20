from pcbnew import BOARD, MODULE
import pcbnew
from ..utilities.kicad import pcbpoint
from dxfgrabber.dxfentities import Circle, DXFEntity


class ComponentPlacing:
    """
    This action perform the placing of the component.
    """

    def __init__(self, board, footprint):
        """

        :param board:
        :type board: BOARD
        :type footprint: MODULE
        """
        self.board = board
        # TODO switch to a component factory
        self.footprint = footprint

    def __call__(self, entity):
        """

        :param entity:
        :type entity: Circle
        :return:
        """

        if entity.dxftype == "CIRCLE":
            # Create a new module from the footprint
            fp = pcbnew.MODULE(self.footprint)
            fp.SetPosition(pcbpoint(entity.center).wxpoint())
            self.board.Add(fp)
