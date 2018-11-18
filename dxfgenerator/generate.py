import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ezdxf
from .octahedron import OctahedronV2
from .utilities import inset_triangle, place_holes, draw_polyline, uniform_sampling_triangle


def generate_dxf(filename, triangle2d, rectangles, centers):
    drawing = ezdxf.new(dxfversion='AC1024')
    modelspace = drawing.modelspace()

    draw_polyline(modelspace, triangle2d)

    for hole in centers:
        modelspace.add_circle(hole, 1)

    for rectangle in rectangles:
        draw_polyline(modelspace, rectangle)

    drawing.saveas(filename)


def smaller_triangle_aab(triangles):
    all_holes = []
    smaller_triangles = []
    for triangle in triangles:
        smaller_triangle = inset_triangle(triangle, [[7.28, 10.01], [7.28, 138.07], [100.34, 10.01]])
        smaller_triangles.append(smaller_triangle)

        holes = place_holes(triangle, [[12.3, 15.9], [12.3, 125.28], [88.85, 17.92]])
        all_holes.append(holes)
    return all_holes, smaller_triangles


def smaller_triangle_bcc(triangles):
    all_holes = []
    smaller_triangles = []
    for triangle in triangles:
        smaller_triangle = inset_triangle(triangle, [[7.91, 8.39], [142.29, 8.39], [7.91, 151.1]])
        smaller_triangles.append(smaller_triangle)

        holes = place_holes(triangle, [[13.66, 13.66], [131.57, 13.66], [13.42, 139.4]])
        all_holes.append(holes)

    return all_holes, smaller_triangles


def main():
    # 1. Gather data from source
    triangles_aab = OctahedronV2.triangles_aab * 1000  # from meters to millimeters
    triangles_bcc = OctahedronV2.triangles_bcc * 1000  # from meters to millimeters

    holes_aab, smaller_aab = smaller_triangle_aab(triangles_aab)
    holes_bcc, smaller_bcc = smaller_triangle_bcc(triangles_bcc)

    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=45, azim=45)

    fig2d = plt.figure(2)
    ax2d = fig2d.add_subplot(111)

    filenames = ["aab1.dxf", "aab2.dxf", "aab3.dxf"]
    colors = ["beige", "black", "blue"]
    for filename, holes, triangle, color in zip(filenames, holes_aab, smaller_aab, colors):
        triangle2d, rectangles, centers = uniform_sampling_triangle(triangle, holes)
        generate_dxf(filename, triangle2d, rectangles, centers)

    filenames = ["bcc1.dxf", "bcc2.dxf", "bcc3.dxf", "bcc4.dxf", "bcc5.dxf", "bcc6.dxf"]
    colors = ["brown", "coral", "cyan", "darkgreen", "gold", "green"]
    for filename, holes, triangle, color in zip(filenames, holes_bcc, smaller_bcc, colors):
        triangle2d, rectangles, centers = uniform_sampling_triangle(triangle, holes)
        generate_dxf(filename, triangle2d, rectangles, centers)

    plt.interactive(True)
    plt.show(block=True)


if __name__ == "__main__":
    main()
