#!/usr/bin/env python3

from math import sqrt
from copy import deepcopy
import numpy as np

def distance(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def find_nearest(points, pos):
    neighbor = None
    dist_min = None
    for key, value in points.items():
        dist = distance(value, pos)
        if dist_min == None or dist_min > dist:
            neighbor = key
            dist_min = dist
    return neighbor

def inside(points, pos, pos2):
    liste = []
    for key, value in points.items():
        if min(pos[0], pos2[0]) < value[0] < max(pos[0], pos2[0]) and min(pos[1], pos2[1]) < value[1] < max(pos[1], pos2[1]):
            liste.append(key)
    return liste

def to_pygame(points, WIDTH, HEIGHT):
    mini_X, maxi_X, mini_Y, maxi_Y = min_max(points)
    for key in points:
        points[key][1] =  maxi_Y - points[key][1]
    return points

def recenter(points, WIDTH, HEIGHT):
    mini_X, maxi_X, mini_Y, maxi_Y = min_max(points)
    dx = maxi_X - mini_X
    dy = maxi_Y - mini_Y
    pos_min_X = ((WIDTH - dx) / 2) - mini_X
    pos_min_Y = ((HEIGHT - dy) / 2) - mini_Y
    for key in points:
        points[key][0] += pos_min_X
        points[key][1] += pos_min_Y + 0.05 * HEIGHT  # Pour decentrer vers le bas (bar d'outils)
    return points

def min_max(points):
    mini_X, maxi_X = None, None
    mini_Y, maxi_Y = None, None
    for key, value in points.items():
        if mini_X == None or mini_X > value[0]:
            mini_X = value[0]
        if mini_Y == None or mini_Y > value[1]:
            mini_Y = value[1]
        if maxi_X == None or maxi_X < points[key][0]:
            maxi_X = points[key][0]
        if maxi_Y == None or maxi_Y < points[key][1]:
            maxi_Y = points[key][1]
    return mini_X, maxi_X, mini_Y, maxi_Y

def redimension(points, WIDTH, HEIGHT):
    mini_X, maxi_X, mini_Y, maxi_Y = min_max(points)
    add_X, add_Y = False, False
    if mini_X <= 0:
        add_X = True
        mini_X = abs(mini_X)
        maxi_X += mini_X
    if mini_Y <= 0:
        add_Y = True
        mini_Y = abs(mini_Y)
        maxi_Y += mini_Y
    ratio = 0.9 * min(WIDTH, HEIGHT) / max(maxi_X, maxi_Y) # modifier ration *0.9 pour laisser une marge et onc modifier aussi to_pygame
    for key in points:
        if add_X:
            points[key][0] += mini_X
        if add_Y:
            points[key][1] += mini_Y
        points[key][0] *= ratio
        points[key][1] *= ratio
    return recenter(points, WIDTH, HEIGHT)

def array_to_dict(liste):
    dico = dict()
    for i, elmt in enumerate(liste):
        dico[i+1] = elmt
    return dico

def coeff_dir(pt1, pt2):
    if pt1[1] == pt2[1]:
        pt1[1] += 0.0001
    if pt1[0] == pt2[0]:
        pt1[0] += 0.0001
    return (pt1[1] - pt2[1]) / (pt1[0] - pt2[0])

def equ_droite(pt1, pt2):
    a = coeff_dir(pt1, pt2)
    b = pt1[1] - pt1[0] * a
    return a, b

def dist_seg(pos, segment):
    a, b = equ_droite(segment[0], segment[1])
    ap = -1/a
    bp = pos[1] - pos[0] * ap
    m = np.array([[-a, 1], [-ap, 1]])
    n = np.array([b, bp])
    x = np.linalg.solve(m,n)
    return distance(pos, x), x

def nearest_seg(points, seg, pos):
    lmb = 20
    near = None
    dist_min = None
    for key, val in seg.items(): 
        dist, x = dist_seg(pos, [points[val[0]], points[val[1]]])
        if (points[val[0]][0] - lmb <= x[0] <= points[val[1]][0] + lmb or points[val[0]][0] + lmb >= x[0] >= points[val[1]][0] - lmb) and (points[val[0]][1] - lmb <= x[1] <= points[val[1]][1] + lmb or points[val[0]][1] + lmb >= x[1] >= points[val[1]][1] - lmb):
            if dist_min == None or dist < dist_min:
                near = key
                dist_min = dist
    return near

def dico_cleaner(dico):
    result = dict()
    cptr = 0
    for k in dico.keys():
        if dico[k] in result.values() or [dico[k][1], dico[k][0]] in result.values():
            continue
        else:
            cptr += 1
            result[cptr] = dico[k]
    return result
