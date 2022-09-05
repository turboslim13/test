import sys
import math
import pygame

R = 4
r = 2

def calculate():
    global point, belong
    uinput = input("Координаты точки (q - чтобы выйти) -- ")
    if uinput == "q":
        pygame.quit()
        sys.exit()
        return

    point = list(map(float, uinput.split()))
    length = math.sqrt(point[0]**2 + point[1]**2)
    
    if length <= R:
        if length <= r or (-2 <= point[0] <= 2 and 0 <= point[1] <= -2) \
             or (point[1] <= -2 and (( point[0] >= -2 and point[1] >= 0.5 * point[0] -2) \
             or (point[0] <= 2 and point[1] >= -0.5 * point[0] - 2))):
                 belong = False
        else:
            belong = True

    else:
        belong = False

def get_rl_pos(x, y, correct_value=(0, 0)):
    return int(origin[0] + x * unit + correct_value[0]), int(origin[1] - y * unit + correct_value[1])

def get_rl_size(value):
    return value * unit

def display():
    screen.fill(bg_color)

    pygame.draw.circle(screen, (60, 60, 60), (origin[0], origin[1]), get_rl_size(4))
    pygame.draw.circle(screen, bg_color, (origin[0], origin[1]), get_rl_size(2))

    pygame.draw.rect(screen, bg_color, (get_rl_pos(-2, 0), (get_rl_size(R), get_rl_size(r))))
    pygame.draw.polygon(screen, bg_color, ((get_rl_pos(-2, -2)), get_rl_pos(-2, -3), get_rl_pos(0, -2)))
    pygame.draw.polygon(screen, bg_color, ((get_rl_pos(0, -2)), get_rl_pos(2, -2, (-1, 0)), get_rl_pos(2, -3, (-1, 0))))
    # Оси
    pygame.draw.line(screen, line_color, (0, origin[1]), (width, origin[1]))
    pygame.draw.line(screen, line_color, (origin[0], 0), (origin[0], height))
    # Начало координат
    pygame.draw.circle(screen, (180, 180, 180), (origin[0], origin[1]), 3)

    pygame.display.update()

pygame.init()

window_size = width, height = 600, 600
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

unit = 50
line_color = (100, 100, 100)
point_colors = ((255, 99, 71), (0, 179, 0)) 
bg_color = (40, 40, 40)
origin = width / 2, height / 2

display()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    calculate()

    screen.fill(bg_color)

    pygame.draw.circle(screen, (60, 60, 60), (origin[0], origin[1]), get_rl_size(4))
    pygame.draw.circle(screen, bg_color, (origin[0], origin[1]), get_rl_size(2))

    pygame.draw.rect(screen, bg_color, (get_rl_pos(-2, 0), (get_rl_size(R), get_rl_size(r))))
    pygame.draw.polygon(screen, bg_color, ((get_rl_pos(-2, -2)), get_rl_pos(-2, -3), get_rl_pos(0, -2)))
    pygame.draw.polygon(screen, bg_color, ((get_rl_pos(0, -2)), get_rl_pos(2, -2, (-1, 0)), get_rl_pos(2, -3, (-1, 0))))
    # оси
    pygame.draw.line(screen, line_color, (0, origin[1]), (width, origin[1]))
    pygame.draw.line(screen, line_color, (origin[0], 0), (origin[0], height))
    # начало координат
    pygame.draw.circle(screen, (180, 180, 180), (origin[0], origin[1]), 3)

    pygame.draw.circle(screen, (point_colors[1] if belong else point_colors[0]), get_rl_pos(point[0], point[1]), 3)
    
    pygame.display.update()
    clock.tick(10)
