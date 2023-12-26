import sys
from functions.display import pygame, turret_sprites, mobs_gen
from functions.geometry import midpoint, get_distance, matrix_rotation

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
#print(resized_base)

# Positionnement de la base
base_rect.center = (WIDTH//2, HEIGHT//2)
base_rect = resized_base.get_rect(center=(WIDTH//2, HEIGHT//2))

# ---- TOURELLE
turret_image = turret_sprites()["turret_on"]
turret_rect = turret_image.get_rect()

# Positionnement de la tourelle
turret_rect.center = (WIDTH//2, HEIGHT//2)

# ---- MOBS
mob_sprites = []

# ---- VARIABLES D'ANIMATION
# Variables de la boucle principale
angle = 0
ROTATION_SPEED = 0.5 # Initial speed
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
            mob = mobs_gen()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dist = get_distance((WIDTH//2, HEIGHT//2), (mouse_x, mouse_y))
            #print(dist)
            
            new_mob = {'image':mob, 
            'rect': mob.get_rect(center=(mouse_x, mouse_y)),
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
    rotated_turret = pygame.transform.rotate(turret_image, angle)
    rotated_turret_rect = rotated_turret.get_rect(center=turret_rect.center)

    # ---- SHOW REFERENTIAL POINTS
    rotated_points = matrix_rotation(turret_rect, angle)
    
    # Get vertex coordinates
    top_left = tuple(rotated_points[0])
    top_right = tuple(rotated_points[1])
    bottom_right = tuple(rotated_points[2])
    bottom_left = tuple(rotated_points[3])
    
    # Vertices
    circle_color = (255,0,0)
    circle_radius = 5
    circle_topleft = pygame.draw.circle(screen, circle_color, top_left, circle_radius)
    circle_topright = pygame.draw.circle(screen, circle_color, top_right, circle_radius)
    circle_bottomleft = pygame.draw.circle(screen, circle_color, bottom_left, circle_radius)
    circle_bottomright = pygame.draw.circle(screen, circle_color, bottom_right, circle_radius)
    
    # Cannon
    circle_color = (0,0,255)
    cannon_point = midpoint(top_left, top_right)
    circle_cannon = pygame.draw.circle(screen, circle_color, cannon_point, circle_radius)
    
    # Laser referential
    circle_color = (255,0,255)
    top_ref = midpoint(top_left, top_right, offset=-44)
    bottom_ref = midpoint(bottom_left, bottom_right, offset=-44)
    laser_ref = midpoint(top_ref, bottom_ref, offset=15)
    circle_top_ref = pygame.draw.circle(screen, circle_color, top_ref, circle_radius)
    circle_bot_ref = pygame.draw.circle(screen, circle_color, bottom_ref, circle_radius)
    circle_laser_ref = pygame.draw.circle(screen, circle_color, laser_ref, 10)


    
    
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
      turret_image = turret_sprites()["turret_deploy"]
    else:
      rotation_speed = ROTATION_SPEED
      turret_image = turret_sprites()["turret_on"]

    # Limiter la vitesse de la boucle
    clock.tick(60)