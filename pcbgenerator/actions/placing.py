from pcbnew import BOARD, MODULE
import pcbnew
from ..utilities.kicad import pcbpoint
from dxfgrabber.dxfentities import Circle, DXFEntity, LWPolyline
import math
import numpy


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
        :type entity: DXFEntity
        :return:
        """
        if isinstance(entity, Circle) and entity.dxftype == "CIRCLE":
            # Create a new module from the footprint
            fp = pcbnew.MODULE(self.footprint)
            fp.SetPosition(pcbpoint(entity.center).wxpoint())
            self.board.Add(fp)
        elif isinstance(entity, LWPolyline) and entity.dxftype == "LWPOLYLINE":
            angle = -longest_angle_for_polygon(entity.points)
            fp = pcbnew.MODULE(self.footprint)
            fp.SetPosition(pcbpoint(centeroidnp(entity.points)).wxpoint())
            fp.SetOrientation(angle * 10)
            self.board.Add(fp)


def centeroidnp(arr):
    arr = numpy.array(arr)
    length = arr.shape[0]
    sum_x = numpy.sum(arr[:, 0])
    sum_y = numpy.sum(arr[:, 1])
    return sum_x/length, sum_y/length


def distpts(a,b):
    return numpy.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)


def anglepts(a,b):
    return math.degrees(math.atan2(b[1]-a[1], b[0]-a[0]))


def longest_angle_for_polygon(poly):
    prevpt = poly[-1]
    length = None
    retval = None
    for pt in poly:
        d = distpts(prevpt, pt)
        if (length and (length>d)):
            prevpt = pt
            continue
        length = d
        retval = anglepts(prevpt, pt)
        prevpt = pt
    return retval