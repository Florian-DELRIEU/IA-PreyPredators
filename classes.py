"""
Module contenant les classes pour la simulation Proies-Prédateurs.

Ce module contient les classes nécessaires pour créer et gérer les blobs proies et prédateurs dans la simulation.

Classes:
    blob: Classe représentant un blob dans la simulation.
    Preys: Classe représentant un groupe de blobs proies.
    Predators: Classe représentant un groupe de blobs prédateurs.
"""
import random
import math
import numpy as np
from pygame_init import *

Preys = []
Predators = []

Predator_rays = [0] + [10,30,45,90,135] + [-10,-30,-45,-90,-135]
Preys_rays =    [0,180] + [30,60,90,120,150] + [-30,-60,-90,-120,-150]

class blob:
    def __init__(self,x=None,y=None,direction=None,is_predator=False,speed=1,detect_range=100,color=RED):
        self.x = random.randint(0,width) if x is None else x
        self.y = random.randint(0,height) if y is None else y
        if direction is None:   self.direction = np.radians(random.randint(0,360))
        else:           self.direction = np.radians(direction)
        self.is_predator = is_predator
        self.size = 10
        self.color = color
        self.speed = speed * 60/FPS # Pour rester constant selon les FPS
        self.iteration = 0
        self.rays = []
        self.rays_angles = []
        self.detect_range = detect_range
        self.target = None
        self.generation = 0
        self.energy = 50 if self.is_predator else 10
        if self.is_predator : Predators.append(self)
        if not self.is_predator : Preys.append(self)
        self.split_cost = 100

    def draw(self, window):
        """
        Dessine les blobs et leurs attribut en fonctions de son type
        :param window: Fenêtre dans laquelle le blob sera déssiné
        """
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)
        #if self.is_predator: self.draw_rays(window)

    def draw_rays(self, window):
        """
        Dessine les rayons des blobs. Cette fonction est dissocié de la fonction :draw: pour pouvoir choisir de
        dessiner les rayons ou pas
        :param window:
        :return:
        """
        for end_x,end_y in self.rays:
            pygame.draw.line(window, WHITE, (self.x, self.y), (end_x, end_y),width=1)

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
        self.keep_in_screen(width,height)
        loop_iteration = random.randint(50,100)
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

    def gain_energy(self,ammont):
        self.energy += ammont
        if self.energy <= 0: self.die()
        if self.energy >= 1.5*self.split_cost: self.split()

    def energy_turn(self):
        ammont = 0
        ammont -= 0.05 * (self.speed / 1) ** 3
        ammont -= 0.01 * (self.detect_range/100) ** 2
        if not self.is_predator: ammont += 0.1
        self.gain_energy(ammont)

    def die(self):
        self.energy=0
        if self in Predators    : Predators.__delitem__(Predators.index(self))
        if self in Preys        : Preys.__delitem__(Preys.index(self))

    def split(self):
        speed = float(self.speed + np.array(random.choices([-0.1,0,+0.1],[1,2,1])))
        detect_range = float(self.detect_range + np.array(random.choices([-10,0,+10],[1,2,1])))
        new_blob = blob(self.x,self.y,None,self.is_predator,color=self.color,speed=speed,detect_range=detect_range)
        new_blob.generation = self.generation + 1
        self.energy -= self.split_cost

    def bite(self,target):
        target.die()
        self.energy += 100
        self.target = None

    def create_rays(self):
        """
        Définie, sans les tracer, les rayons de détections des blobs et stock les extrémités dans :self.rays:
        :return:
        """
        self.rays = []
        self.rays_angles = self.direction + np.radians(np.array(
            Predator_rays if self.is_predator else Preys_rays
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
                        break
        self.target = closest_prey
        # Changement de couleur si proie detecté
        self.color = RED if self.target is None else BLACK

    def keep_in_screen(self, width, height):
        # Vérifier et ajuster les coordonnées du blob pour qu'il reste à l'intérieur de la fenêtre
        if self.x < 0:
            self.x = 0
        elif self.x > width:
            self.x = width
        if self.y < 0:
            self.y = 0
        elif self.y > height:
            self.y = height

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