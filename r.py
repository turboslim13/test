import math
import sys
import pygame
import time


class Slider:
    def __init__(self, start_pt, end_pt, t_value, set_func, whole_value):
        self.start_pt = pygame.Vector2(start_pt) 
        self.end_pt = pygame.Vector2(end_pt)
            
        self.start_pt_color = ( 100, 101, 140 )
        self.end_pt_color = (136, 136, 136)
        self.pt_radius = 7

        self.direction = self.end_pt - self.start_pt
        self.direction_color = (100, 100, 100)
        self.filled_line_color = self.start_pt_color

        self.t_value = t_value
        self.slide_pt = lerp(self.start_pt, self.end_pt, self.t_value)
        self.slide_pt_color = self.start_pt_color
        self.slide_pt_radius = 10

        self.set_func = set_func
        self.length_whole_value = len(whole_value)
        if self.length_whole_value == 1:
            self.whole_value = whole_value[0]
        elif self.length_whole_value == 2:
            self.whole_value = pygame.Vector2(whole_value)
        elif self.length_whole_value == 3:
            self.whole_value = pygame.Vector3(whole_value)

        self.collide_rect = pygame.Rect(self.start_pt.x - self.pt_radius, self.start_pt.y - self.slide_pt_radius,
                self.direction.x + 2 * self.pt_radius, 2 * self.slide_pt_radius)
        
        self.font = pygame.font.SysFont('Verdana', 25)
        self.t_value_text_color = (self.start_pt_color)
        self.t_value_text = self.font.render(f'T value {round(self.t_value, 3)}', 1, self.t_value_text_color)
        self.t_value_text_pos = self.start_pt + pygame.Vector2(-20, 15)

    def collide(self, pos):
        direction = pos - self.slide_pt
        if direction.x**2 + direction.y**2 <= self.slide_pt_radius**2:
            return True
        return False

    def change_value(self):
        value = 0
        if self.length_whole_value == 2:
            value = (self.whole_value[0] * self.t_value, self.whole_value[1] * self.t_value)
        elif self.length_whole_value == 3:
            vec = pygame.Vector3(255, 0, 0) + self.whole_value * self.t_value
            value = (vec[0], vec[1], vec[2])
        else:
            value = self.whole_value * self.t_value
        self.set_func(value)
    
    def draw(self, screen):
        pygame.draw.line(screen, self.direction_color, self.start_pt, self.end_pt, 5)  
        pygame.draw.line(screen, self.filled_line_color, self.start_pt, self.slide_pt, 5)  

        # border points
        pygame.draw.circle(screen, self.start_pt_color, self.start_pt, self.pt_radius)
        pygame.draw.circle(screen, self.end_pt_color, self.end_pt, self.pt_radius)
        
        # slide point
        pygame.draw.circle(screen, self.slide_pt_color, self.slide_pt, self.slide_pt_radius)

        #pygame.draw.rect(screen, (255, 0, 0), self.collide_rect, 1)

        screen.blit(self.t_value_text, self.t_value_text_pos)
    

def lerp(a:pygame.Vector2, b:pygame.Vector2, t:float):
    return a + (b - a) * t


def inverse_lerp(a:pygame.Vector2, b:pygame.Vector2, point:pygame.Vector2):
    return (point.x - a.x) / (b - a).x


pygame.init()
width, height = (800, 700)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

'''
pos_text = font.render(f'Pos {pos_lerp}', 1, (255, 255, 255))
'''

'''
mpos_text = font.render(f'MousePos {pygame.mouse.get_pos()}', 1, (255, 255, 255))
'''


def update():
    mpos = pygame.mouse.get_pos()
    
    if current > -1:
        slider = sliders[current]
        slider.slide_pt.x = mpos[0]
        if slider.slide_pt.x > slider.end_pt.x:
            slider.slide_pt.x = slider.end_pt.x
        elif slider.slide_pt.x < slider.start_pt.x:
            slider.slide_pt.x = slider.start_pt.x
       
        slider_slide_pt = slider.start_pt + slider.slide_pt
        slider.t_value = inverse_lerp(slider.start_pt, slider.end_pt, slider.slide_pt)
        slider.t_value_text = slider.font.render(f'T value {round(slider.t_value, 3)}', 1, slider.t_value_text_color)
        slider.change_value()

        '''
        pos_text = font.render(f'Pos {pos_lerp}', 1, (255, 255, 255))
        '''

    '''
    mpos_text = font.render(f'MousePos {mpos}', 1, (255, 255, 255))
    '''
        

def draw():
    # text
    '''
    screen.blit(pos_text, (100, height - 100))
    '''
    '''
    screen.blit(mpos_text, (400, height - 100))
    '''
    screen.fill((50, 50, 50))
    screen.blit(surf, (315, 70))

    for slider in sliders:
        slider.draw(screen)

    pygame.display.update()

surf = pygame.Surface((200, 200))
alpha_slider = Slider((145, 450), (645, 450), 0.5, surf.set_alpha, [255])
color_slider = Slider((145, 350), (645, 350), 0, surf.fill, [-255, 0, 255])

sliders = [alpha_slider, color_slider]
sliders_len = len(sliders)
for slider in sliders:
    slider.change_value()

current = -1
prev_mpos = pygame.mouse.get_pos()
current_mpos = prev_mpos

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(sliders_len):
                    if sliders[i].collide(event.pos) or sliders[i].collide_rect.collidepoint(event.pos):
                        current = i
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                current = -1
        
    update()
    draw()
    clock.tick(60)
