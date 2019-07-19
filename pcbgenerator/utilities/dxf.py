import dxfgrabber


class ActionApplication:

    def __init__(self, action, rules):
        """

        :param action:
        :type action:
        :param rules:
        :type rules: list[object]
        """
        self.action = action
        self.rules = rules


def traverse_dxf(filepath, applications=None):
    """

    :param filepath:
    :param applications:
    :type applications: list[ActionApplication]
    :return:
    """

    if applications is None:
        applications = []

    dxf = dxfgrabber.readfile(filepath)

    for e in dxf.entities.get_entities():

        for application in applications:
            if all(map(lambda x: x(e), application.rules)):
                application.action(e)

        if e.dxftype == "LINE":
            print("LINE")
        elif e.dxftype == "CIRCLE":
            print("CIRCLE")
        elif e.dxftype == "ARC":
            print("ARC")
        elif e.dxftype == "LWPOLYLINE":
            print("LWPOLYLINE")
            print(e)
