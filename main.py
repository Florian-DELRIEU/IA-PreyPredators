import pygame
import time
from pygame_init import window,WHITE,FPS,BLACK,RED
from classes import blob,Preys,Predators

# Blobs
for _ in range (15): blob(None,None,None,False)
for _ in range (5): blob(None,None,None,True)

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
    for blob in Predators + Preys:
        if blob in Predators : blob.detect(Preys)
        blob.move()
        blob.draw(window)
        if blob.energy <= 0: blob.die()
    pygame.display.update()

# Quitter Pygame
pygame.quit()
