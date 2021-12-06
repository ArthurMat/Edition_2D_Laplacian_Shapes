#!/usr/bin/env python3

from math import sqrt

def distance(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def find_nearest(points, pos):
    neighbor = None
    dist_min = None
    for key, value in points.items():
        dist = distance(value, pos)
        if dist_min == None or dist_min > dist:
            neighbor = value
            dist_min = dist
    return neighbor

def inside(points, pos, pos2):
    liste = []
    for key, value in points.items():
        if min(pos[0], pos2[0]) < value[0] < max(pos[0], pos2[0]) and min(pos[1], pos2[1]) < value[1] < max(pos[1], pos2[1]):
            liste.append(value)
    return liste
    