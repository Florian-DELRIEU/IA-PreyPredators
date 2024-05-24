import pygame
import random
import math
import numpy as np
from pygame_init import width,height,RED,GREEN,FPS,window,BLACK

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
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)
        if self.is_predator: self.draw_rays(window)

    def move(self,method = "random"):
        if not self.is_predator:    method = "random"
        if self.is_predator:        method = "predator"
        self.iteration += 1
        #self.keep_in_screen()
        if method == "random":
            self.x += self.speed * np.cos(self.direction)
            self.y += self.speed * np.sin(self.direction)
            if self.iteration == 100:
                self.direction = random.randint(0,360)
                self.iteration -= 100
        if method == "predator":
            pass

    def draw_rays(self, window, ray_length=100, num_rays=8):
        angle_step = 360 / num_rays
        for i in range(num_rays):
            angle = math.radians(i * angle_step)
            end_x = self.x + ray_length * math.cos(angle)
            end_y = self.y + ray_length * math.sin(angle)
            pygame.draw.line(window, BLACK, (self.x, self.y), (end_x, end_y),width=1)

    def keep_in_screen(self):
        # todo fix this
        # Assurer que les blobs restent dans la fenêtre
        self.x = max(0, min(self.x, width - self.size))
        self.y = max(0, min(self.y, height() - self.size))