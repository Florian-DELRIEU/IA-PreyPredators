import pygame
import math
from pygame_init import *
from classes import blob, Preys, Predators

# Création des blobs
for _ in range(15):
    blob(None, None, None, False, color=GREEN,speed=1)
for _ in range(5):
    blob(None, None, None, True, color=RED, speed=1)

selected_blob = None
running = True
frame = 0
paused = False
clock = pygame.time.Clock()

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

    window.fill(GREY)

    time_string = f"Temps: {frame // 60:02}:{frame % 60:02}"
    text_surface = font.render(time_string, True, WHITE)
    window.blit(text_surface, (width - text_surface.get_width() - 10, 10))

    if selected_blob:
        info_text = f"Type: {'Prédateur' if selected_blob.is_predator else 'Proie'}\n" \
                    f"Generation: {selected_blob.generation:.2f}\n" \
                    f"Speed: {selected_blob.speed:.2f}\n" \
                    f"Energie: {selected_blob.energy:.2f}\n" \
                    f"Cible: {'True' if selected_blob.target else 'False'}"
        selected_blob.create_rays()
        selected_blob.draw_rays(window)
        info_surface = font.render(info_text, True, WHITE)
        window.blit(info_surface, (10, 10))

    if not paused:
        for blob in Predators + Preys:
            if blob in Predators:
                blob.detect(Preys)
            blob.move()
            blob.energy_turn()
        clock.tick(FPS)
        frame += 1

    for blob in Preys + Predators:
        blob.draw(window)

    pygame.display.update()

pygame.quit()
