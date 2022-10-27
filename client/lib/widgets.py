import pygame
from pygame.locals import *

green = pygame.Color(68,216,68)
white = pygame.Color(255,255,255)
yellow = pygame.Color(255,235,4)
red = pygame.Color(255,0,0)
orange = pygame.Color(255,127,0)

class Taskbar():
    def __init__(self, _fill=50, _idx=0, _x=0, _y=0):
        self.img = pygame.image.load(r'./data/images/buttons/taskbar.png')
        self.x = _x
        self.y = _y
        self.w = 860
        self.h = 75
        self.rect = pygame.Rect(_x, _y, self.w, self.h)

    def draw(self, surface):
        surface.blit(self.img,(self.x,self.y))

class Checkbox():
    def __init__(self, _checked=False, _label='', _x=0, _y=0):
        self.checked = _checked
        self.label = _label
        self.x = _x
        self.y = _y
        self.w = 40 
        self.h = 40
        self.rect = pygame.Rect(_x, _y, self.w, self.h)

    def draw(self, surface):
        _font = pygame.font.SysFont('Comic Sans MS', 26)
        if self.checked:
            self.img = pygame.image.load(r'./data/images/buttons/check.png')
            _desc = _font.render(self.label, False, green)

        else:
            self.img = pygame.image.load(r'./data/images/buttons/nocheck.png')
            _desc = _font.render(self.label, False, white)

        surface.blit(self.img,(self.x,self.y))
        surface.blit(_desc,(self.x + 30,self.y - 12))


class Button():
    def __init__(self, _img, _desc, _x, _y, _h, _w):
        self.img = pygame.image.load('.\\data\\button_icons\\' + _img + '.png')
        self.img_act = pygame.image.load('.\\data\\button_icons\\' + _img + '_act.png')
        self.desc = _desc
        self.active = False
        self.x = _x
        self.y = _y
        self.w = _w
        self.h = _h
        self.rect = pygame.Rect(_x, _y, self.w, self.h)

    def draw(self, surface):
        if(self.active):
            #print("button active")
            _img = self.img_act
        else:
            _img = self.img
        surface.blit(_img,(self.x,self.y))
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)
