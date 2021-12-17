import networkx as nx  # Library for graphs manipulation
import numpy as np
from triangulate import *


def load_polyfile(filename):
    """Load the polyfile of the file filename and return the associated graph"""
    verts, edges = get_datas(filename)
    graph = nx.Graph()

    for i, position in enumerate(verts):
        graph.add_node(i, pos=position)

    for e in edges:
        graph.add_edge(*e)

    return graph


def compute_h(g, e_matrix):
    """Compute H for an edge e (e_matrix) associated to the matrix g"""
    mat1 = np.array([[-1, 0, 1, 0, 0, 0, 0, 0],
                     [0, -1, 0, 1, 0, 0, 0, 0]])

    mat3 = np.matmul(np.transpose(g), g)  # GT * G
    mat3 = np.linalg.inv(mat3)  # (GT * G)^-1
    mat3 = np.matmul(mat3, g)  # (GT * G)^-1 * G

    return mat1 - np.matmul(e_matrix, mat3)


def n(graphe, edge_to_compute):
    """Find the point useful to compute a new edge (see schema of paper)"""
    v1, v2 = edge_to_compute
    liste = [v1, v2]
    for neighbour in graphe.adj(v1):
        if neighbour in graphe.adj(v2):
            liste.append(neighbour)
            if len(liste) == 4:
                return liste

    # Only 3 points
    liste.append(None)

    return liste


handles = [1, 2]

#  Récupérer les points à modifier
graphe_polyfile = load_polyfile("A.poly")

# Créer un nouveau gk avec les points à modifier
new_graph = graphe_polyfile.subgraph(graphe_polyfile.nodes)


def compute_g(vertices_list):
    """Compute the matrix G associated to the vertices vertices_list"""
    gk_list = []
    for vertex in vertices_list:
        vx = vertex['pos'](0)
        vy = vertex['pos'](1)

        gk_list.append(vx)
        gk_list.append(vy)
        gk_list.append(vy)
        gk_list.append(-vx)

    return np.array(gk_list).reshape((8, 2))


def compute_a1_b1(w):
    a1 = []
    b = []

    for edge in new_graph.edges:
        l1 = [0 for i in range(len(new_graph.nodes) * 2)]
        l2 = [0 for i in range(len(new_graph.nodes) * 2)]

        # Compute Gk
        vertices = n(graphe_polyfile, edge)
        gk = compute_g(vertices)

        vl = vertices[3]

        # Compute ek_matrix
        vi, vj = np.array(edge[0]), np.array(edge[1])
        ek = vj - vi
        ekx, eky = ek[0], ek[1]
        ek_matrix = np.array([ekx, eky, eky, -ekx]).reshape((2, 2))

        # Comput h
        h = compute_h(gk, ek_matrix)

        # Add the bloc associated to vi
        l1[vi * 2] = h[0][0]
        l1[vi * 2 + 1] = h[0][1]
        l2[vi * 2] = h[1][0]
        l2[vi * 2 + 1] = h[1][1]

        # Add the bloc associated to vj
        l1[vj * 2] = h[0][2]
        l1[vj * 2 + 1] = h[0][3]
        l2[vj * 2] = h[1][2]
        l2[vj * 2 + 1] = h[1][3]

        # Add the bloc associated to vl
        l1[vl * 2] = h[0][4]
        l1[vl * 2 + 1] = h[0][5]
        l2[vl * 2] = h[1][4]
        l2[vl * 2 + 1] = h[1][5]

        if len(vertices) == 4:
            # Not a border
            vr = vertices[4]

            # Add the bloc associated to vr
            l1[vr * 2] = h[0][6]
            l1[vr * 2 + 1] = h[0][7]
            l2[vr * 2] = h[1][6]
            l2[vr * 2 + 1] = h[1][7]

        # Add tow ligne to matrix a
        a1.append(l1)
        a1.append(l2)

        # Add tow 0 in matrix b
        b.append(0)
        b.append(0)

    for p in handles:
        l1 = [0 for i in range(len(new_graph.nodes) * 2)]
        l2 = [0 for i in range(len(new_graph.nodes) * 2)]

        l1[2*p] = w
        l2[2*p+1] = w

        # Add tow ligne to matrix a
        a1.append(l1)
        a1.append(l2)

        # Add tow ligne to matrix    b
        b.append(w * graphe_polyfile.nodes[p][0])
        b.append(w * graphe_polyfile.nodes[p][1])

    return np.array(a1), np.transpose(np.array(b))


def compute_a2_b2(w, vprime):
    a2 = []
    b2_x = []
    b2_y = []

    for edge in new_graph.edges:
        l1 = [0 for i in range(len(new_graph.nodes) * 2)]

        # Compute Gk
        vertices = n(graphe_polyfile, edge)
        gk = compute_g(vertices)

        vl = vertices[3]

        # Compute ek_matrix
        vi, vj = np.array(edge[0]), np.array(edge[1])
        ek = vj - vi
        ekx, eky = ek[0], ek[1]
        ek_matrix = np.array([ekx, eky, eky, -ekx]).reshape((2, 2))

        vi = (vprime[2 * vi], vprime[2 * vi + 1])
        vj = (vprime[2 * vj], vprime[2 * vj + 1])
        vl = (vprime[2 * vl], vprime[2 * vl + 1])

        if len(vertices) == 4:
            # Not a border
            vr = vertices[4]
            vr = (vprime[2 * vr], vprime[2 * vr + 1])
        else:
            vr = (0, 0)

        coordinates = [vi[0], vi[1], vj[0], vj[1],
                       vl[0], vl[1], vr[0], vr[1]]
        coordinates = np.transpose(np.array(coordinates))

        # on calcul Gkt * Gk
        mat3 = np.matmul(np.transpose(gk), gk)
        # on calcul (Gkt*Gk)-1
        mat3 = np.linalg.inv(mat3)
        # on calcul mat3 [ck, sk]
        mat3 = np.matmul(mat3, np.transpose(gk))
        mat3 = np.transpose(np.matmul(mat3, coordinates))
        ck = mat3[0]
        sk = mat3[1]

        # on calcul Tk
        a = 1 / (ck ** 2 + sk ** 2)
        tk = [[a * ck, a * sk],
              [-a * sk, a * ck]]

        # Calcul de A2
        # on veut calculer vi''-vj'' - T'i edge_k
        l1[vi] = -1  # vi''
        l1[vj] = 1  # -vj''

        # on ajoute la ligne dans A2
        a2.append(l1)

        # calcul de b
        # edge_k [ekx,
        #    eky]
        ek = np.transpose(np.array(ek))
        # b = Tkek
        ek = np.transpose(np.matmul(tk, ek))
        # on ajoute dans b2_x et b2_y
        b2_x.append(ek[0])
        b2_y.append(ek[1])



    for p in handles:
        l1 = [0 for i in range(len(new_graph.nodes) * 2)]
        l2 = [0 for i in range(len(new_graph.nodes) * 2)]

        l1[2*p] = w
        l2[2*p+1] = w

        # Add tow ligne to matrix a
        a1.append(l1)
        a1.append(l2)

        # Add tow ligne to matrix    b
        b.append(w * graphe_polyfile.nodes[p][0])
        b.append(w * graphe_polyfile.nodes[p][1])

    return np.array(a1), np.transpose(np.array(b))
