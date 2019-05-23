import numpy as np


class OctahedronV2:
    """
    This class stores the vertices of a 2V octahedron dome.

    The octahedron is built starting from the original polyhedron by using 2 subdivisions for a class-I triangulation.
    The result is composed by two types of faces, we will call them AAB and BCC (the letters represent the edges of the
    face). These faces are stored inside two different arrays inside this class, for each face in the array you have the
    three vertices composing it.
    """

    """
    List of triangular faces with edges A-A-B.
    """
    triangles_aab = np.array((
        (np.array((0.223607, 0.111803, 0.000000)),
         np.array((0.250000, 0.000000, 0.000000)),
         np.array((0.223607, 0.000000, 0.111803))),
        (np.array((-0.000000, 0.111803, 0.223607)),
         np.array((-0.000000, 0.000000, 0.250000)),
         np.array((0.111803, 0.000000, 0.223607))),
        (np.array((-0.000000, 0.223607, 0.111803)),
         np.array((0.000000, 0.250000, 0.000000)),
         np.array((0.111803, 0.223607, 0.000000)))
    ))

    """
    List of triangular faces with edges B-C-C
    """
    triangles_bcc = np.array((
        (np.array((-0.000000, 0.111803, 0.223607)),
         np.array((0.111803, 0.000000, 0.223607)),
         np.array((0.144338, 0.144338, 0.144338))),
        (np.array((0.111803, 0.000000, 0.223607)),
         np.array((0.223607, 0.000000, 0.111803)),
         np.array((0.144338, 0.144338, 0.144338))),
        (np.array((0.223607, 0.111803, 0.000000)),
         np.array((0.223607, 0.000000, 0.111803)),
         np.array((0.144338, 0.144338, 0.144338))),
        (np.array((0.111803, 0.223607, 0.000000)),
         np.array((0.223607, 0.111803, 0.000000)),
         np.array((0.144338, 0.144338, 0.144338))),
        (np.array((-0.000000, 0.223607, 0.111803)),
         np.array((-0.000000, 0.111803, 0.223607)),
         np.array((0.144338, 0.144338, 0.144338))),
        (np.array((-0.000000, 0.223607, 0.111803)),
         np.array((0.111803, 0.223607, 0.000000)),
         np.array((0.144338, 0.144338, 0.144338)))
    ))
