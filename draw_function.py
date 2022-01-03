#!/usr/bin/env python3

import sys
import pygame
from tools import *
from copy import deepcopy
from constant import *
from laplacian import *

def draw_poly(screen, points, seg, item, seg_proche):
    for key, value in seg.items():
        if item and key == seg_proche:
            pygame.draw.line(screen, color=RED, start_pos=points[value[0]], end_pos=points[value[1]], width=2)
        else:
            pygame.draw.line(screen, color=BLACK, start_pos=points[value[0]], end_pos=points[value[1]], width=2)

def draw_points(screen, data):
    for key, value in data.points.items():
        pygame.draw.circle(screen, color=BLACK, center=value, radius=max(min(4, min(data.WIDTH, data.HEIGHT)* 0.009),1.75))

def select(points, pos, pos2):
    liste = inside(points, pos, pos2)
    if len(liste) == 0:
        cercle = find_nearest(points, pos)
        liste.append(cercle)
    return liste

def move(points, liste_cercles, pos, pos2):
    dx = (pos2[0] - pos[0]) / 1  # Gain
    dy = (pos2[1] - pos[1]) / 1  # Gain
    for key in liste_cercles:
        points[key][0] += dx
        points[key][1] += dy

def move2(points, seg, liste_cercles, pos, pos2):
    arr = compute_new_points(points, seg, liste_cercles, w=1000)
    return arr


def reset_button(screen, WIDTH, HEIGHT):
    pi = 3.14159265359
    rec = pygame.Rect(WIDTH*0.95 - HEIGHT*0.012, HEIGHT*0.012, HEIGHT*0.025, HEIGHT*0.025)
    pygame.draw.circle(screen, color=DARK_RED, center=(WIDTH*0.95, HEIGHT*0.05/2), radius=HEIGHT*0.02)
    pygame.draw.arc(screen, color=WHITE, rect=rec, start_angle=pi, stop_angle=pi/2, width=3)

def s(screen, WIDTH, HEIGHT, white):
    if white:
        color = WHITE
    else:
        color = BLACK
    pi = 3.14159265359
    rec = pygame.Rect(WIDTH*0.05-HEIGHT*0.0125,HEIGHT*0.0125, HEIGHT*0.025, HEIGHT*0.0175)
    rec2 = pygame.Rect(WIDTH*0.05-HEIGHT*0.0125,HEIGHT*0.025, HEIGHT*0.025, HEIGHT*0.0175)
    pygame.draw.arc(screen, color, rect=rec, start_angle=pi/3, stop_angle=3*pi/2, width=3)
    pygame.draw.arc(screen, color, rect=rec2, start_angle=4*pi/3, stop_angle=pi/2, width=3)

def m(screen, WIDTH, HEIGHT, white):
    if white:
        color = WHITE
    else:
        color = BLACK
    points=[[WIDTH*0.11-HEIGHT*0.011, HEIGHT*0.032], [WIDTH*0.11-HEIGHT*0.011, HEIGHT*0.013], [WIDTH*0.11, HEIGHT*0.025], [WIDTH*0.11+HEIGHT*0.011, HEIGHT*0.013], [WIDTH*0.11+HEIGHT*0.011, HEIGHT*0.032]]
    pygame.draw.lines(screen, color, closed=False, points=points, width=3)

