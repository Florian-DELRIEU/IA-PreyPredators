import pygame
from classes import blob

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

# Blobs
Preys = [blob(None,None,False) for _ in range (10)]
Predators = [blob(None,None,True) for _ in range (2)]

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Dessiner la fenêtre
    window.fill(WHITE)
    # move all blobs
    for blob in Preys + Predators:
        blob.draw(window)
        blob.move()
    pygame.display.update()

# Quitter Pygame
pygame.quit()
