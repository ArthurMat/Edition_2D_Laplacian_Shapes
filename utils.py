import networkx as nx
import numpy as np
import scipy
from triangulate import *

def load_polyfile(filename):
    vertices, edges = get_datas(filename)
    graph = nx.Graph()

    for i, coords in enumerate(vertices):
        graph.add_node(i, pos=coords)

    for edge in edges:
        graph.add_edge(*edge)

    return graph



def get_L(g):
    lap = nx.laplacian_matrix(g)  # D - A

    degrees_inv = []
    for vertice in g.nodes:
        degrees_inv.append(1 / len(g.adj(vertice)))

    inv_deg = np.diag(degrees_inv) # Matrice des inverses des degrées D^-1 (mmatrice diagonale)

    return inv_deg.dot(lap)