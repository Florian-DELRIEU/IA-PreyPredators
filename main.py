import pygame
import time
import math
from pygame_init import *
from classes import blob,Preys,Predators

# Blobs
for _ in range (15): blob(None,None,None,False,color=GREEN)
for _ in range (1): blob(None,None,None,True,color=RED,speed=1.2)

selected_blob = None
# Boucle principale
running = True
frame = 0
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for blob in Preys + Predators:
                if math.hypot(blob.x - mouse_x, blob.y - mouse_y) <= blob.size:
                    selected_blob = blob
                    break
                else:
                    selected_blob = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
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

    # Affiche les information d'un blob si selectionné
    if selected_blob:
        info_text = (f"""Type: {'Prédateur' if selected_blob.is_predator else 'Proie'} \n
                     Energie: {selected_blob.energy:.2f} \n
                     Cible: {"False" if selected_blob.target is None else "True"}""")
        selected_blob.draw_rays(window)
        info_surface = font.render(info_text, True, BLACK)
        window.blit(info_surface, (10, 10))

    if not paused:
        for blob in Predators + Preys:
            if blob in Predators : blob.detect(Preys)
            blob.move()
            blob.draw(window)
            if blob.energy <= 0: blob.die()
        pygame.display.update()

# Quitter Pygame
pygame.quit()
