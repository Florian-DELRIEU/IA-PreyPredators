import pygame

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
width, height = 800*1, 600*1
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation Proie-Prédateur")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Others
FPS = 60