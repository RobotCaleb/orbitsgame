from pygame import Surface
from common import Vec2, ColorValue, FRAME_TIME
import pygame
import math

class Body():
    def __init__(self, mass: float, pos: Vec2, color: ColorValue):
        self.mass = mass
        self.pos = pos
        self.vel = Vec2(0, 0)
        self.color = color
        self.path = []

    def draw(self, screen: Surface):
        if len(self.path) > 1:
            for i in range(0, len(self.path) - 1):
                pygame.draw.line(screen, self.color, self.path[i], self.path[i+1])
        pygame.draw.circle(screen, self.color, self.pos, math.sqrt(self.mass*0.001))

    def update(self):
        self.pos += self.vel * FRAME_TIME
        self.path.append(Vec2(self.pos))
        if len(self.path) > 100:
            self.path.pop(0)
