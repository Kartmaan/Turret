import os
from functions.display import pygame, random
from functions.sound import SoundManager

sounds = SoundManager()
deploy_played = 0
rain_played = 0
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
    self.current_speed = 0
    self.rotation_speed_sentinel = 0.6
    self.rotation_speed_alert = 0.1
    self.rotation_speed_fire = 0.0 # No rotation
    self.mode = "sentinel" # "alert", "fire"
    
  def rotate(self):
    """Increases the angle value depending on the rotation mode"""
    if self.mode == "sentinel": # Search for targets
      self.angle += self.rotation_speed_sentinel
      self.current_speed = self.rotation_speed_sentinel
    if self.mode == "alert": # Target found
      self.angle += self.rotation_speed_alert
      self.current_speed = self.rotation_speed_alert
    if self.mode == "fire": # Ready to fire
      self.angle += self.rotation_speed_fire
      self.current_speed = self.rotation_speed_fire
    
  def get_angle(self):
    """ Get current turret angle """
    return int(self.angle%360)

class SteamAnimation(pygame.sprite.Sprite):
    """ Animation of the steam jet """
    def __init__(self):
        super().__init__()
        self.folder = "assets/images/sprites/anim/steam"
        self.number_of_sprites = self.how_many_sprites(self.folder)
        
        self.in_animation = False
        self.steam_played = 0
        self.sprites = []
        
        for i in range(0,self.number_of_sprites):
            path = self.folder + f"/steam_{i}.png"
            img = pygame.image.load(path)
            img = pygame.transform.smoothscale_by(img, 0.5)
            self.sprites.append(img)
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        #self.rect.bottomleft = pygame.math.Vector2(100,100)
    
    def how_many_sprites(self, folder:str) -> int:
        """Determines how many .png files are in the folder

        Args:
            folder : Path of the folder containing the sprites

        Returns:
            int: Number of sprites contained in the folder
        """        
        number_of_files = 0

        for file in os.listdir(folder):
            extension = os.path.splitext(file)[1]

            if extension == ".png":
                number_of_files += 1
        
        return number_of_files
    
    def arrange(self, refs:dict, rotationObject):
        """ Adapts the size and rotation of sprites based 
        on reference points 
        TODO : Arranger l'orientation du sprite selon les 
        coordonnées 'steam_origin' et 'steam_end' """
        self.sprites = []
        self.rect.center = refs["steam_end"]
        for i in range(0,self.number_of_sprites):
            path = self.folder + f"/steam_{i}.png"
            img = pygame.image.load(path)
            img = pygame.transform.smoothscale_by(img, 0.5)
            #img = pygame.transform.rotate(img, rotationObject.angle)
            self.sprites.append(img)
            
    def animate(self, anim_bool:bool = True):
        """Animation trigger

        Args:
            anim_bool : _description_. Defaults to True.
        """        
        self.in_animation = anim_bool
    
    def update(self, refs:dict, speed:float = 0.15):
        """ TODO :  Changer la position des sprites 
        en fonction des points référentiels refs["steam_origin"]"""
        self.rect.center = refs["steam_origin"]
        if self.in_animation == True:
            self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
            self.in_animation = False
            self.steam_played += 1   
        self.image = self.sprites[int(self.current_sprite)]

steam_sprites = pygame.sprite.Group()
steam_anim = SteamAnimation()

def steam_jet(screen:pygame.surface.Surface, refs:dict,
              rotationObject):
    """Runs the steam jet animation

    Args:
        screen : The main surface on which to draw
        refs : Dictionary containing the coordinates of 
        all reference points
    """    
    steam_sprites.empty()
    steam_anim.arrange(refs, rotationObject)
    steam_sprites.add(steam_anim)
    
    steam_sprites.draw(screen)
    steam_sprites.update(refs, 0.16)
    
    if steam_anim.steam_played < 1:
        steam_anim.animate(anim_bool=True)

def rotate_turret(screen:pygame.surface.Surface, turretObject,
                  rotationObject, refs:dict):
    """Rotates the turret

    Args:
        screen: The main surface on which to draw
        rotationObject: Rotation object
    """
    global deploy_played    
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    if rotationObject.mode == "sentinel":
        steam_anim.steam_played = 0
        deploy_played = 0
        if not pygame.mixer.get_busy():
            sounds.play_sound("sentinel")
        turret_image = turretObject.turret_sentinel
        
    if rotationObject.mode == "alert":
        sounds.stop_sound("sentinel")
        if not pygame.mixer.get_busy():
            sounds.play_sound("alert")
        turret_image = turretObject.turret_alert
    
    if rotationObject.mode == "fire":
        sounds.stop_sound("alert")
        sounds.stop_sound("sentinel")
        turret_image = turretObject.turret_fire
        if not pygame.mixer.get_busy() and deploy_played < 1:
            sounds.play_sound("deploy")
            deploy_played+=1
        
        steam_jet(screen, refs, rotationObject)
        
    turret_rect = turret_image.get_rect()
    turret_rect.center = (WIDTH//2, HEIGHT//2)
    
    rotated_surface = pygame.transform.rotate(turret_image, rotationObject.angle)
    rotated_rect = rotated_surface.get_rect(center=turret_rect.center)
    
    screen.blit(rotated_surface, rotated_rect)
    
    rotationObject.rotate()

def make_it_rain(screen:pygame.surface.Surface):
    """Makes rain appear according to certain parameters

    Args:
        screen : The main surface on which to draw
    """
    global rain_played
    if rain_played < 1:
        sounds.play_rain()
        rain_played += 1
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    raindrop_color = (220, 220, 200)
    raindrop_intensity = 40
    raindrop_length = random.randint(2,10)
    #rain_speed = random.uniform(0.1,0.8)
            
    def generate_raindrop():
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        speed = random.uniform(0.01,0.08)
        return {'x': x, 'y': y, 'speed' : speed}
    
    raindrops = [generate_raindrop() for _ in range(raindrop_intensity)]
    
    for raindrop in raindrops:
        pygame.draw.line(screen, raindrop_color, 
                (raindrop['x'], raindrop['y']),
                (raindrop['x'], raindrop['y'] + raindrop_length), 1)
        
        raindrop['y'] += raindrop['speed']
        
        if raindrop['y'] > HEIGHT:
            raindrop['y'] = 0
            raindrop['x'] = random.randint(0, WIDTH)