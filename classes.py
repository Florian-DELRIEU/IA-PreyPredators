import pygame
import random
import math
import numpy as np
from pygame_init import width,height,RED,GREEN,FPS,window,BLACK,GREY

Preys = []
Predators = []

class blob:
    def __init__(self,x=None,y=None,direction=None,is_predator=False):
        if x is None:   self.x = random.randint(0,width)
        else:           self.x = x
        if y is None:   self.y = random.randint(0,height)
        else:           self.y = y
        if direction is None:   self.direction = np.radians(random.randint(0,360))
        else:           self.direction = np.radians(direction)
        self.is_predator = is_predator
        self.size = 10
        self.color = RED if is_predator else GREEN
        self.speed = 2 * 60/FPS # Pour rester constant selon les FPS
        self.iteration = 0
        self.rays = []
        self.rays_angles = []
        self.detect_range = 100
        self.target = None
        self.energy = 100
        if self.is_predator : Predators.append(self)
        if not self.is_predator : Preys.append(self)

    def draw(self, window):
        """
        Dessine les blobs et leurs attribut en fonctions de son type
        :param window: Fenêtre dans laquelle le blob sera déssiné
        """
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)
        if self.is_predator: self.draw_rays(window)

    def draw_rays(self, window):
        """
        Dessine les rayons des blobs. Cette fonction est dissocié de la fonction :draw: pour pouvoir choisir de
        dessiner les rayons ou pas
        :param window:
        :return:
        """
        for end_x,end_y in self.rays:
            pygame.draw.line(window, GREY, (self.x, self.y), (end_x, end_y),width=1)

    def move(self,method = "random"):
        """
        Execute une itération de mouvement pour le blob.
        :param method: Méthode de déplacement
                - "random": Marche aléatoire (actuellement pour les proies)
                - "predator": ---pas encore implémenté---
        :return:
        """
        if not self.is_predator or self.target is None:
            method = "random"
        elif self.is_predator:
            method = "predator"
        self.iteration += 1
        #self.keep_in_screen()
        loop_iteration = random.randint(0,10)
        if method == "random":
            self.x += self.speed * np.cos(self.direction)
            self.y += self.speed * np.sin(self.direction)
            if self.iteration >= loop_iteration:
                self.direction = np.radians(random.randint(0,360))
                self.iteration -= loop_iteration
        if method == "predator":
            self.iteration = 0
            self.x += self.speed * np.cos(self.direction)
            self.y += self.speed * np.sin(self.direction)
        if self.is_predator : self.gain_energy(-0.1)
        if not self.is_predator : self.gain_energy(1)

    def gain_energy(self,ammont):
        self.energy += ammont
        if self.energy <= 0: self.die()
        if self.energy >= 1000: self.split()


    def die(self):
        if self in Predators    : Predators.__delitem__(Predators.index(self))
        if self in Preys        : Preys.__delitem__(Preys.index(self))

    def split(self):
        blob(self.x,self.y,None,self.is_predator)
        self.energy -= 500

    def bite(self,target):
        target.energy -= 10000
        self.energy += 500

    def create_rays(self):
        """
        Définie, sans les tracer, les rayons de détections des blobs et stock les extrémités dans :self.rays:
        :return:
        """
        self.rays = []
        self.rays_angles = self.direction + np.radians(np.array(
            [0] + [10,30,45,90,135] + [-10,-30,-45,-90,-135]
        ))
        for i in range(len(self.rays_angles)):
            current_angle = self.rays_angles[i]
            end_x = self.x + self.detect_range * math.cos(current_angle)
            end_y = self.y + self.detect_range * math.sin(current_angle)
            self.rays.append((end_x, end_y))

    def detect(self, preys):
        """
        Vérifie si l'un des rayons détécte une proies. Si plusieurs proies sont détectés alors la prlus proche est
        sauvegardé
        :param preys: Listes des proies pouvant être détecté
        :return: Proie la plus proche
        """
        # Initialisation
        self.create_rays()
        self.target = None
        closest_prey = None
        min_distance = self.detect_range
        # Boucle de détection
        for prey in preys:
            for i in range(len(self.rays)):
                end_x,end_y = self.rays[i]
                # Vérifie si une proie est détectée
                if self.line_intersects_circle(self.x, self.y, end_x, end_y, prey.x, prey.y, prey.size):
                    distance = math.hypot(prey.x - self.x, prey.y - self.y)
                    # Vérifie si la proie en cours est plus proche qu'une autre
                    if distance < min_distance:
                        min_distance = distance
                        closest_prey = prey
                        self.direction = self.rays_angles[i]
                    # Verifié si contact avec la proie
                    if distance <= self.size:
                        self.bite(prey)
        self.target = closest_prey
        # Changement de couleur si proie detecté
        if self.target is None: self.color = RED
        else:                   self.color = BLACK

    def keep_in_screen(self):
        """
        Assure que les blobs restent dans les limites de l'écran
        TODO Fix it
        """
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.x = max(self.size, min(self.x, screen_width - self.size))
        self.y = max(self.size, min(self.y, screen_height - self.size))

    def line_intersects_circle(self, x1, y1, x2, y2, cx, cy, prey_radius):
        """
        Vérifie si le segement (x1, y1) to (x2, y2) intersecte le cercle de centre (cx, cy) avec son rayon.
         - A: Centre du predateur
         - B: Extremité du rayon
         - C: Centre de la proie
         - H: Point sur le rayon le plus proche de C (toujours entre A et B)

         :return: True si il y a intersection sinon False
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