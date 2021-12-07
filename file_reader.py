#!/usr/bin/env python3

def skip_space(ligne, i):
    char = ligne[i]
    while char == " ":
        i += 1
        char = ligne[i]
    return i

def read_int(ligne, i):
    tmp = ""
    i = skip_space(ligne, i)
    char = ligne[i]
    while char != " ":
        tmp += char
        i += 1
        if i == len(ligne):
            break
        char = ligne[i]
    return int(tmp), i

def read_float(ligne, i):
    tmp = ""
    i = skip_space(ligne, i)
    char = ligne[i]
    while char != " ":
        tmp += char
        i += 1
        if i == len(ligne):
            break
        char = ligne[i]
    return float(tmp), i

def first_line(ligne):
    i = 0
    nb_point, i = read_int(ligne, i)
    deuxD, i = read_int(ligne, i)
    if deuxD != 2:
        raise ValueError('Given file is not a 2D polyline')
    return nb_point


def to_dict(path):
    if path[-5:] != ".poly":
        raise ValueError("Given file has not the good extention (.poly)")
    prem_ligne, seg_line = False, False
    nb_point, nb_seg = 0, 0
    cptr = 1
    dico_points = dict()
    dico_seg = dict()
    with open(path, "r") as fichier:
        for ligne in fichier:
            if ligne[0] == "#":
                continue
            if not prem_ligne:
                prem_ligne = True
                nb_point = first_line(ligne)
            else:
                if cptr <= nb_point and not seg_line:
                    i = 0
                    key, i = read_int(ligne, i)
                    x, i = read_float(ligne, i)
                    y, i = read_float(ligne, i)
                    dico_points[key] = [x, y]
                elif cptr <= nb_seg and seg_line:
                    i = 0
                    key, i = read_int(ligne, i)
                    x, i = read_int(ligne, i)
                    y, i = read_int(ligne, i)
                    dico_seg[key] = [x, y]
                elif prem_ligne and not seg_line:
                    seg_line = True
                    i = 0
                    cptr = 0
                    nb_seg, i = read_int(ligne, i)
                cptr += 1
    return dico_points, dico_seg
            