import pygame
import random
import numpy as np

GREEN = (0, 170, 0)
RED = (255, 0, 0)

class blob:
    def __init__(self,x=None,y=None,is_predator=False):
        if x is None:   self.x = random.randint(300,500)
        else:           self.x = x
        if y is None:   self.y = random.randint(200,400)
        else:           self.y = y
        self.is_predator = is_predator
        self.size = 10
        self.color = RED if is_predator else GREEN
        self.speed = 1
        self.direction = 0
        self.iteration = 0

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

    def move(self,method = "random"):
        if not self.is_predator:    method = "random"
        if self.is_predator:        method = "predator"
        self.iteration += 1
        if method == "random":
            self.x += self.speed * np.cos(self.direction)
            self.y += self.speed * np.sin(self.direction)
            if self.iteration == 100:
                self.direction = random.randint(0,360)
                self.iteration -= 100
        if method == "predator":
            pass
