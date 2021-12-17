import networkx as nx  # Library for graphs manipulation
import numpy as np
from triangulate import *


def load_polyfile(f_name):
    """Load the polyfile of the file f_name and return the associated graph"""
    verts, edges = get_datas(f_name)
    graph = nx.Graph()

    # Create vertices
    for i, position in enumerate(verts):
        graph.add_node(i, pos=position)

    # Create edges
    for e in edges:
        graph.add_edge(e[0] - 1, e[1] - 1)  # We subtract 1 because indice of vertex start to 1 instead of 0

    return graph


def compute_h(g, e_matrix):
    """Compute H for an edge e associated to the matrix e_matrix and g"""
    mat1 = np.array([[-1, 0, 1, 0, 0, 0, 0, 0],
                     [0, -1, 0, 1, 0, 0, 0, 0]])

    mat3 = np.matmul(np.transpose(g), g)  # GT * G
    mat3 = np.linalg.inv(mat3)  # (GT * G)^-1
    mat3 = np.matmul(mat3, np.transpose(g))  # (GT * G)^-1 * G

    return mat1 - np.matmul(e_matrix, mat3)


def n(graphe, edge_to_compute):
    """Find the point useful to compute a new edge (see schema of paper)"""
    v1, v2 = edge_to_compute
    liste = [v1, v2]
    for neighbour in graphe.adj[v1]:
        if neighbour in graphe.adj[v2]:
            liste.append(neighbour)
            if len(liste) == 4:
                # Enough points
                return liste

    return liste


def compute_g(graphe, vertices):
    """Compute the matrix G associated to the vertices vertices_list"""
    gk_list = []
    for vertex in vertices:
        vx = graphe.nodes[vertex]['pos'][0]
        vy = graphe.nodes[vertex]['pos'][1]

        gk_list.append(vx)
        gk_list.append(vy)
        gk_list.append(vy)
        gk_list.append(-vx)

    if len(vertices) == 3:
        # We ere on the border of the polyline : we add a null point
        gk_list.append(0)
        gk_list.append(0)
        gk_list.append(0)
        gk_list.append(0)

    return np.array(gk_list).reshape((8, 2))


def compute_a1_b1(graphe, handles, w):
    """Compute A1 and b1 for the first step of the laplacian edition of the graphe with the parameter w."""
    a1 = []
    b = []

    for edge in graphe.edges:
        l1 = [0 for _ in range(len(graphe.nodes) * 2)]
        l2 = [0 for _ in range(len(graphe.nodes) * 2)]

        # Compute Gk
        vertices = n(graphe, edge)
        gk = compute_g(graphe, vertices)

        # Compute ek_matrix
        vi, vj = np.array(graphe.nodes[edge[0]]['pos']), np.array(graphe.nodes[edge[1]]['pos'])
        ek = vj - vi
        ekx, eky = ek[0], ek[1]
        ek_matrix = np.array([ekx, eky, eky, -ekx]).reshape((2, 2))

        # Comput h
        h = compute_h(gk, ek_matrix)

        i, j, l = vertices[0], vertices[1], vertices[2]
        # Add the bloc associated to vi
        l1[i * 2] = h[0][0]
        l1[i * 2 + 1] = h[0][1]
        l2[i * 2] = h[1][0]
        l2[i * 2 + 1] = h[1][1]

        # Add the bloc associated to vj
        l1[j * 2] = h[0][2]
        l1[j * 2 + 1] = h[0][3]
        l2[j * 2] = h[1][2]
        l2[j * 2 + 1] = h[1][3]

        # Add the bloc associated to vl
        l1[l * 2] = h[0][4]
        l1[l * 2 + 1] = h[0][5]
        l2[l * 2] = h[1][4]
        l2[l * 2 + 1] = h[1][5]

        if len(vertices) == 4:
            # Not a border
            r = vertices[3]

            # Add the bloc associated to vr
            l1[r * 2] = h[0][6]
            l1[r * 2 + 1] = h[0][7]
            l2[r * 2] = h[1][6]
            l2[r * 2 + 1] = h[1][7]

        # Add two ligne to matrix a
        a1.append(l1)
        a1.append(l2)

        # Add two 0 in matrix b
        b.append(0)
        b.append(0)

    for p in handles:
        l1 = [0 for _ in range(len(graphe.nodes) * 2)]
        l2 = [0 for _ in range(len(graphe.nodes) * 2)]

        l1[2*p] = w
        l2[2*p+1] = w

        # Add two lines to matrix a
        a1.append(l1)
        a1.append(l2)

        # Add two lines to matrix    b
        b.append(w * graphe.nodes[p]['pos'][0])
        b.append(w * graphe.nodes[p]['pos'][1])

    return np.array(a1), np.transpose(np.array(b))


