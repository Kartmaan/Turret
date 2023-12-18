import pygame
import sys
from time import sleep

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turret")

# ---- BASE

# ---- TOURELLE
# Image de la tourelle
turret_image = pygame.image.load("assets/images/sprites/turret.png")
turret_rect = turret_image.get_rect()

# Redimension de la tourelle
coef = 1.5
new_turret_size = (turret_rect.width//coef, turret_rect.height//coef)
resized_turret = pygame.transform.scale(turret_image, new_turret_size)

# Positionnement de la tourelle
turret_rect.center = (WIDTH // 2, HEIGHT // 2)

# ---- VARIABLES D'ANIMATION
# Variables de la boucle principale
angle = 0
rotation_speed = 1  # Vitesse de rotation (en degrés par image)
clock = pygame.time.Clock()

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Effacer l'écran
    screen.fill((255, 255, 255))  # Fond blanc

    # Rotation de la tourelle
    rotated_turret = pygame.transform.rotate(resized_turret, angle)
    rotated_turret_rect = rotated_turret.get_rect(center=turret_rect.center)

    # Affichage de la rotation
    screen.blit(rotated_turret, rotated_turret_rect)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Modifier l'angle pour simuler la rotation continue
    angle += rotation_speed
    print(angle%360)

    if angle % 360 >= 180:
      rotation_speed = 0.5

    # Limiter la vitesse de la boucle
    clock.tick(60)
