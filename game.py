import pygame
import random

from pygame.time import Clock
from pygame import Surface
from typing import List
from common import Vec2, FRAME_RATE, FRAME_TIME, GRAVITY

from body import Body

pygame.init()

clock = Clock()

bodies: List[Body] = []

body = Body(20000000, Vec2(511, 383), (0, 255, 0))
bodies.append(body)


def apply_gravity() -> None:
    # m = mass
    # F = force
    # A = acceleration

    # F = G(m1*m2)/r^2
    # F = mA
    # A = F/m
    for i, b1 in enumerate(bodies):
        for j in range(i+1, len(bodies)):
            b2 = bodies[j]
            force = (GRAVITY * (b1.mass * b2.mass)) / b1.pos.distance_squared_to(b2.pos)
            b1.vel += force * FRAME_TIME / b1.mass * (b2.pos - b1.pos).normalize()
            b2.vel += force * FRAME_TIME / b2.mass * (b1.pos - b2.pos).normalize()


screen = pygame.display.set_mode((1024, 768))

running = True

mouse: Vec2 = Vec2(0)
was_held: bool = False
start_mouse: Vec2 = Vec2(0)

temp_body: Body = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse.get_pos()
    is_held = pygame.mouse.get_pressed()[0]

    if is_held and was_held:
        if temp_body is None:
            c = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            temp_body = Body(0, mouse, c)
            start_mouse = Vec2(mouse)
        else:
            temp_body.mass += 100
    elif was_held and not is_held:
        temp_body.vel = start_mouse - mouse
        bodies.append(temp_body)
        temp_body = None

    was_held = is_held

    screen.fill((0, 0, 0))

    # update the world
    apply_gravity()
    [body.update() for body in bodies]

    # draw the world
    [body.draw(screen) for body in bodies]
    if temp_body is not None:
        temp_body.draw(screen)

    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.quit()