def compute_a2_b2(graphe, handles, v_prime, w):
    a2 = []
    b2_x = []
    b2_y = []

    for edge in graphe.edges:
        l1 = [0 for _ in range(len(graphe.nodes) * 2)]

        # Compute Gk
        vertices = n(graphe, edge)
        gk = compute_g(graphe, vertices)

        # Compute ek_matrix
        i, j, l = vertices[0], vertices[1], vertices[2]
        vi, vj = np.array(graphe.nodes[edge[0]]['pos']), np.array(graphe.nodes[edge[1]]['pos'])
        ek = vj - vi

        vi = (v_prime[2 * i], v_prime[2 * i + 1])
        vj = (v_prime[2 * j], v_prime[2 * j + 1])
        vl = (v_prime[2 * l], v_prime[2 * l + 1])

        if len(vertices) == 4:
            # Not a border
            r = vertices[3]
            vr = (v_prime[2 * r], v_prime[2 * r + 1])
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
        l1[i] = -1  # vi''
        l1[j] = 1  # -vj''

        # on ajoute la ligne dans A2
        a2.append(l1)

        # calcul de b
        # edge_k [ekx,
        #    eky]
        ek = np.transpose(ek)
        # b = Tk * ek
        ek = np.transpose(np.matmul(tk, ek))
        # on ajoute dans b2_x et b2_y
        b2_x.append(ek[0])
        b2_y.append(ek[1])

    # on ajoute maintenant la partie point fixe de la matrice
    for p in handles:
        l1 = [0 for _ in range(len(graphe.nodes) * 2)]
        l1[p] = w

        # on ajoute les deux lignes dans la matrice
        a2.append(l1)

        # on ajoute 2 lignes dans b
        b2_x.append(w * graphe.nodes[p]['pos'][0])
        b2_y.append(w * graphe.nodes[p]['pos'][1])

    return np.array(a2), np.array(b2_x), np.array(b2_y)


def compute_new_points(handles, w):
    #  Récupérer les points à modifier
    graphe_polyfile = load_polyfile("A")
    for i in handles:
        graphe_polyfile.nodes[i]['pos'][0] = graphe_polyfile.nodes[i]['pos'][0] + 0.01
    a1, b1 = compute_a1_b1(graphe_polyfile, handles, w)
    a = np.matmul(np.transpose(a1), a1)
    b = np.matmul(np.transpose(a1), b1)

    # on résout l'équation
    v_prime = np.linalg.solve(a, b)

    # on fixe le scale
    a2, b2_x, b2_y = compute_a2_b2(graphe_polyfile, handles, v_prime, w)
    a = np.matmul(np.transpose(a2), a2)
    b_x = np.matmul(np.transpose(a2), b2_x)
    b_y = np.matmul(np.transpose(a2), b2_y)

    # TODO : Erreur 'Numpy error: Matrix is singular' -> matrice pas inversible = pas unique solution
    vx = np.linalg.solve(a, b_x)
    vy = np.linalg.solve(a, b_y)
    return vx, vy


if __name__ == '__main__':
    vx_array, vy_array = compute_new_points([1, 2], 1000)
