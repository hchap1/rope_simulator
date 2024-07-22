import pygame, math, random, copy
pygame.init()
screen = pygame.display.set_mode((1920, 1080), vsync=True)
font = pygame.font.Font("freesansbold.ttf", 25)
clock = pygame.time.Clock()
running = True

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Point:
    def __init__(self, position, locked):
        self.locked = locked
        self.position = position
        self.old_position = position

class Stick:
    def __init__(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b
        dx = point_a.position.x - point_b.position.x
        dy = point_a.position.y - point_b.position.y
        self.length = math.sqrt(dx*dx+dy*dy)
        
points = []
sticks = []
active = False

for i in range(len(points)-1):
    sticks.append(Stick(points[i], points[i+1]))

while running:
    dt = clock.tick(60)
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        mx,my = pygame.mouse.get_pos()
        to_remove = -1
        for i in range(len(sticks)):
            dlx = sticks[i].point_a.position.x - sticks[i].point_b.position.x
            dly = sticks[i].point_a.position.y - sticks[i].point_b.position.y
            dx = sticks[i].point_a.position.x - mx
            dy = sticks[i].point_a.position.y - my
            angle_stick = math.degrees(math.atan2(dly,dlx))
            angle_point = math.degrees(math.atan2(dy,dx))
            angle_delta = angle_stick - angle_point
            dist = math.sqrt(dx*dx+dy*dy)
            dist_from_line = math.sin(math.radians(angle_delta)) * dist
            if dist_from_line < 5:
                x1, y1 = sticks[i].point_a.position.x, sticks[i].point_a.position.y
                x2, y2 = sticks[i].point_b.position.x, sticks[i].point_b.position.y
                min_x = min(x1, x2)
                max_x = max(x1, x2)
                min_y = min(y1, y2)
                max_y = max(y1, y2)
                if min_x <= mx <= max_x and min_y <= my <= max_y:
                    sticks.pop(i)
                    break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                active = not active
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                points.append(Point(Vec2(mx,my), True))
                closest = -1
                dist = -1
                for i in range(len(points)-1):
                    dx = points[i].position.x-mx
                    dy = points[i].position.y-my
                    if dist == -1 or math.sqrt(dx*dx+dy*dy) < dist:
                        closest = i
                        dist = math.sqrt(dx*dx+dy*dy)
                if closest != -1:
                    sticks.append(Stick(points[-1], points[closest]))
            if event.button == 3:
                mx, my = pygame.mouse.get_pos()
                points.append(Point(Vec2(mx,my), False))
                dist = -1
                closest = -1
                for i in range(len(points)-1):
                    dx = points[i].position.x-mx
                    dy = points[i].position.y-my
                    if dist == -1 or math.sqrt(dx*dx+dy*dy) < dist:
                        closest = i
                        dist = math.sqrt(dx*dx+dy*dy)
                if closest != -1:
                    sticks.append(Stick(points[-1], points[closest]))
            if event.button == 2:
                mx, my = pygame.mouse.get_pos()
                points.append(Point(Vec2(mx,my), False))
                dist = -1
                dist2 = -1
                closest = -1
                closest2 = -1
                for i in range(len(points)-1):
                    dx = points[i].position.x-mx
                    dy = points[i].position.y-my
                    if dist == -1 or math.sqrt(dx*dx+dy*dy) < dist:
                        dist2 = dist
                        closest2 = closest
                        closest = i
                        dist = math.sqrt(dx*dx+dy*dy)
                    elif dist2 == -1 or math.sqrt(dx*dx+dy*dy) < dist2:
                        closest2 = i
                        dist2 = math.sqrt(dx*dx+dy*dy)
                if closest != -1:
                    sticks.append(Stick(points[-1], points[closest]))
                if closest2 != -1:
                    sticks.append(Stick(points[-1], points[closest2]))
                
    screen.fill((255, 255, 255))
    if active:
        random.shuffle(points)
        for p in points:
            if not p.locked:
                position_before_update = copy.deepcopy(p.position)
                dx = p.position.x - p.old_position.x
                dy = p.position.y - p.old_position.y
                p.position.x += dx
                p.position.y += dy
                p.position.y += dt 
                p.old_position = position_before_update 

        for i in range(5):
            for s in sticks:
                center = Vec2((s.point_a.position.x + s.point_b.position.x) / 2, (s.point_a.position.y + s.point_b.position.y) / 2)
                dx = s.point_a.position.x - s.point_b.position.x
                dy = s.point_a.position.y - s.point_b.position.y
                magnitude = math.sqrt(dx*dx+dy*dy)
                dir = Vec2(dx / magnitude, dy / magnitude)
                if not s.point_a.locked:
                    s.point_a.position = Vec2(center.x + dir.x * s.length * 0.5, center.y + dir.y * s.length * 0.5)
                if not s.point_b.locked:
                    s.point_b.position = Vec2(center.x - dir.x * s.length * 0.5, center.y - dir.y * s.length * 0.5)
    for s in sticks:
        a = s.point_a.position
        b = s.point_b.position
        pygame.draw.line(screen, (0, 0, 0), (a.x, a.y), (b.x, b.y), 10)
    for p in points:
        colour = (0,255,0)
        if p.locked: colour = (255,0,0)
        pygame.draw.circle(screen, colour, (p.position.x, p.position.y), 10)
    pygame.display.update()
pygame.quit()

