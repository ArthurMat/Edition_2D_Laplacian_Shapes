#!/usr/bin/env python3

import sys
import pygame
from tools import *
from copy import deepcopy
from constant import *
from laplacian import *

def draw_poly(screen, data, item, seg_proche):
    for key, value in data.seg.items():
        if item and key == seg_proche:
            pygame.draw.line(screen, color=RED, start_pos=data.points[value[0]], end_pos=data.points[value[1]], width=2)
        else:
            pygame.draw.line(screen, color=BLACK[data.day], start_pos=data.points[value[0]], end_pos=data.points[value[1]], width=2)

def draw_points(screen, data):
    for key, value in data.points.items():
        pygame.draw.circle(screen, color=BLACK[data.day], center=value, radius=max(min(4, min(data.WIDTH, data.HEIGHT)* 0.009),1.75))

def select(points, pos, pos2):
    liste = inside(points, pos, pos2)
    if len(liste) == 0:
        cercle = find_nearest(points, pos)
        liste.append(cercle)
    return liste

def move(points, handles, pos, pos2):
    dx = (pos2[0] - pos[0]) / 1  # Gain
    dy = (pos2[1] - pos[1]) / 1  # Gain
    for key in handles:
        points[key][0] += dx
        points[key][1] += dy

def move2(points, seg, handles, old_coords):
    arr = compute_new_points(points, seg, handles, old_coords, w=1000)
    return arr


