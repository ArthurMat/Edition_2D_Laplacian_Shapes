#!/usr/bin/env python3

import pygame
import sys

def draw(screen, points, seg):
    for key, value in seg.items():
        pygame.draw.line(screen, color=(0, 0, 0), start_pos=points[value[0]], end_pos=points[value[1]], width=2)

def to_pygame(points, HEIGHT, mini_X, maxi_Y):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    for key in points:
        points[key][1] += (HEIGHT - maxi_Y) / 2
        points[key][1] = HEIGHT - points[key][1]
        points[key][0] -= mini_X / 2
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
    ratio = min(WIDTH, HEIGHT) / max(maxi_X, maxi_Y)
    for key in points:
        if add_X:
            points[key][0] += mini_X
        if add_Y:
            points[key][1] += mini_Y
        points[key][0] *= ratio
        points[key][1] *= ratio
    return to_pygame(points, HEIGHT, mini_X * ratio, maxi_Y * ratio)

def main_interface(points, seg, WIDTH=1000, HEIGHT=1000):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    clock = pygame.time.Clock()

    points = redimension(points, WIDTH, HEIGHT)

    screen.fill((255, 255, 255))
    draw(screen, points, seg)

    pygame.display.update()

    pause_flag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    pause_flag = not pause_flag
        if pause_flag:
            pygame.display.update()