import sys
import math
import pygame

def get_distance(p1: tuple, p2: tuple) -> float:
  """Returns the distance between two coordinates

  Args:
  p1 : First coordinates
  p2 : Second coordinates

  Returns:
  The distance between the two coordinates 
  """
  distance = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
  return distance

def get_angle(p1:tuple, p2:tuple) -> float:
  angle_rad = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
  angle_deg = math.degrees(angle_rad)
  return angle_deg

def get_angle_2(p1, p2, p3):
  # Vecteur des deux côtés
  vector1 = (p1[0] - p2[0], p1[1] - p2[1])
  vector2 = (p3[0] - p2[0], p3[1] - p2[1])

  # Calcul du produit scalaire
  dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

  # Calcul des longueurs des vecteurs
  magn1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
  magn2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

  # Angle en radian
  angle_rad = math.acos(dot_product / (magn1 * magn2))

  # Conversion degré
  angle_deg = math.degrees(angle_rad)

  return angle_deg

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turret")

# ---- BASE
# Image de la base
base_image = pygame.image.load("assets/images/sprites/turret_base.png")
base_rect = base_image.get_rect()

# Redimension de la base
coef = 2 #2
new_base_size = (base_rect.width//coef, base_rect.height//coef)
resized_base = pygame.transform.smoothscale(base_image, new_base_size)
print(resized_base)

# Positionnement de la base
base_rect.center = (WIDTH//2, HEIGHT//2)
base_rect = resized_base.get_rect(center=(WIDTH//2, HEIGHT//2))

# ---- TOURELLE
# Image de la tourelle
turret_image = pygame.image.load("assets/images/sprites/turret.png")
turret_rect = turret_image.get_rect()

# Redimension de la tourelle
coef = 1.5 #1.5
new_turret_size = (turret_rect.width//coef, turret_rect.height//coef)
resized_turret = pygame.transform.smoothscale(turret_image, new_turret_size)
print(resized_turret)

# Positionnement de la tourelle
turret_rect.center = (WIDTH//2, HEIGHT//2)

# ---- ROTATING LASER
# Position initiale
rect = resized_turret.get_rect()
center = (WIDTH//2, HEIGHT//2)

# Rayon de rotation de center
radius_vector = pygame.math.Vector2(20,0)

# Vecteurs initiaux
start_vector = center + radius_vector
line_vector = center + pygame.math.Vector2(WIDTH//2,0)

# ---- MOBS
# Image du mob
mob_image = pygame.image.load("assets/images/sprites/mob.png")
mob_rect = mob_image.get_rect()

# Redimension du mob
coef = 10
new_mob_size = (mob_rect.width//coef, mob_rect.height//coef)
resized_mob = pygame.transform.smoothscale(mob_image, new_mob_size)

# Emplacement des mobs
mob_sprites = []

# ---- VARIABLES D'ANIMATION
# Variables de la boucle principale
angle = 0
ROTATION_SPEED = -0.5
rotation_speed = ROTATION_SPEED  # Vitesse de rotation (en degrés par image)
clock = pygame.time.Clock()

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          max_mobs = 5
          if len(mob_sprites) <= max_mobs-1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dist = get_distance((WIDTH//2, HEIGHT//2), (mouse_x, mouse_y))

            new_mob = {'image':resized_mob, 
            'rect': resized_mob.get_rect(center=(mouse_x, mouse_y)),
            'pos' : (mouse_x, mouse_y),
            'dist' : dist}

            mob_sprites.append(new_mob)
            #print(mob_sprites)

    # Effacer l'écran
    screen.fill((25, 25, 25))  # Fond blanc

    # Affichage continu des mobs
    for mob in mob_sprites:
      screen.blit(mob['image'], mob['rect'])

    # Affichage de la base
    screen.blit(resized_base, base_rect)

    # Rotation de la tourelle
    rotated_turret = pygame.transform.rotate(resized_turret, angle)
    rotated_turret_rect = rotated_turret.get_rect(center=turret_rect.center)

    # ---- STATIC LASER
    from_point = (rotated_turret_rect.center[0]-50, rotated_turret_rect.center[1]+20)
    target = (from_point[0], from_point[1]-(WIDTH*2))
    pygame.draw.line(screen, (255,0,0), from_point, target, 2)

    # ---- ROTATING LASER
    # Mise à jour des vecteurs en fonction de la rotation
    #start_vector = center + radius_vector.rotate(angle)
    start_vector = pygame.math.Vector2((rotated_turret_rect.center[0], rotated_turret_rect.center[1])) + radius_vector.rotate(angle)
    line_vector = center + pygame.math.Vector2(WIDTH*2, 0).rotate(-angle)

    # Dessiner ligne
    pygame.draw.line(screen, (255,0,0), start_vector, line_vector, 2)

    # ---- MISE A JOUR
    # Affichage de la rotation
    screen.blit(rotated_turret, rotated_turret_rect)

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Modifier l'angle pour simuler la rotation continue
    angle += rotation_speed
    #print(int(angle%360))

    if 180 <= int(angle % 360) <= 270:
      rotation_speed = ROTATION_SPEED-0.2
    else:
      rotation_speed = ROTATION_SPEED

    # Limiter la vitesse de la boucle
    clock.tick(60)