import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ezdxf


def plane_2d_frame(point, normal, axis):
    o = point
    x = axis / np.linalg.norm(axis)
    y = np.cross(normal, x)
    y /= np.linalg.norm(y)
    return o, x, y


def project_point_to_2d_frame(frame, point):
    t1 = np.dot(frame[1], point - frame[0])
    t2 = np.dot(frame[2], point - frame[0])
    return t1, t2


def project_vector_to_2d_frame(frame, point, vector):
    t1, t2 = project_point_to_2d_frame(frame, point)
    t3, t4 = project_point_to_2d_frame(frame, point + vector)
    return (t1, t2), (t3 - t1, t4 - t2)


def draw_polyline(modelspace, line):
    modelspace.add_polyline2d(line, {"closed": True})


def compute_rectangle(origin2d, direction2d):
    tangent = np.array([direction2d[1], -direction2d[0]])
    direction2d /= np.linalg.norm(direction2d)
    tangent /= np.linalg.norm(tangent)

    origin2d = np.array(origin2d)

    first_point = origin2d - direction2d/2.0 * 5 - tangent/2.0 * 2
    second_point = first_point + tangent * 2
    third_point = second_point + direction2d * 5
    fourth_point = third_point - tangent * 2
    return list(first_point), list(second_point), list(third_point), list(fourth_point)


def uniform_sampling_triangle(filename, triangle, holes, ax, ax2d, color="blue"):
    drawing = ezdxf.new(dxfversion='AC1024')
    modelspace = drawing.modelspace()

    edge1 = triangle[1] - triangle[0]
    edge2 = triangle[2] - triangle[0]

    normalized_edge1 = edge1 / np.linalg.norm(edge1)
    normalized_edge2 = edge2 / np.linalg.norm(edge2)

    normal = np.cross(normalized_edge1, normalized_edge2)

    frame_2d = plane_2d_frame(triangle[0], normal, edge1)

    triangle2d = [project_point_to_2d_frame(frame_2d, triangle[0]),
                  project_point_to_2d_frame(frame_2d, triangle[1]),
                  project_point_to_2d_frame(frame_2d, triangle[2])]

    draw_polyline(modelspace, triangle2d)

    for hole in holes:
        center = project_point_to_2d_frame(frame_2d, hole)
        modelspace.add_circle(center, 1)

    up = np.array((0, 0, 1))

    ax2d.scatter(triangle2d[0][0], triangle2d[0][1])
    ax2d.scatter(triangle2d[1][0], triangle2d[1][1])
    ax2d.scatter(triangle2d[2][0], triangle2d[2][1])
    for u in np.linspace(0, 1, 10):
        for v in np.linspace(0, 1, 10):
            if u + v <= 1.0:
                point = triangle[0] + u*edge1 + v*edge2
                pi_normal = np.cross(point, up)

                direction = np.cross(normal, pi_normal)
                direction /= np.linalg.norm(direction)
                direction *= 10
                # plt.scatter(point[0], point[1])
                ax.quiver(point[0], point[1], point[2],
                          direction[0], direction[1], direction[2])
                ax.scatter(point[0], point[1], point[2], color=color)

                point2d = project_point_to_2d_frame(frame_2d, point)
                # ax2d.scatter(point2d[0], point2d[1])

                origin2d, direction2d = project_vector_to_2d_frame(frame_2d, point, direction)
                # ax2d.quiver(origin2d[0], origin2d[1], direction2d[0], direction2d[1])

                if not np.isnan(direction2d[0]) and not np.isnan(direction2d[1]):
                    draw_polyline(modelspace, compute_rectangle(origin2d, direction2d))

    # drawing.saveas(filename)


def smaller_triangle_aab(triangles):
    all_holes = []
    smaller_triangles = []
    for triangle in triangles:
        edge1 = triangle[1] - triangle[0]
        edge2 = triangle[2] - triangle[0]
        edge3 = triangle[2] - triangle[1]
        print(np.linalg.norm(edge1))
        print(np.linalg.norm(edge2))
        print(np.linalg.norm(edge3))
        print()
        normalized_edge1 = edge1 / np.linalg.norm(edge1)
        normalized_edge2 = edge2 / np.linalg.norm(edge2)

        smaller_triangle = [triangle[0] + 7.28 * normalized_edge1 + 10.01 * normalized_edge2,
                            triangle[0] + 7.28 * normalized_edge1 + 138.07 * normalized_edge2,
                            triangle[0] + 100.34 * normalized_edge1 + 10.01 * normalized_edge2]

        smaller_triangles.append(smaller_triangle)

        holes = [triangle[0] + 12.3 * normalized_edge1 + 15.9 * normalized_edge2,
                 triangle[0] + 12.3 * normalized_edge1 + 125.28 * normalized_edge2,
                 triangle[0] + 88.85 * normalized_edge1 + 17.92 * normalized_edge2]

        all_holes.append(holes)

        smaller_edge1 = smaller_triangle[1] - smaller_triangle[0]
        smaller_edge2 = smaller_triangle[2] - smaller_triangle[0]
        smaller_edge3 = smaller_triangle[2] - smaller_triangle[1]

        print(np.linalg.norm(smaller_edge1))
        print(np.linalg.norm(smaller_edge2))
        print(np.linalg.norm(smaller_edge3))
        print()
        # uniform_sampling_triangle(triangle, normal)
    return all_holes, smaller_triangles


