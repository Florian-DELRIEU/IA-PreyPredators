import pygame
import time
from pygame_init import window,WHITE,FPS,BLACK,RED
from classes import blob

# Blobs
Preys =     [blob(None,None,None,False) for _ in range (15)]
Predators = [blob(None,None,None,True) for _ in range (1)]

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
    for blob in Preys:
        blob.draw(window)
        blob.move()
    for blob in Predators:
        blob.target = None
        blob.target = blob.detect(Preys)
        blob.move()
        blob.draw(window)
        if blob.target is not None: blob.color = BLACK
        if blob.target is None:     blob.color = RED
    pygame.display.update()

# Quitter Pygame
pygame.quit()
