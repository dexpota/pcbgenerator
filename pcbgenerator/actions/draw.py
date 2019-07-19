from dxfgrabber.dxfentities import LWPolyline, DXFEntity
from pcbnew import BOARD
import pcbnew
import math
from ..utilities.kicad import pcbpoint


class DrawInLayer:
    """
    This action draw a DXFEntity inside a specific layer.
    """

    def __init__(self, board, layer):
        """

        :param board:
        :type board: BOARD
        :param layer:
        :type layer: str
        """
        self.board = board
        self.layer = layer

    def __call__(self, entity):
        """

        :param entity:
        :type entity: DXFEntity
        :return:
        """
        if type(entity) is LWPolyline:
            self._draw(entity)
        else:
            raise NotImplemented(f"{self.__class__.__name__}: this action currently support only LWPolyline")

    def create_basic_segment(self):
        seg = pcbnew.DRAWSEGMENT(self.board)
        seg.SetLayer(self.layer)
        seg.SetShape(pcbnew.S_POLYGON)
        self.board.Add(seg)
        return seg

    def _draw(self, element):
        seg = self.create_basic_segment()
        points = element.points
        seg.SetShape(pcbnew.S_POLYGON)

        sps = seg.GetPolyShape()
        i = sps.NewOutline()
        outline = sps.Outline(i)

        for pnt in points:
            ppt = pcbpoint(pnt[0], pnt[1]).wxpoint()
            outline.Append(ppt[0], ppt[1])


def bulge_to_arc(p0, p1, bulge):
    my1 = (p0[1] + p1[1]) / 2.0
    mx1 = (p0[0] + p1[0]) / 2.0
    angle = math.atan(bulge) * 4.0
    angleDeg = math.degrees(angle)

    dist = math.sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)
    sagitta = dist / 2.0 * bulge
    radius = abs(((dist / 2.0) ** 2 + sagitta ** 2) / (2 * sagitta))

    alen = abs(radius * angle)
    theta = 4.0 * math.atan(abs(bulge))
    gamma = (math.pi - theta) / 2.0

    if bulge > 0:
        phi = math.atan2(p1[1] - p0[1], p1[0] - p0[0]) + gamma
    else:
        phi = math.atan2(p1[1] - p0[1], p1[0] - p0[0]) - gamma

    cx = p0[0] + radius * math.cos(phi)
    cy = p0[1] + radius * math.sin(phi)
    startAngle = math.acos((p0[0] - cx) / radius)
    endAngle = startAngle + angle

    return (cx, cy), radius, math.degrees(startAngle), angleDeg