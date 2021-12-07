#!/usr/bin/env python3

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