def reset_button(screen, data):
    pi = 3.14159265359
    rec = pygame.Rect(data.WIDTH*0.95 - data.HEIGHT*0.012, data.HEIGHT*0.012, data.HEIGHT*0.025, data.HEIGHT*0.025)
    pygame.draw.circle(screen, color=DARK_RED, center=(data.WIDTH*0.95, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
    pygame.draw.arc(screen, color=WHITE[0], rect=rec, start_angle=pi, stop_angle=pi/2, width=3)

def s(screen, WIDTH, HEIGHT, BLANC):
    if BLANC:
        color = WHITE[0]
    else:
        color = BLACK[0]
    pi = 3.14159265359
    rec = pygame.Rect(WIDTH*0.05-HEIGHT*0.0125,HEIGHT*0.0125, HEIGHT*0.025, HEIGHT*0.0175)
    rec2 = pygame.Rect(WIDTH*0.05-HEIGHT*0.0125,HEIGHT*0.025, HEIGHT*0.025, HEIGHT*0.0175)
    pygame.draw.arc(screen, color, rect=rec, start_angle=pi/3, stop_angle=3*pi/2, width=3)
    pygame.draw.arc(screen, color, rect=rec2, start_angle=4*pi/3, stop_angle=pi/2, width=3)

def m(screen, WIDTH, HEIGHT, BLANC):
    if BLANC:
        color = WHITE[0]
    else:
        color = BLACK[0]
    points=[[WIDTH*0.11-HEIGHT*0.011, HEIGHT*0.032], [WIDTH*0.11-HEIGHT*0.011, HEIGHT*0.013], [WIDTH*0.11, HEIGHT*0.025], [WIDTH*0.11+HEIGHT*0.011, HEIGHT*0.013], [WIDTH*0.11+HEIGHT*0.011, HEIGHT*0.032]]
    pygame.draw.lines(screen, color, closed=False, points=points, width=3)

def add_remove(screen, data, mode, item):
    p=[[data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005],
       [data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.045],
       [data.WIDTH*0.45 + data.HEIGHT*0.1, data.HEIGHT*0.045],
       [data.WIDTH*0.45 + data.HEIGHT*0.1, data.HEIGHT*0.005]]
    if mode == 1:
        pygame.draw.circle(screen, color=BLUE_OFF, center=(data.WIDTH*0.45, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.rect(screen, color=GRAY_OFF, rect=pygame.Rect(data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005, data.HEIGHT*0.06, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=BLACK[0], closed=True, points=p, width=2)
    elif mode > 1:
        pygame.draw.circle(screen, color=LIGHT_BLUE, center=(data.WIDTH*0.45, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.rect(screen, color=LIGHT_GRAY, rect=pygame.Rect(data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005, data.HEIGHT*0.06, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=BLACK[0], closed=True, points=p, width=2)
        pygame.draw.rect(screen,color=VERY_LIGHT_GRAY, rect=pygame.Rect(data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.005, data.HEIGHT*0.03, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=BLACK[0], closed=True, points=[[data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.005], [data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.045], [data.WIDTH*0.45 + data.HEIGHT*0.14, data.HEIGHT*0.045], [data.WIDTH*0.45 + data.HEIGHT*0.14, data.HEIGHT*0.005]], width=2)
        pygame.draw.rect(screen, color=WHITE[0], rect=pygame.Rect(data.WIDTH*0.45-data.HEIGHT*0.015, data.HEIGHT*0.0225, data.HEIGHT*0.03, data.HEIGHT*0.005))
        pygame.draw.polygon(screen, color=BLACK[0], points=[[data.WIDTH*0.45 + data.HEIGHT*0.115, data.HEIGHT*0.02], [data.WIDTH*0.45 + data.HEIGHT*0.135, data.HEIGHT*0.02], [data.WIDTH*0.45 + data.HEIGHT*0.125, data.HEIGHT*0.01]])
        pygame.draw.polygon(screen, color=BLACK[0], points=[[data.WIDTH*0.45 + data.HEIGHT*0.115, data.HEIGHT*0.03], [data.WIDTH*0.45 + data.HEIGHT*0.135, data.HEIGHT*0.03], [data.WIDTH*0.45 + data.HEIGHT*0.125, data.HEIGHT*0.04]])
        if mode == 3:  # mode ajout
            pygame.draw.rect(screen, color=WHITE[0], rect=pygame.Rect(data.WIDTH*0.45-data.HEIGHT*0.0025, data.HEIGHT*0.01, data.HEIGHT*0.005, data.HEIGHT*0.03))
        else:  # mode suppression
            pygame.draw.circle(screen, color=LIGHT_RED, center=(data.WIDTH*0.45 - data.HEIGHT*0.04, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.015)
            pygame.draw.rect(screen, color=WHITE[0], rect=pygame.Rect(data.WIDTH*0.45-data.HEIGHT*0.051, data.HEIGHT*0.0225, data.HEIGHT*0.02, data.HEIGHT*0.005))
        if item:  # segment
            pygame.draw.line(screen, color=BLACK[0], start_pos=[data.WIDTH*0.45 + data.HEIGHT*0.05, data.HEIGHT*0.025], end_pos=[data.WIDTH*0.45 + data.HEIGHT*0.09, data.HEIGHT*0.025], width=3)
        else:  # point
            pygame.draw.circle(screen, color=BLACK[0], center=(data.WIDTH*0.45 + data.HEIGHT*0.07, data.HEIGHT*0.025), radius=data.HEIGHT*0.015)
    elif mode == 0:
        pygame.draw.circle(screen, color=BLUE_OFF, center=(
            data.WIDTH*0.45, data.HEIGHT*0.05/2), radius=data.HEIGHT*0.02)
        pygame.draw.rect(screen, color=LIGHT_GRAY, rect=pygame.Rect(
            data.WIDTH*0.45 + data.HEIGHT*0.04, data.HEIGHT*0.005, data.HEIGHT*0.06, data.HEIGHT*0.04))
        pygame.draw.lines(
            screen, color=BLACK[0], closed=True, points=p, width=2)
        pygame.draw.rect(screen, color=VERY_LIGHT_GRAY, rect=pygame.Rect(
            data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.005, data.HEIGHT*0.03, data.HEIGHT*0.04))
        pygame.draw.lines(screen, color=BLACK[0], closed=True, points=[[data.WIDTH*0.45 + data.HEIGHT*0.11, data.HEIGHT*0.005], [data.WIDTH*0.45 + data.HEIGHT *
                          0.11, data.HEIGHT*0.045], [data.WIDTH*0.45 + data.HEIGHT*0.14, data.HEIGHT*0.045], [data.WIDTH*0.45 + data.HEIGHT*0.14, data.HEIGHT*0.005]], width=2)
        pygame.draw.polygon(screen, color=BLACK[0], points=[[data.WIDTH*0.45 + data.HEIGHT*0.115, data.HEIGHT*0.02], [
                            data.WIDTH*0.45 + data.HEIGHT*0.135, data.HEIGHT*0.02], [data.WIDTH*0.45 + data.HEIGHT*0.125, data.HEIGHT*0.01]])
        pygame.draw.polygon(screen, color=BLACK[0], points=[[data.WIDTH*0.45 + data.HEIGHT*0.115, data.HEIGHT*0.03], [
                            data.WIDTH*0.45 + data.HEIGHT*0.135, data.HEIGHT*0.03], [data.WIDTH*0.45 + data.HEIGHT*0.125, data.HEIGHT*0.04]])
        if item:
            pygame.draw.circle(screen, color=BLACK[0], center=(
                data.WIDTH*0.45 + data.HEIGHT*0.07, data.HEIGHT*0.025), radius=data.HEIGHT*0.01)
        else:  # point
            pygame.draw.circle(screen, color=RED, center=(
                data.WIDTH*0.45 + data.HEIGHT*0.07, data.HEIGHT*0.025), radius=data.HEIGHT*0.01)


def update(screen, data, mode, item, seg_proche):
    # Screen
    screen.fill(WHITE[data.day])
    # Polyline
    draw_poly(screen, data, item, seg_proche)
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
    reset_button(screen, data)
    # Nodes
    for key in data.handles:
        pygame.draw.circle(screen, color=RED, center=data.points[key], radius=max(
            min(4, min(data.WIDTH, data.HEIGHT) * 0.009), 1.75))
    for key in data.fixes:
        pygame.draw.circle(screen, color=BLACK[data.day], center=data.points[key], radius=max(
            min(4, min(data.WIDTH, data.HEIGHT) * 0.009), 1.75))
