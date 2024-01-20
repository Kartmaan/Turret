import sys
from functions.display import Mobs, TurretSprites, pygame, laser
from functions.display import background, turret_base_sprite, debug_mode
from functions.geometry import ref_points, detection
from functions.animation import Rotation, MakeItRain, RotateTurret
from functions.animation import get_sounds, get_thunder
from functions.sound import MusicManager

# Pygame initialisation
pygame.init()

# Main surface initialisation
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turret")

# Classes
rotation = Rotation()
turrets = TurretSprites()
mobs = Mobs()
rainfall = MakeItRain(screen)
music = MusicManager()
sounds = get_sounds()
thunder = get_thunder()
turret_rotation = RotateTurret()

debug = False
rain = True
music_on = True
clock = pygame.time.Clock()
fps = 60

if music_on:
    music.play_music()

# BACKGROUND
background_img = background()

# TURRET BASE
turret_base = turret_base_sprite()
turret_base_rect = turret_base.get_rect()
turret_base_rect.center = (WIDTH//2, HEIGHT//2)

# TURRET
turret_image = turrets.turret_sentinel
turret_rect = turret_image.get_rect()
turret_rect.center = (WIDTH//2, HEIGHT//2)

# MAIN LOOP
while True:
  # Updating reference points at each rotation angle
  refs = ref_points(screen, turret_rect, rotation.angle)
  
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      
      # LEFT CLICK
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mobs.add_mob(screen, pygame.mouse.get_pos(), turret_base, refs)
      # RIGHT CLICK
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
        mobs.kill_mob()
  
  # Erase screen
  screen.fill((25, 25, 25))
  
  # If debug mode is activated the background and the 
  # turret base isn't displayed
  if not debug:
    screen.blit(background_img, (0,0))
    screen.blit(turret_base, turret_base_rect)
  
  # Display of living mobs
  for mob in mobs.living_mobs:
    screen.blit(mob['image'], mob['rect'])
  
  # Rotates the turret by one angle value
  #rotate_turret(screen, turrets, rotation, mobs, refs)
  turret_rotation.rotate(screen, turrets, rotation, mobs, refs)
  
  # Displays the laser segment and returns the coordinates 
  # of its ends
  laser_segment = laser(screen, refs["laser_start"], rotation.angle)
  
  # Checks if a mob is intersected by the segment and returns 
  # the coordinates of that mob if so. If nothing is detected, 
  # the function returns None
  laser_detect = detection(laser_segment[0], laser_segment[1], mobs.living_mobs)
  
  # Displaying rain
  if rain:
    rainfall.rain()
  
  # No mobs intersected by the laser segment
  if laser_detect == None:
    rotation.mode="sentinel"
  
  # Mob intersected by the laser segment
  if laser_detect != None:
    rotation.mode="alert"
  
  # Checks if a mob is intersected by the cannon segment 
  # (segment visible only in debug mode)
  cannon_detect = detection(refs["cannon"], refs["target"], mobs.living_mobs)
  # Mob intersected by the cannon segment
  if cannon_detect != None:
    rotation.mode="fire"
    mobs.in_target = cannon_detect
  
  # Displaying debug mode
  if debug:
    debug_mode(screen, refs, turret_base_rect, 
                rotation, mobs, sounds, thunder,
                rainfall, clock)
  
  # Display upadate
  pygame.display.flip()

  # Limit loop speed
  clock.tick(fps)