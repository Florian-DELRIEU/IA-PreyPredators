import pygame
import time
from pygame_init import window,WHITE,FPS,BLACK,RED
from classes import blob

# Blobs
Preys =     [blob(None,None,None,False) for _ in range (15)]
Predators = [blob(None,None,None,True) for _ in range (5)]

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
        blob.move()
        blob.draw(window)
        blob.gain_energy(0)
        if blob.energy <= 0: Preys.__delitem__(Preys.index(blob))
    for blob in Predators:
        blob.detect(Preys)
        blob.move()
        blob.draw(window)
        if blob.energy <= 0: Predators.__delitem__(Predators.index(blob))
    pygame.display.update()

# Quitter Pygame
pygame.quit()
