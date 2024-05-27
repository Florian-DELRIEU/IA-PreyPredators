import pygame
import time
from pygame_init import *
from classes import blob,Preys,Predators

# Blobs
for _ in range (1): blob(None,None,None,False)
for _ in range (0): blob(None,None,None,True)

# Boucle principale
running = True
frame = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Dessiner la fenêtre
    window.fill(WHITE)

    # move all blobs
    time.sleep(1/FPS)

    # Calcul du temps de simulation
    frame += 1
    minutes = frame // 60
    seconds = frame % 60
    time_string = f"Temps: {minutes:02}:{seconds:02}"

    # Dessiner le temps de simulation en haut à droite
    text_surface = font.render(time_string, True, BLACK)
    window.blit(text_surface, (width - text_surface.get_width() - 10, 10))

    for blob in Predators + Preys:
        if blob in Predators : blob.detect(Preys)
        blob.move()
        blob.draw(window)
        if blob.energy <= 0: blob.die()
    pygame.display.update()

# Quitter Pygame
pygame.quit()
