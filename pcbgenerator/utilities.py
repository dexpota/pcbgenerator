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
