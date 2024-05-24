import pygame
import time
from pygame_init import window,WHITE,FPS
from classes import blob

# Blobs
Preys = [blob(None,None,False) for _ in range (3)]
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
    time.sleep(1/FPS)
    for blob in Preys + Predators:
        blob.draw(window)
        blob.move()


    pygame.display.update()

# Quitter Pygame
pygame.quit()
