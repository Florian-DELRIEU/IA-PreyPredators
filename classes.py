import pygame
import random
import math
import numpy as np
from pygame_init import width,height,RED,GREEN,FPS,window,BLACK

class blob:
    def __init__(self,x=None,y=None,direction=None,is_predator=False):
        if x is None:   self.x = random.randint(0,width)
        else:           self.x = x
        if y is None:   self.y = random.randint(0,height)
        else:           self.y = y
        if direction is None:   self.direction = random.randint(0,360)
        else:           self.direction = direction
        self.is_predator = is_predator
        self.size = 10
        self.color = RED if is_predator else GREEN
        self.speed = 2 * 60/FPS # Pour rester constant selon les FPS
        self.iteration = 0
        self.rays = []
        self.detect_range = 100
        self.target = None
        self.create_rays()

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

    def create_rays(self):
        rays_angles = self.direction + np.array([0,45,90,180,270,315])
        for i in range(len(rays_angles)):
            current_angle = np.radians(rays_angles[i])
            end_x = self.x + self.detect_range * math.cos(current_angle)
            end_y = self.y + self.detect_range * math.sin(current_angle)
            self.rays.append((end_x, end_y))

    def draw_rays(self, window):
        for end_x,end_y in self.rays:
            pygame.draw.line(window, BLACK, (self.x, self.y), (end_x, end_y),width=1)

    def detect(self, preys):
        closest_prey = None
        min_distance = self.detect_range
        for prey in preys: # for each prey
            for end_x, end_y in self.rays: # for each rays
                if self.line_intersects_circle(self.x, self.y, end_x, end_y, prey.x, prey.y, prey.size):
                    distance = math.hypot(prey.x - self.x, prey.y - self.y)
                    if distance < min_distance:
                        min_distance = distance
                        closest_prey = prey
        return closest_prey

    def keep_in_screen(self):
        """ Assure que les blobs restent dans les limites de l'écran """
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.x = max(self.size, min(self.x, screen_width - self.size))
        self.y = max(self.size, min(self.y, screen_height - self.size))

    def line_intersects_circle(self, x1, y1, x2, y2, cx, cy, prey_radius):
        """
        Check if the line segment (x1, y1) to (x2, y2) intersects with the circle centered at (cx, cy) with radius
         - A: Centre du predateur
         - B: Extremité du rayon
         - C: Centre de la proie
         - H: Point sur le rayon le plus proche de C (entre A et B)
        """
        ac = [cx - x1, cy - y1] # Vecteur (predateur-Proie)
        ab = [x2 - x1, y2 - y1] # Vecteur (Rayon)
        norm_ab = ab[0] ** 2 + ab[1] ** 2
        scal_acab = ac[0] * ab[0] + ac[1] * ab[1]
        t = scal_acab / norm_ab

        if t < 0:   t = 0
        elif t > 1: t = 1

        ah = [ab[0] * t + x1, ab[1] * t + y1]
        HC = math.hypot(ah[0] - cx, ah[1] - cy)

        return HC <= prey_radius