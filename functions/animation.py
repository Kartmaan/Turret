""" 
animation.py - Animation module

Module containing the classes and functions responsible for 
different animations, such as turret rotation, rain or projectiles
"""
import os
import time
from functions.display import pygame, random
from functions.sound import SoundManager

sounds = SoundManager()

# Some sounds should only be played once when the event occurs, 
# these variables will make it possible to ensure it. It will be 
# uncremented by 1 when the event takes place and reset to 0 at 
# the exit of the event
deploy_sound_played = 0
bang_sound_played  = 0
strong_wind_soung_played = 0

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

class BangAnimation():
    """Projectile animation"""
    
    def __init__(self):
        self.start_point = None
        self.target_point = None
        self.current_pos = None
        self.move_vector = None
        self.speed = 3
        self.bang_played = 0 # Animation
        self.vals_initialized = 0
    
    def init_vals(self, start:pygame.math.Vector2, 
             target:pygame.math.Vector2):
        if self.vals_initialized < 1:
            self.start_point = start
            self.target_point = target
            self.current_pos = self.start_point
            self.move_vector = self.target_point - self.start_point
            self.move_vector.normalize_ip()
            self.vals_initialized = 1
            self.green_val = 200
            self.color_jump = 20
    
    def animate(self, screen:pygame.surface.Surface, start:pygame.math.Vector2, 
             target:pygame.math.Vector2, mobsObject):
        global bang_sound_played
        self.init_vals(start, target)
        
        if self.bang_played < 1:
            if bang_sound_played < 1:
                sounds.play_sound("fire")
                bang_sound_played += 1
            self.green_val = (self.green_val + self.color_jump) % 255
            radius = random.randint(2,9)
            self.current_pos += self.move_vector * self.speed
            pygame.draw.circle(screen, (255,self.green_val,0), (int(self.current_pos.x), 
                int(self.current_pos.y)), radius)

            if self.current_pos.distance_to(self.target_point) < 5:
                self.bang_played = 1
                mobsObject.destroyed_mob()
                #mobsObject.kill_mob()

