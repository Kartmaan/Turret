import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rotation de deux vecteurs avec Vector2")

# Couleur des lignes (en RGB)
line_color = (255, 0, 0)  # Rouge

# Position initiale du centre de rotation
center = pygame.math.Vector2(screen_width // 2, screen_height // 2)

# Vecteur représentant le rayon de rotation (diamètre plus réduit)
radius_vector = pygame.math.Vector2(25, 0)

# Vecteurs initiaux
start_vector = center + radius_vector
line_vector = center + pygame.math.Vector2(100, 0)

# Angle initial
angle = 0

# Vitesse de rotation (en degrés par image)
rotation_speed = 0.5
small_rad_pos = []
large_rad_pos = []

# ------------------ Boucle principale ------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Effacer l'écran
    screen.fill((255, 255, 255))  # Fond blanc

    # Mettre à jour les vecteurs en fonction de la rotation
    start_vector = center + radius_vector.rotate(angle)
    line_vector = center + pygame.math.Vector2(200, 0).rotate(angle)
    
    # Visualisation du rayon
    if start_vector not in small_rad_pos:
        small_rad_pos.append(start_vector)
    for pos in small_rad_pos:
        pygame.draw.circle(screen, (0,0,0), pos, 2) 
    
    if line_vector not in large_rad_pos:
        large_rad_pos.append(line_vector)
    for pos in large_rad_pos:
        pygame.draw.circle(screen, (0,255,150), pos, 2)

    # Dessiner les lignes
    pygame.draw.line(screen, line_color, start_vector, line_vector, 3)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Modifier l'angle pour simuler la rotation continue
    angle += rotation_speed

    # Limiter la vitesse de la boucle
    pygame.time.Clock().tick(60)