import pygame
import random
import numpy as np
from pygame_init import width,height,RED,GREEN,FPS

class blob:
    def __init__(self,x=None,y=None,is_predator=False):
        if x is None:   self.x = random.randint(0,width)
        else:           self.x = x
        if y is None:   self.y = random.randint(0,height)
        else:           self.y = y
        self.is_predator = is_predator
        self.size = 10
        self.color = RED if is_predator else GREEN
        self.speed = 1 * 60/FPS # Pour rester constant selon les FPS
        self.direction = random.randint(0,360)
        self.iteration = 0

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

    def move(self,method = "random"):
        if not self.is_predator:    method = "random"
        if self.is_predator:        method = "predator"
        self.iteration += 1
        self.keep_in_screen()
        if method == "random":
            self.x += self.speed * np.cos(self.direction)
            self.y += self.speed * np.sin(self.direction)
            if self.iteration == 100:
                self.direction = random.randint(0,360)
                self.iteration -= 100
        if method == "predator":
            pass

    def keep_in_screen(self):
        if self.x < 0: self.x = width
        if self.y < 0: self.x = height
        if self.x > width: self.x = 0
        if self.y > height: self.y = 0