steam_sprites = pygame.sprite.Group()
steam_anim = SteamAnimation()
bang = BangAnimation()

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
                  rotationObject, mobsObject, refs:dict):
    """Rotates the turret

    Args:
        screen: The main surface on which to draw
        rotationObject: Rotation object
    """
    global deploy_sound_played
    global bang_sound_played    
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    if rotationObject.mode == "sentinel":
        steam_anim.steam_played = 0
        bang.vals_initialized = 0
        bang.bang_played = 0
        bang_sound_played = 0
        deploy_sound_played = 0
        mobsObject.in_target = None
        deploy_played = 0
        if not sounds.in_playing("sentinel"):
            sounds.play_sound("sentinel")
        turret_image = turretObject.turret_sentinel
        
    if rotationObject.mode == "alert":
        sounds.stop_sound("sentinel")
        if not sounds.in_playing("alert"):
            sounds.play_sound("alert")
        turret_image = turretObject.turret_alert
    
    if rotationObject.mode == "fire":
        sounds.stop_sound("alert")
        sounds.stop_sound("sentinel")
        turret_image = turretObject.turret_fire
        if deploy_sound_played < 1:
            sounds.play_sound("deploy")
            deploy_sound_played+=1
        
        if not sounds.in_playing("deploy"):
            steam_jet(screen, refs, rotationObject)
            bang.animate(screen, refs["cannon"], mobsObject.in_target, mobsObject)
        
    turret_rect = turret_image.get_rect()
    turret_rect.center = (WIDTH//2, HEIGHT//2)
    
    rotated_surface = pygame.transform.rotate(turret_image, rotationObject.angle)
    rotated_rect = rotated_surface.get_rect(center=turret_rect.center)
    
    screen.blit(rotated_surface, rotated_rect)
    
    rotationObject.rotate()

class Thunder():
    def __init__(self):
        self.path = "assets/images/storm.png"
        self.img = pygame.image.load(self.path)
        self.in_lightning = False
        self.lightning_start_time = None
        self.lightning_duration = None
    
    def lightning_dice(self):
        probability = 0.04
        proba = probability / 100
        
        if self.in_lightning:
            duration = time.time() - self.lightning_start_time
            if duration <= self.lightning_duration:
                return True
            else:
                self.in_lightning = False
                return False
        
        rand_num = random.random()
        
        if rand_num < proba:
            self.in_lightning = True
            self.lightning_start_time = time.time()
            self.lightning_duration = random.uniform(0.2,1.2)
            print(f"lightning - duration : {round(self.lightning_duration,1)}s")
            return True
        else:
            self.in_lightning = False
            return False
    
    def lightning(self, screen=pygame.surface.Surface):
        if self.lightning_dice():
            screen.blit(self.img, (0,0))
        

thunder = Thunder()

class MakeItRain():
    """Shows the rain animation on the screen as well as the 
    effect of the wind on it"""
    
    def __init__(self, screen:pygame.surface.Surface):
        self.screen = screen
        self.WIDTH = self.screen.get_width()
        self.HEIGHT = self.screen.get_height()
        self.raindrop_color = (220, 220, 200)
        self.raindrop_intensity = 40 # Raindrops on screen
        self.in_wind = False # Wind animation in progress
        self.wind_start_time = None
    
    def generate_raindrop(self) -> dict:
        """Generates the coordinates of a raindrop in a dict"""
        
        x = random.randint(0, self.WIDTH)
        y = random.randint(0, self.HEIGHT)
        speed = random.uniform(0.01, 0.08)
        return {'x': x, 'y' : y, 'speed' : speed}
    
    def wind_dice(self) -> bool:
        """Sets the probability for a wind effect to appear. The 
        function returns True if the probability is realized, 
        False otherwise 
        """
        
        # We establish a low probability value because the rain 
        # function will be called each time through the main 
        # Pygame loop, i.e. several dozen times per second 
        # depending on the fps.
        probability = 0.003
        wind_duration = random.randint(3,5)
        
        # A wind effect is already being animated, we ensure that 
        # it lasts a time determined by the value in seconds of 
        # wind_duration
        if self.in_wind:
            duration = time.time() - self.wind_start_time
            if duration <= wind_duration:
                return True
            else:
                self.in_wind = False
                return False
        
        # No wind effect is being animated, we calculate the 
        # probability of realization.
        proba = probability / 100
        rand_num = random.random()
        if rand_num < proba:
            print(f"wind - duration : {wind_duration}s")
            self.in_wind = True
            self.wind_start_time = time.time()
            return True
        else:
            self.in_wind = False
            return False
    
    def rain(self):
        """Shows rain animation on screen"""
        global strong_wind_soung_played
        
        if not sounds.in_playing("rain"):
            sounds.play_sound("rain")
        if not sounds.in_playing("wind"):
            sounds.play_sound("wind")
        
        # Generating coordinates of all raindrops
        raindrops = [self.generate_raindrop() for _ in range(self.raindrop_intensity)]
        
        # Random variation in the length of raindrops
        raindrop_length = random.randint(2,10)
        
        # Drawing raindrops
        for raindrop in raindrops:
            if not self.wind_dice(): # No wind
                strong_wind_soung_played = 0
                sounds.fadeout("strong_wind", 1000)
                pygame.draw.line(self.screen, self.raindrop_color,
                        (raindrop['x'], raindrop['y']),
                        (raindrop['x'], raindrop['y'] + raindrop_length), 1)
            
            else: # Wind
                if not sounds.in_playing("strong_wind") and strong_wind_soung_played < 1:
                    sounds.play_sound("strong_wind")
                    strong_wind_soung_played += 1
                pygame.draw.line(self.screen, self.raindrop_color,
                        (raindrop['x'], raindrop['y']),
                        (raindrop['x'] - raindrop_length, raindrop['y'] + raindrop_length), 1)
            
            #raindrop['y'] += raindrop['speed']
            
            if raindrop['y'] > self.HEIGHT:
                raindrop['y'] = 0
                raindrop['x'] = random.randint(0, self.WIDTH)
        
        thunder.lightning(self.screen)