import pygame
import random
import numpy as np

GREEN = (0, 170, 0)
RED = (255, 0, 0)

class blob:
    def __init__(self,x,y,is_predator):
        self.x = x
        self.y = y
        self.is_predator = is_predator
        self.size = 10
        self.color = RED if is_predator else GREEN
        self.speed = 1
        self.direction = 0
        self.iteration = 0

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

    def move(self,method = "random"):
        self.iteration += 1
        if method == "random":
            self.x += self.speed * np.cos(self.direction)
            self.y += self.speed * np.sin(self.direction)
            if self.iteration == 100:
                self.direction = random.randint(0,360)
                self.iteration -= 100
