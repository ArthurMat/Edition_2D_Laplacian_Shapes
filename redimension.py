#!/usr/bin/env python3

def to_pygame(points, HEIGHT):
    for key in points:
        points[key][1] =  0.9 * HEIGHT - points[key][1]
    return points

def rescale(points, WIDTH, HEIGHT, mini_X, maxi_Y):
    for key in points:
        points[key][1] += (0.9 * HEIGHT - maxi_Y) / 2
        points[key][0] -= (mini_X - 0.1 * WIDTH) / 2
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
    return rescale(points, WIDTH, HEIGHT, mini_X * ratio, maxi_Y * ratio)