def smaller_triangle_bcc(triangles):
    all_holes = []
    smaller_triangles = []
    for triangle in triangles:
        edge1 = triangle[1] - triangle[0]
        edge2 = triangle[2] - triangle[0]
        print(np.linalg.norm(edge1))
        print(np.linalg.norm(edge2))
        print()
        normalized_edge1 = edge1 / np.linalg.norm(edge1)
        normalized_edge2 = edge2 / np.linalg.norm(edge2)

        normal = np.cross(normalized_edge1, normalized_edge2)

        smaller_triangle = [triangle[0] + 7.91 * normalized_edge1 + 8.39 * normalized_edge2,
                            triangle[0] + 142.29 * normalized_edge1 + 8.39 * normalized_edge2,
                            triangle[0] + 7.91 * normalized_edge1 + 151.1 * normalized_edge2]

        smaller_triangles.append(smaller_triangle)

        holes = [triangle[0] + 13.66 * normalized_edge1 + 13.66 * normalized_edge2,
                 triangle[0] + 131.57 * normalized_edge1 + 13.66 * normalized_edge2,
                 triangle[0] + 13.42 * normalized_edge1 + 139.4 * normalized_edge2]

        all_holes.append(holes)

        smaller_edge1 = smaller_triangle[1] - smaller_triangle[0]
        smaller_edge2 = smaller_triangle[2] - smaller_triangle[0]
        smaller_edge3 = smaller_triangle[2] - smaller_triangle[1]

        print(np.linalg.norm(smaller_edge1))
        print(np.linalg.norm(smaller_edge2))
        print(np.linalg.norm(smaller_edge3))
        print()
        # uniform_sampling_triangle(triangle, normal)
    return all_holes, smaller_triangles


def main():
    triangles_aab = (
        (1000 * np.array((0.223607, 0.111803, 0.000000)),
         1000 * np.array((0.250000, 0.000000, 0.000000)),
         1000 * np.array((0.223607, 0.000000, 0.111803))),  # face AAB
        (1000 * np.array((-0.000000, 0.111803, 0.223607)),
         1000 * np.array((-0.000000, 0.000000, 0.250000)),
         1000 * np.array((0.111803, 0.000000, 0.223607))),  # face AAB
        (1000 * np.array((-0.000000, 0.223607, 0.111803)),
         1000 * np.array((0.000000, 0.250000, 0.000000)),
         1000 * np.array((0.111803, 0.223607, 0.000000)))  # face AAB
    )

    triangles_bcc = (
        (1000 * np.array((-0.000000, 0.111803, 0.223607)),
         1000 * np.array((0.111803, 0.000000, 0.223607)),
         1000 * np.array((0.144338, 0.144338, 0.144338))),  # face bcc
        (1000 * np.array((0.111803, 0.000000, 0.223607)),
         1000 * np.array((0.223607, 0.000000, 0.111803)),
         1000 * np.array((0.144338, 0.144338, 0.144338))),  # face bcc
        (1000 * np.array((0.223607, 0.111803, 0.000000)),
         1000 * np.array((0.223607, 0.000000, 0.111803)),
         1000 * np.array((0.144338, 0.144338, 0.144338))),  # face bcc
        (1000 * np.array((0.111803, 0.223607, 0.000000)),
         1000 * np.array((0.223607, 0.111803, 0.000000)),
         1000 * np.array((0.144338, 0.144338, 0.144338))),  # face bcc
        (1000 * np.array((-0.000000, 0.223607, 0.111803)),
         1000 * np.array((-0.000000, 0.111803, 0.223607)),
         1000 * np.array((0.144338, 0.144338, 0.144338))),  # face bcc
        (1000 * np.array((-0.000000, 0.223607, 0.111803)),
         1000 * np.array((0.111803, 0.223607, 0.000000)),
         1000 * np.array((0.144338, 0.144338, 0.144338)))  # face bcc
    )

    holes_aab, smaller_aab = smaller_triangle_aab(triangles_aab)
    holes_bcc, smaller_bcc = smaller_triangle_bcc(triangles_bcc)

    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')

    fig2d = plt.figure(2)
    ax2d = fig2d.add_subplot(111)

    filenames = ["aab1.dxf", "aab2.dxf", "aab3.dxf"]
    colors = ["beige", "black", "blue"]
    for filename, holes, triangle, color in zip(filenames, holes_aab, smaller_aab, colors):
        uniform_sampling_triangle(filename, triangle, holes, ax, ax2d, color)

    filenames = ["bcc1.dxf", "bcc2.dxf", "bcc3.dxf", "bcc4.dxf", "bcc5.dxf", "bcc6.dxf"]
    colors = ["brown", "coral", "cyan", "darkgreen", "gold", "green"]
    for filename, holes, triangle, color in zip(filenames, holes_bcc, smaller_bcc, colors):
        uniform_sampling_triangle(filename, triangle, holes, ax, ax2d, color)

    plt.interactive(True)
    plt.show(block=True)


if __name__ == "__main__":
    main()
