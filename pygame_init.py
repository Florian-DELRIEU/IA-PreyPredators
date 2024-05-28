"""
Module contenant les fonctions d'initialisation de Pygame.

Ce module contient les fonctions nécessaires pour initialiser Pygame et créer la fenêtre de la simulation.

Fonctions:
    None

Classes:
    None
"""


import pygame

# Initialisation de Pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial",12)

# Configuration de la fenêtre
width, height = 1200*1, 1000*1
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation Proie-Prédateur")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (50,50,50)

# Others
FPS = 60