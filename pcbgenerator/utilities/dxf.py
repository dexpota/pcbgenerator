import dxfgrabber


def traverse_dxf(filepath, actions=None):
    if actions is None:
        actions = []

    dxf = dxfgrabber.readfile(filepath)

    for e in dxf.entities.get_entities():
        if e.dxftype == "LINE":
            print("LINE")
        elif e.dxftype == "CIRCLE":
            print("CIRCLE")
        elif e.dxftype == "ARC":
            print("ARC")
        elif e.dxftype == "LWPOLYLINE":
            actions[0](e)
            print("LWPOLYLINE")
            print(e)
