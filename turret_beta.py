import sys
from functions.display import pygame, Mobs, turret_sprites, laser
from functions.display import background, debug_mode
from functions.geometry import ref_points, detection
from functions.animation import Rotation, rotate_turret, make_it_rain

rotation = Rotation()

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turret")

debug = True
rain = False
clock = pygame.time.Clock()
fps = 60

# ---- BASE
# Image de la base
base_image = pygame.image.load("assets/images/sprites/turret_base.png")
base_rect = base_image.get_rect()

# Redimension de la base
coef = 0.5 #2
new_base_size = (base_rect.width*coef, base_rect.height*coef)
resized_base = pygame.transform.smoothscale(base_image, new_base_size)
#print(resized_base)

# Positionnement de la base
base_rect.center = (WIDTH//2, HEIGHT//2)
base_rect = resized_base.get_rect(center=(WIDTH//2, HEIGHT//2))
#print(base_rect)

# ---- TOURELLE
turret_image = turret_sprites()["turret_on"]
turret_rect = turret_image.get_rect()
#print(turret_rect)

# Positionnement de la tourelle
turret_rect.center = (WIDTH//2, HEIGHT//2)

# ---- MOBS
mobs = Mobs()

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          mobs.add_mob(screen, pygame.mouse.get_pos())
    
    # Effacer l'écran
    screen.fill((25, 25, 25))
    
    if not debug:
      background(screen)
    
    # Affichage continu des mobs
    for mob in mobs.living_mobs:
      screen.blit(mob['image'], mob['rect'])

    # Affichage de la base
    if not debug:
      screen.blit(resized_base, base_rect)

    refs = ref_points(screen, turret_rect, rotation.angle)
    
    # ---- MISE A JOUR
    # Affichage de la rotation
    rotate_turret(screen, rotation, refs)
    laser_segment = laser(screen, refs["laser_start"], rotation.angle)
    laser_detect = detection(laser_segment[0], laser_segment[1], mobs.living_mobs)
    
    if debug:
      debug_mode(screen, refs, rotation, mobs)
      
    if rain:
      make_it_rain(screen)
    
    if laser_detect == None:
      rotation.mode="sentinel"
      
    if laser_detect != None:
      rotation.mode="alert"
      
    cannon_detect = detection(refs["cannon"], refs["target"], mobs.living_mobs)
    if cannon_detect != None:
      rotation.mode="fire"
    
    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la vitesse de la boucle
    clock.tick(fps)