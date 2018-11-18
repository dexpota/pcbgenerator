import dxfgrabber


def traverse_dxf(filepath):
    dxf = dxfgrabber.readfile(filepath)

    for e in dxf.entities.get_entities():
        if e.dxftype == "LINE":
            print("LINE")
        elif e.dxftype == "CIRCLE":
            print("CIRCLE")
        elif e.dxftype == "ARC":
            print("ARC")
        elif e.dxftype == "LWPOLYLINE":
            print("LWPOLYLINE")