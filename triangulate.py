#!/usr/bin/env python3

import subprocess
import os
import sys

def triangulate(filename):
    """Crée une triangulation de Delaunay sous contrainte avec une aire maximum de 0.01 (argument de -a)"""

    return_code = subprocess.call(["./triangle", "-a5", filename])

    if return_code != 0:
        print("Erreur dans la triangulation")


def get_lines(filename, func):
    list_lines = open(filename,'r').read().split('\n')
    lines = []

    for line in list_lines:
        if len(line) > 0 and line[0] == "#":
            continue

        # On utilsie try car is on tente de convertir en int des floats on aura une erreur
        try:
            lines.append([func(i) for i in line.split()])
        except:
            continue

    return lines


def get_datas(filename):
    """Renvoie la liste des sommets et des segments asssociés à une triangulation de fichier"""
    vertices = []
    segments = []

    # Lecture des sommets
    lines_float = get_lines(filename + ".1.node", float)
    nb_vertices, dimension = int(lines_float[0][0]), int(lines_float[0][1])
    
    if dimension != 2:
        print("Erreur : Dimension des sommets différente de 2.")
        return

    for i in range(1, nb_vertices + 1):
        vertices.append([lines_float[i][1], lines_float[i][2]])


    # Lecture de la polyligne
    with open(filename + ".1.poly", "r") as f:
        lines_int = get_lines(filename + ".1.poly", int)
    
    nb_segments = lines_int[1][0]
    for i in range(2, nb_segments + 1):
        segments.append([lines_int[i][1], lines_int[i][2]])
    
    # Lecture des triangles
    lines_int = get_lines(filename + ".1.ele", int)
    
    nb_segments = lines_int[0][0]
    for i in range(1, nb_segments + 1):
        v1, v2, v3 = lines_int[i][1], lines_int[i][2], lines_int[i][3]

        if [v1, v2] not in segments and [v2, v1] not in segments:
            segments.append([v1, v2])
        if [v2, v3] not in segments and [v3, v2] not in segments:
            segments.append([v2, v3])
        if [v3, v1] not in segments and [v1, v3] not in segments:
            segments.append([v3, v1])
        
    return vertices, segments


if __name__ == "__main__":
    triangulate(sys.argv[1])

    filename = os.path.splitext(sys.argv[1])[0]
    get_datas(filename)
