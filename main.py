import pygame, math, random, cop
from vector import Vector
import pygame, random, copy

class Node:
    def __init__(self, pos, locked):
        self.pos = pos
        self.last_pos = pos
        self.locked = locked

class Stick:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.length = a.pos.distance_to(b.pos)

sticks = []
nodes = []

def physics(dt):
    for node in nodes:
        if not node.locked:
            old_pos = copy.deepcopy(node.pos)
            delta_pos = node.pos.subtract(node.last_pos).add(Vector(0, dt*dt*0.05))
            node.pos.add_ip(delta_pos)
            node.last_pos = old_pos
    for i in range(5):
        for stick in sticks:
            midpoint = stick.a.pos.add(stick.b.pos).divide(2)
            normal = stick.a.pos.subtract(stick.b.pos).normalize()
            if not stick.a.locked:
                stick.a.pos = midpoint.add(normal.multiply(stick.length * 0.5))
            if not stick.b.locked:
                stick.b.pos = midpoint.subtract(normal.multiply(stick.length * 0.5))

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
running = True
simulating = False

while running:
    dt = clock.tick(60)
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                simulating = not simulating
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 or event.button == 3:
                m = Vector.component_from_tuple(pygame.mouse.get_pos())
                place_new = True
                for node in nodes:
                    dist = m.distance_to(node.pos)
                    if dist < 10:
                        place_new = False
                        node.locked = not node.locked
                if place_new:
                    new_node = Node(m, event.button == 3)
                    closest_idx = -1
                    closest_idx2 = -1
                    distance = -1
                    distance2 = -1
                    for n in range(len(nodes)):
                        dist = nodes[n].pos.distance_to(new_node.pos)
                        if dist < distance or distance == -1:
                            distance2 = distance
                            closest_idx2 = closest_idx
                            distance = dist
                            closest_idx = n
                        elif dist < distance2 or distance2 == -1:
                            distance = dist
                            closest_idx2 = n
                    nodes.append(new_node)
                    if closest_idx != -1:
                        sticks.append(Stick(nodes[closest_idx], nodes[-1])) 
                    if closest_idx2 != -1 and pygame.key.get_pressed()[pygame.K_SPACE]:
                        sticks.append(Stick(nodes[closest_idx2], nodes[-1]))
    if simulating:
        physics(dt)
    for stick in sticks:
        pygame.draw.line(screen, (0,0,0), stick.a.pos.get_position(), stick.b.pos.get_position(), 5)
    for node in nodes:
        colour = [0,255,0]
        if node.locked: colour = [255,0,0]
        pygame.draw.circle(screen, colour, node.pos.get_position(), 10) 

    pygame.display.update()
pygame.quit()

