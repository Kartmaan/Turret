import pygame
import sys
import math

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tracer une ligne avec Pygame")

# Couleur de la ligne (en RGB)
line_color = (0, 0, 0)  # Rouge

# Charger l'image de la tourelle (remplacez le chemin par votre propre image)
tourelle_image = pygame.image.load("assets/images/sprites/turret.png")
original_tourelle_rect = tourelle_image.get_rect(center=(screen_width // 2, screen_height // 2))

# Longueur du segment CD dans le référentiel local
segment_length = 50

# Variables de la boucle principale
angle = 0
rotation_speed = 2  # Vitesse de rotation (en degrés par image)
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
    rotated_tourelle = pygame.transform.rotate(tourelle_image, angle)
    rotated_tourelle_rect = rotated_tourelle.get_rect(center=original_tourelle_rect.center)

    # Calculer la position du point d'ancrage dans le référentiel local
    local_anchor_point = (rotated_tourelle_rect.centerx, rotated_tourelle_rect.centery + segment_length / 2)

    # Tracer la ligne à partir du point d'ancrage local
    target_point = (rotated_tourelle_rect.centerx, rotated_tourelle_rect.centery + 100)
    target_point= (0,0)

    #pygame.draw.line(screen, line_color, local_anchor_point, target_point, 2)
    x2 = rotated_tourelle_rect.midtop[0] * math.sin(angle%360)
    y2 = rotated_tourelle_rect.midtop[1] * math.cos(angle%360)

    pygame.draw.line(screen, line_color, (0,0), (x2, y2), 2)

    # Afficher la tourelle
    screen.blit(rotated_tourelle, rotated_tourelle_rect)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Modifier l'angle pour simuler la rotation continue
    angle += rotation_speed

    # Limiter la vitesse de la boucle
    clock.tick(60)