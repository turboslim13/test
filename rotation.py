import sys
import math
import pygame

pygame.init()
SIZE = WIDTH, HEIGHT = (700, 700)
SCREEN_CENTER = pygame.math.Vector2(SIZE[0] / 2, SIZE[1] / 2)
SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()

GREY = (70, 70, 70)
WHITE = (155, 155, 155)
inter_color = (92, 214, 92)


class Point:
    def __init__(self, plane, pos=(0, 0), scale=0, rotation=0, color=WHITE):
        self.plane = plane
        self.measure = Measure(pos, scale, rotation)
        self.render_pos = self.plane.get_glob(self.measure.pos)
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.render_pos, 10)

    def info(self):
        print("-- Point -- ")
        print(f"Position -- {self.measure.pos}")
        print(f"Render position -- {self.render_pos}")
        print(f"Color -- {self.color}")

    def rel_set_pos(self, pos):
        self.render_pos = pos
        self.measure.pos = self.plane.get_local(pos)

    def rotate(self, deg):
        self.measure.rotate(deg)
        self.render_pos = self.plane.get_glob(self.measure.pos)
        # self.info()


class AABB(Point):
    def __init__(self, plane, pos=(0, 0), scale=(40, 40), rotation=0, centered=True):
        super().__init__(plane, pos)
        if centered:
            offsetx = scale[0] / 2
            offsety = scale[1] / 2

            self.vertices = [
                Point(plane, (offsetx, offsety)),
                Point(plane, (offsetx, -offsety)),
                Point(plane, (-offsetx, offsety)),
                Point(plane, (-offsetx, -offsety)),
            ]
        else:
            self.vertices = [
                Point(plane, (0, 0)),
                Point(plane, (scale[0], 0)),
                Point(plane, (scale[0], scale[1])),
                Point(plane, (0, scale[1])),
            ]

    def rotate(self, deg):
        for vert in self.vertices:
            vert.rotate(screen)


    def draw(self, screen):
        for vert in self.vertices:
            vert.draw(screen)


class CoordPlane:
    def __init__(self, origin=SCREEN_CENTER, unit=1):
        self.origin = origin
        self.unit = unit
        self.objs = []

        self.line_connection = []

        # colors
        self.line_width = 3
        self.line_color = GREY

    def draw(self, screen):
        pygame.draw.line(SCREEN, self.line_color, (self.origin.x, 0), (self.origin.x, HEIGHT), self.line_width)
        pygame.draw.line(SCREEN, self.line_color, (0, self.origin.y), (WIDTH, self.origin.y), self.line_width)
        pygame.draw.circle(SCREEN, WHITE, self.origin, 4)

        for obj in self.objs:
            obj.draw(screen)

        for i in range(len(self.line_connection)):
            pygame.draw.line(SCREEN, self.line_color, self.line_connection[i][0].render_pos, self.line_connection[i][1].render_pos)


    def get_glob(self, pos):
        vec = pygame.math.Vector2(pos)
        if vec.y != 0:
            vec.y = -vec.y
        return self.origin + vec

    def get_local(self, pos):
        vec = pos - self.origin
        if vec.y != 0:
            vec.y = -vec.y
        return vec

    def add(self, obj):
        self.objs.append(obj)

    def info(self):
        print("-------------------------------------")
        for obj in self.objs:
            obj.info()
            print("-------------------------------------")

    def create_connection(self):
        self.line_connection = [
            [self.objs[0], self.objs[1]],
            [self.objs[1], self.objs[2]],
            [self.objs[2], self.objs[3]],
            [self.objs[3], self.objs[0]],

            [self.objs[4], self.objs[5]],
            [self.objs[5], self.objs[6]],
            [self.objs[6], self.objs[7]],
            [self.objs[7], self.objs[4]],
        ]
            
class Measure:
    def __init__(self, pos, scale, rotation):
        self.pos = pygame.math.Vector2(pos) 
        self.scale = scale
        self.rotation = rotation

    def rotate(self, deg):
        rad = math.radians(deg)
        rotated = pygame.math.Vector2()
        rotated.x = self.pos.x * math.cos(rad) - self.pos.y * math.sin(rad)
        rotated.y = self.pos.x * math.sin(rad) + self.pos.y * math.cos(rad)
        self.pos = rotated


plane = CoordPlane()
rect_width = 200
rect_height = 200
plane.add(Point(plane, (-rect_width / 2, rect_height / 2)))
plane.add(Point(plane, (rect_width / 2, rect_height / 2)))
plane.add(Point(plane, (rect_width / 2, -rect_height / 2)))
plane.add(Point(plane, (-rect_width / 2, -rect_height / 2)))

scale_x, scale_y = 2, 2 
plane.add(Point(plane, (0, rect_height / 2 * scale_y)))
plane.add(Point(plane, (rect_width / 2 * scale_x , 0)))
plane.add(Point(plane, (0, -rect_height / 2 * scale_y)))
plane.add(Point(plane, (-rect_width / 2 * scale_x, 0)))
plane.create_connection()

circle_rad = rect_width / 2
circle_rad1 = math.sqrt(circle_rad**2 + circle_rad**2)

play = False

while True:
    mpos = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                plane.objs[0].rel_set_pos(mpos)
                plane.info()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                play = not play

    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_q]:
        for obj in plane.objs:
            obj.rotate(5)
    elif key_pressed[pygame.K_e]:
        for obj in plane.objs:
            obj.rotate(-5)

    if play:
        plane.objs[0].rotate(1.5)
        plane.objs[1].rotate(1.5)
        plane.objs[2].rotate(1.5)
        plane.objs[3].rotate(1.5)

        plane.objs[4].rotate(2)
        plane.objs[5].rotate(2.5)
        plane.objs[6].rotate(3)
        plane.objs[7].rotate(3.5)
        '''
        plane.objs[4].rotate(1)
        plane.objs[5].rotate(1.5)
        plane.objs[6].rotate(2)
        plane.objs[7].rotate(2.5)
        '''
    # Draw
    SCREEN.fill((0, 0, 0))
    pygame.draw.circle(SCREEN, plane.line_color, plane.origin, rect_width, 1)
    pygame.draw.circle(SCREEN, (170, 128, 128), plane.origin, circle_rad1, 1)
    plane.draw(SCREEN)

    pygame.display.update()

    CLOCK.tick(60)









