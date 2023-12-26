import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Exemple de rotation de Vector2")

# Couleur de la ligne (en RGB)
line_color = (255, 0, 0)  # Rouge

# Position initiale du vecteur
start_vector = pygame.math.Vector2(screen_width//2, screen_height//2)

# Vecteur qui sera utilisé pour représenter la ligne
line_vector = start_vector + pygame.math.Vector2(200, 200)

# Angle initial
angle = 0

# Vitesse de rotation (en degrés par image)
rotation_speed = -0.5

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Effacer l'écran
    screen.fill((255, 255, 255))  # Fond blanc

    # Dessiner la ligne initiale
    pygame.draw.line(screen, line_color, start_vector, line_vector, 2)

    # Mettre à jour le vecteur en fonction de la rotation
    line_vector = start_vector + pygame.math.Vector2(400, 0).rotate(angle)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Modifier l'angle pour simuler la rotation continue
    angle += rotation_speed

    # Limiter la vitesse de la boucle
    pygame.time.Clock().tick(60)