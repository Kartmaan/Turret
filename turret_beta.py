import sys
from functions.display import pygame, turret_sprites, mobs_gen
from functions.display import laser, debug_mode
from functions.geometry import get_distance, ref_points, detection
from functions.animation import rotate_turret

class Rotation():
  """ The positions and angular velocities of the turret are crucial 
  values in the program and must be able to be consulted and modified 
  by most functions. For this we create a Rotation class whose 
  instantiated object can be distributed to the functions concerned 
  and manipulated by them so that all parties are aware of the 
  states of the turret.
  The object has 3 rotation modes: 'sentinel', 'alert' and 'fire' 
  with different rotation speeds for each of them
  """  
  def __init__(self):
    self.angle = 0
    self.rotation_speed_sentinel = 0.5
    self.rotation_speed_alert = 0.07
    self.rotation_speed_fire = 0.0
    self.mode = "sentinel" # "alert", "fire"
    
  def rotate(self):
    if self.mode == "sentinel": # Search for targets
      self.angle += self.rotation_speed_sentinel
    if self.mode == "alert": # Target found
      self.angle += self.rotation_speed_alert
    if self.mode == "fire": # Ready to fire
      self.angle += self.rotation_speed_fire
    
  def get_angle(self):
    """ Get current turret angle """
    return int(self.angle%360)

rotation = Rotation()

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turret")

debug = True
detected = False
clock = pygame.time.Clock()
fps = 60

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

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          max_mobs = 8
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

    refs = ref_points(screen, turret_rect, rotation.angle)
    
    if debug:
      debug_mode(screen, refs)
    
    # ---- MISE A JOUR
    # Affichage de la rotation
    rotate_turret(screen, rotation)
    laser_segment = laser(screen, refs["laser_start"], rotation.angle)
    detect = detection(laser_segment[0], laser_segment[1], mob_sprites)
    
    if detect != None:
      rotation.mode="alert"
      print(detect)
    else:
      rotation.mode="sentinel"
    
    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter la vitesse de la boucle
    clock.tick(fps)