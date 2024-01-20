""" 
animation.py - Animation module

Module containing the classes and functions responsible for 
different animations, such as turret rotation, rain or projectiles
"""
import os
import time
from functions.display import pygame, random
from functions.sound import get_sounds

sounds = get_sounds()

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
    
  def get_angle(self) -> int:
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
        self.bang_sound_played = 0 # TEST
    
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
        #global bang_sound_played
        self.init_vals(start, target)
        
        if self.bang_played < 1:
            if bang.bang_sound_played < 1:
                sounds.play_sound("fire")
                bang.bang_sound_played += 1
            self.green_val = (self.green_val + self.color_jump) % 255
            radius = random.randint(2,9)
            self.current_pos += self.move_vector * self.speed
            pygame.draw.circle(screen, (255,self.green_val,0), (int(self.current_pos.x), 
                int(self.current_pos.y)), radius)

            if self.current_pos.distance_to(self.target_point) < 5:
                self.bang_played = 1
                mobsObject.destroyed_mob()
                #mobsObject.kill_mob()

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

class RotateTurret:
    def __init__(self):
        self.turret_mode = None
        self.turret_image = None
        self.deploy_sound_played = 0
        #self.bang_sound_played = 0
        
    def sentinel_mode(self, turretObject, mobsObject):
        bang.bang_sound_played = 0
        steam_anim.steam_played = 0
        bang.vals_initialized = 0
        bang.bang_played = 0
        self.deploy_sound_played = 0
        mobsObject.in_target = None
        
        if not sounds.in_playing("sentinel"):
            sounds.play_sound("sentinel")
        
        self.turret_image = turretObject.turret_sentinel
    
    def alert_mode(self, turretObject) -> None:
        sounds.stop_sound("sentinel")
        if not sounds.in_playing("alert"):
            sounds.play_sound("alert")
            
        self.turret_image = turretObject.turret_alert
    
    def fire_mode(self, screen:pygame.surface.Surface, 
                  turretObject, rotationObject:Rotation, 
                  mobsObject, refs:dict) -> None: 
        sounds.stop_sound("alert")
        sounds.stop_sound("sentinel")
        self.turret_image = turretObject.turret_fire
        if self.deploy_sound_played < 1:
            sounds.play_sound("deploy")
            self.deploy_sound_played+=1
        
        if not sounds.in_playing("deploy"):
            steam_jet(screen, refs, rotationObject)
            bang.animate(screen, refs["cannon"], mobsObject.in_target, mobsObject)
    
    def rotate(self, screen:pygame.surface.Surface, 
               turretObject,rotationObject:Rotation, 
               mobsObject, refs:dict) -> None:
        
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()
        
        self.turret_mode = rotationObject.mode
        
        if self.turret_mode == "sentinel":
            self.sentinel_mode(turretObject, mobsObject)
        
        if self.turret_mode == "alert":
            self.alert_mode(turretObject)
        
        if self.turret_mode == "fire":
            self.fire_mode(screen, turretObject, rotationObject,
                           mobsObject, refs)
        
        turret_rect = self.turret_image.get_rect()
        turret_rect.center = (WIDTH//2, HEIGHT//2)
        
        rotated_surface = pygame.transform.rotate(self.turret_image, rotationObject.angle)
        rotated_rect = rotated_surface.get_rect(center=turret_rect.center)
        
        screen.blit(rotated_surface, rotated_rect)
        
        rotationObject.rotate()

class Thunder():
    """Makes lightning appear and thunder heard.
    
    Lightning appears according to a defined probability index 
    and for a limited random time, just like the time between 
    the disappearance of lightning and the sound of thunder."""
    
    def __init__(self):
        self.path = "assets/images/storm.png"
        self.img = pygame.image.load(self.path)
        
        self.in_lightning = False
        self.lightning_start_time = None
        self.lightning_duration = None
        self.lightning_displayed = 0
        
        self.after_lightning = False
        self.after_lightning_start_time = None
        self.after_lightning_duration = None
    
    def lightning_dice(self) -> bool:
        """Function acting like a dice, if it returns True the 
        lightning flash is displayed on the screen, if it returns 
        False nothing is displayed. The lightning() function of 
        this class only displays the lightning image according to 
        the return of this function

        Returns:
            bool: A boolean
        """        
        probability = 0.06
        proba = probability / 100
        
        # The lightning has just disappeared from the screen, 
        # no other lightning must take place for a specific time, 
        # in order to play the sound of thunder. The delay between 
        # lightning and thunder is a random value in seconds :
        # self.after_lightning_duration
        if self.after_lightning:
            duration = time.time() - self.after_lightning_start_time
            if duration <= self.after_lightning_duration: # In time
                return False
            else: # Deadline
                self.after_lightning = False
                sounds.play_sound("thunder")
                return False
        
        # A lightning bolt is being displayed, it will be 
        # displayed for a time determined by 
        # self.lightning_duration. After the time elapses, the 
        # lightning disappears and the self.after_lightning 
        # state variable is set to True
        if self.in_lightning:
            duration = time.time() - self.lightning_start_time
            if duration <= self.lightning_duration: # In time
                return True
            
            else: # Deadline
                self.in_lightning = False
                self.after_lightning_start_time = time.time()
                self.after_lightning_duration = random.uniform(1.5,3.5)
                self.after_lightning = True
                return False
        
        # We assume here that self.in_lightning and 
        # self.after_lightning are False, we nevertheless wait 
        # for the end of the "tunder" sound if it's being played
        # to display a new lightning
        if not sounds.in_playing("thunder"):
            rand_num = random.random()
            
            # The probability is realized, the state variable 
            # self.in_lightning is set to True
            if rand_num < proba: # The probability is realized
                self.lightning_displayed += 1
                self.in_lightning = True
                self.lightning_start_time = time.time()
                self.lightning_duration = random.uniform(0.2,1.2)
                return True
            
            # The probability isn't realized. No lightning
            else:
                self.in_lightning = False
                return False
    
    def lightning(self, screen=pygame.surface.Surface) -> None:
        """Display a lightning bolt on the screen according 
        to the return from self.lightning_dice()

        Args:
            screen: The main Pygame surface where to draw
        """        
        if self.lightning_dice():
            screen.blit(self.img, (0,0))
        
thunder = Thunder()

def get_thunder():
    return thunder

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
        self.strong_wind_sound_played = 0
        self.strong_wind_displayed = 0
    
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
            self.strong_wind_displayed += 1
            self.in_wind = True
            self.wind_start_time = time.time()
            return True
        else:
            self.in_wind = False
            return False
    
    def rain(self) -> None:
        """Shows rain animation on screen"""
        
        #global strong_wind_soung_played
        
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
                self.strong_wind_soung_played = 0
                sounds.fadeout("strong_wind", 1000)
                pygame.draw.line(self.screen, self.raindrop_color,
                        (raindrop['x'], raindrop['y']),
                        (raindrop['x'], raindrop['y'] + raindrop_length), 1)
            
            else: # Wind
                if not sounds.in_playing("strong_wind") and self.strong_wind_soung_played < 1:
                    sounds.play_sound("strong_wind")
                    self.strong_wind_soung_played += 1
                pygame.draw.line(self.screen, self.raindrop_color,
                        (raindrop['x'], raindrop['y']),
                        (raindrop['x'] - raindrop_length, raindrop['y'] + raindrop_length), 1)
            
            #raindrop['y'] += raindrop['speed']
            
            if raindrop['y'] > self.HEIGHT:
                raindrop['y'] = 0
                raindrop['x'] = random.randint(0, self.WIDTH)
        
        # Probability roll for the display of lightning
        thunder.lightning(self.screen)