def add_remove(screen, data, mode, item):
    p=[[data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005],
       [data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.045],
       [data.WIDTH*0.45 + data.HEIGHT*0.1, data.HEIGHT*0.045],
       [data.WIDTH*0.45 + data.HEIGHT*0.1, data.HEIGHT*0.005]]
    if mode < 2:
        pygame.draw.circle(screen, color=BLUE_OFF, center=(data.WIDTH*0.45, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.rect(screen, color=GRAY_OFF, rect=pygame.Rect(data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005, data.HEIGHT*0.06, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=BLACK, closed=True, points=p, width=2)
    else:
        pygame.draw.circle(screen, color=LIGHT_BLUE, center=(data.WIDTH*0.45, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.rect(screen, color=LIGHT_GRAY, rect=pygame.Rect(data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005, data.HEIGHT*0.06, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=BLACK, closed=True, points=p, width=2)
        pygame.draw.rect(screen,color=VERY_LIGHT_GRAY, rect=pygame.Rect(data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.005, data.HEIGHT*0.03, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=BLACK, closed=True, points=[[data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.005], [data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.045], [data.WIDTH*0.45 + data.HEIGHT*0.14, data.HEIGHT*0.045], [data.WIDTH*0.45 + data.HEIGHT*0.14, data.HEIGHT*0.005]], width=2)
        pygame.draw.rect(screen, color=WHITE, rect=pygame.Rect(data.WIDTH*0.45-data.HEIGHT*0.015, data.HEIGHT*0.0225, data.HEIGHT*0.03, data.HEIGHT*0.005))
        pygame.draw.polygon(screen, color=BLACK, points=[[data.WIDTH*0.45 + data.HEIGHT*0.115, data.HEIGHT*0.02], [data.WIDTH*0.45 + data.HEIGHT*0.135, data.HEIGHT*0.02], [data.WIDTH*0.45 + data.HEIGHT*0.125, data.HEIGHT*0.01]])
        pygame.draw.polygon(screen, color=BLACK, points=[[data.WIDTH*0.45 + data.HEIGHT*0.115, data.HEIGHT*0.03], [data.WIDTH*0.45 + data.HEIGHT*0.135, data.HEIGHT*0.03], [data.WIDTH*0.45 + data.HEIGHT*0.125, data.HEIGHT*0.04]])
        if mode == 3:  # mode ajout
            pygame.draw.rect(screen, color=WHITE, rect=pygame.Rect(data.WIDTH*0.45-data.HEIGHT*0.0025, data.HEIGHT*0.01, data.HEIGHT*0.005, data.HEIGHT*0.03))
        else:  # mode suppression
            pygame.draw.circle(screen, color=LIGHT_RED, center=(data.WIDTH*0.45 - data.HEIGHT*0.04, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.015)
            pygame.draw.rect(screen, color=WHITE, rect=pygame.Rect(data.WIDTH*0.45-data.HEIGHT*0.051, data.HEIGHT*0.0225, data.HEIGHT*0.02, data.HEIGHT*0.005))
        if item:  # segment
            pygame.draw.line(screen, color=BLACK, start_pos=[data.WIDTH*0.45 + data.HEIGHT*0.05, data.HEIGHT*0.025], end_pos=[data.WIDTH*0.45 + data.HEIGHT*0.09, data.HEIGHT*0.025], width=3)
        else:  # point
            pygame.draw.circle(screen, color=BLACK, center=(data.WIDTH*0.45 + data.HEIGHT*0.07, data.HEIGHT*0.025), radius=data.HEIGHT*0.015)

def update(screen, data, mode, item, seg_proche):
    # Screen
    screen.fill(WHITE)
    # Polyline
    draw_poly(screen, data.points, data.seg, item, seg_proche)
    # Toolbar
    pygame.draw.rect(screen, GRAY, pygame.Rect(0, 0, data.WIDTH, 0.05 * data.HEIGHT))
    add_remove(screen, data, mode, item)
    # Buttons
    if mode > 1:
        draw_points(screen, data)
        pygame.draw.circle(screen, color=RED_OFF, center=(data.WIDTH*0.05, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.circle(screen, color=GREEN_OFF, center=(data.WIDTH*0.11, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        s(screen, data.WIDTH, data.HEIGHT, 0)
        m(screen, data.WIDTH, data.HEIGHT, 0)
    elif mode == 0:
        pygame.draw.circle(screen, color=RED, center=(data.WIDTH*0.05, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.circle(screen, color=GREEN_OFF, center=(data.WIDTH*0.11, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        s(screen, data.WIDTH, data.HEIGHT, 1)
        m(screen, data.WIDTH, data.HEIGHT, 0)
    elif mode == 1:
        pygame.draw.circle(screen, color=RED_OFF, center=(data.WIDTH*0.05, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.circle(screen, color=GREEN, center=(data.WIDTH*0.11, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        s(screen, data.WIDTH, data.HEIGHT, 0)
        m(screen, data.WIDTH, data.HEIGHT, 1)
    # if data.load:
    #     pygame.draw.circle(screen, color=ORANGE, center=(data.WIDTH*0.75, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
    #     pygame.draw.circle(screen, color=ORANGE_OFF, center=(data.WIDTH*0.75 + data.HEIGHT*0.06, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
    # else:
    #     pygame.draw.circle(screen, color=ORANGE_OFF, center=(data.WIDTH*0.75, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
    #     pygame.draw.circle(screen, color=ORANGE, center=(data.WIDTH*0.75 + data.HEIGHT*0.06, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
    reset_button(screen, data.WIDTH, data.HEIGHT)
    # Nodes
    for key in data.liste_cercles:
        pygame.draw.circle(screen, color=RED, center=data.points[key], radius=max(min(4, min(data.WIDTH, data.HEIGHT)* 0.009),1.75))
