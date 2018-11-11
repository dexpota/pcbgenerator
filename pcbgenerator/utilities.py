import numpy as np


def inset_triangle(triangle, barycentric_coordinates):
    edge1 = triangle[1] - triangle[0]
    edge2 = triangle[2] - triangle[0]

    normalized_edge1 = edge1 / np.linalg.norm(edge1)
    normalized_edge2 = edge2 / np.linalg.norm(edge2)

    smaller_triangle = [
        triangle[0] + barycentric_coordinates[0][0]*normalized_edge1 + barycentric_coordinates[0][1]*normalized_edge2,
        triangle[0] + barycentric_coordinates[1][0]*normalized_edge1 + barycentric_coordinates[1][1]*normalized_edge2,
        triangle[0] + barycentric_coordinates[2][0]*normalized_edge1 + barycentric_coordinates[2][1]*normalized_edge2]

    return smaller_triangle


def place_holes(triangle, barycentric_coordinates):
    edge1 = triangle[1] - triangle[0]
    edge2 = triangle[2] - triangle[0]

    normalized_edge1 = edge1 / np.linalg.norm(edge1)
    normalized_edge2 = edge2 / np.linalg.norm(edge2)

    holes = [
        triangle[0] + barycentric_coordinates[0][0]*normalized_edge1 + barycentric_coordinates[0][1]*normalized_edge2,
        triangle[0] + barycentric_coordinates[1][0]*normalized_edge1 + barycentric_coordinates[1][1]*normalized_edge2,
        triangle[0] + barycentric_coordinates[2][0]*normalized_edge1 + barycentric_coordinates[2][1]*normalized_edge2]

    return holes


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


def compute_rectangle(origin2d, direction2d, d1, d2):
    tangent = np.array([direction2d[1], -direction2d[0]])
    direction2d /= np.linalg.norm(direction2d)
    tangent /= np.linalg.norm(tangent)

    origin2d = np.array(origin2d)

    first_point = origin2d - direction2d/2.0 * d1 - tangent/2.0 * d2
    second_point = first_point + tangent * d2
    third_point = second_point + direction2d * d1
    fourth_point = third_point - tangent * d2
    return [first_point, second_point, third_point, fourth_point]


def uniform_sampling_triangle(triangle):
    edge1 = triangle[1] - triangle[0]
    edge2 = triangle[2] - triangle[0]

    normalized_edge1 = edge1 / np.linalg.norm(edge1)
    normalized_edge2 = edge2 / np.linalg.norm(edge2)

    normal = np.cross(normalized_edge1, normalized_edge2)

    frame_2d = plane_2d_frame(triangle[0], normal, edge1)

    triangle2d = [project_point_to_2d_frame(frame_2d, triangle[0]),
                  project_point_to_2d_frame(frame_2d, triangle[1]),
                  project_point_to_2d_frame(frame_2d, triangle[2])]

    up = np.array((0, 0, 1))

    for u in np.linspace(0, 1, 10):
        for v in np.linspace(0, 1, 10):
            if u + v <= 1.0:
                point = triangle[0] + u*edge1 + v*edge2
                pi_normal = np.cross(point, up)

                direction = np.cross(normal, pi_normal)
                direction /= np.linalg.norm(direction)
                direction *= 10

                point2d = project_point_to_2d_frame(frame_2d, point)

                origin2d, direction2d = project_vector_to_2d_frame(frame_2d, point, direction)

                if not np.isnan(direction2d[0]) and not np.isnan(direction2d[1]):
                    compute_rectangle(origin2d, direction2d, 5, 5)

