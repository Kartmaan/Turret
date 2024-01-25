""" 
animation.py - Animation module

Module containing the classes and functions responsible for 
different animations, such as turret rotation, rain or projectiles
"""
import os
import time
from functions.geometry import np, get_distance, midpoint
from functions.display import pygame, random, get_mobs
from functions.sound import get_sounds

sounds = get_sounds()
mobs = get_mobs()

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
    
    # WORK IN PROGRESS
    if self.mode == "retract": # Ready to retract
        self.angle += self.rotation_speed_fire
        self.current_speed = self.rotation_speed_fire
    
  def get_angle(self) -> int:
    """ Get current turret angle """
    return int(self.angle%360)

rotation = Rotation()

def get_rotation():
    """ Allows other modules to retrieve the rotation object """
    return rotation

# ---------- <WORK IN PROGRESS> ----------
class SteamAnimation(pygame.sprite.Sprite):
    """ WORK IN PROGRESS - NOT YET USED
    TODO : Correctly position the sprites according to the rotations
    from refs["steam_origin] to refs["steam_end"]. 
    Animation of the steam jet """
    def __init__(self):
        super().__init__()
        self.folder = "assets/images/sprites/anim/steam"
        self.number_of_sprites = self.how_many_sprites(self.folder)
        
        self.in_animation = False
        self.steam_played = 0
        self.sprites = []
        
        self.debug_print = 0
        
        for i in range(0,self.number_of_sprites):
            path = self.folder + f"/steam_{i}.png"
            img = pygame.image.load(path)
            img = pygame.transform.smoothscale_by(img, 0.5)
            #img = pygame.transform.rotate(img, 90)
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
        on reference points"""
        sprite_rect = self.sprites[1].get_rect()
        self.sprites = []
        origin = refs["steam_origin"]
        end = refs["steam_end"]
        
        angle_rad = np.arctan2(end.y - origin.y, end.x - origin.x)
        angle_rad = np.degrees(angle_rad)
        
        distance = get_distance(origin, end)
        
        rect = pygame.Rect(0, 0, sprite_rect.width,  distance)
        rect.center = midpoint(origin, end)
        
        for i in range(0,self.number_of_sprites):
            path = self.folder + f"/steam_{i}.png"
            img = pygame.image.load(path)
            img = pygame.transform.smoothscale_by(img, 0.5)
            img = pygame.transform.rotate(img, -angle_rad)
            rotated_rect = img.get_rect(center=rect.center)
            self.sprites.append(img)
            
    def animate(self, anim_bool:bool = True):
        """Animation trigger

        Args:
            anim_bool : _description_. Defaults to True.
        """        
        self.in_animation = anim_bool
    
    def update(self, refs:dict, speed:float = 0.15):
        self.rect.center = refs["steam_origin"]
        if self.in_animation == True:
            self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
            self.in_animation = False
            self.steam_played += 1   
        self.image = self.sprites[int(self.current_sprite)]

# WORK IN PROGRESS - NOT YET USED
steam_sprites = pygame.sprite.Group()
steam_anim = SteamAnimation()

def steam_jet(screen:pygame.surface.Surface, refs:dict,
              rotationObject):
    """ WORK IN PROGRESS - NOT YET USED
    Runs the steam jet animation

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
# ---------- </WORK IN PROGRESS> ----------

class Blast(pygame.sprite.Sprite):
    """ Blast animation """
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.folder = "assets/images/sprites/anim/blast"
        self.nb_of_sprites = self.how_many_sprites(self.folder)
        
        self.images = []
        self.blast_played = 0 # Animation counter
        self.blast_sound_played = 0 # Sound counter
        self.target_hit = False
        
        for num in range(1, self.nb_of_sprites+1):
            img = pygame.image.load(f"assets/images/sprites/anim/blast/blast_{num}.png")
            img = pygame.transform.smoothscale_by(img, 0.2)
            self.images.append(img)
        
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.counter = 0
    
    def positioning(self, pos:tuple):
        """Place the center of the explosion at the coordinates 
        of the currently targeted mob

        Args:
            pos: Coordinates of the center of the explosion
            (tuple or Vector2)
        """        
        self.rect.center = pos
    
    def update(self):
        explosion_speed = 5
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
            mobs.kill_mob()
            self.index = 0
            self.counter = 0
            self.blast_played += 1
    
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

blast_group = pygame.sprite.Group()        
blast_anim = Blast()

def blast_launcher(screen:pygame.surface.Surface):
    """Launching the blast animation.
    
    The animation is only launched at the precise moment when 
    the projectile comes into contact with the targeted mob. 
    The function is called in the fire_mode() function of 
    the RotateTurret class.

    Args:
        screen: Main Pygame surface
    """    
    blast_anim.positioning(mobs.in_target)
    blast_group.draw(screen)
    blast_group.update()
    blast_group.add(blast_anim)

class Projectile():
    """Projectile animation"""
    
    def __init__(self):
        self.start_point = None
        self.target_point = None
        self.current_pos = None
        self.move_vector = None
        self.speed = 3
        self.bang_played = 0 # Animation counter
        self.bang_sound_played = 0 # Sound counter
        self.vals_initialized = 0 # Process counter
        self.retract_sound_palayed = 0 # WORK IN PROGRESS 
    
    def init_vals(self, start:pygame.math.Vector2, 
             target:pygame.math.Vector2):
        """Sets constructor attribute values, like the starting 
        and ending point of the projectile as well as calculating 
        the direction vector

        Args:
            start: Projectile starting point coordinates
            target: Projectile target point coordinates
        """
        # Since this function will be called in a local loop of 
        # the program (the fire_mode function of the RotateTurret 
        # class), we ensure that the values are only initialized 
        # once
        if self.vals_initialized < 1:
            self.start_point = start
            self.target_point = target
            self.current_pos = self.start_point
            self.move_vector = self.target_point - self.start_point
            
            # The magnitude of the vector is normalized to 1 
            # because we are only interested in the direction.
            self.move_vector.normalize_ip()
            
            self.vals_initialized = 1
            
            # The green value of the projectile's RGB varies in 
            # color_jump steps during the animation
            self.green_val = 200
            self.color_jump = 20
    
    def animate(self, screen:pygame.surface.Surface, start:pygame.math.Vector2, 
             target:pygame.math.Vector2, mobsObject):
        """Start of projectile animation

        Args:
            screen: Main Pygame surface
            start: Projectile starting point coordinates
            target: Projectile target point coordinates
            mobsObject: Mobs object
        """

        # Initialization of the values necessary for establishing 
        # the trajectory
        self.init_vals(start, target)
        
        if self.bang_played < 1:
            # Play sound
            if projectile.bang_sound_played < 1:
                sounds.play_sound("fire")
                projectile.bang_sound_played += 1
                
            # We vary the green value and set random values to 
            # the projectile radius to add a flame effect
            self.green_val = (self.green_val + self.color_jump) % 255
            radius = random.randint(2,9)
            
            # Movement of the projectile according to the defined 
            # vector and speed
            self.current_pos += self.move_vector * self.speed
            
            # Projectile display
            pygame.draw.circle(screen, (255,self.green_val,0), (int(self.current_pos.x), 
                int(self.current_pos.y)), radius)

            # The projectile has reached its destination, we add a 
            # proximity margin to ensure that the point will not 
            # be skipped
            if self.current_pos.distance_to(self.target_point) < 5:
                self.bang_played = 1 # Animation counter
                
                # The targeted projectile is transformed into 
                # debris so that the turret remains aligned until 
                # the explosion animation ends
                mobsObject.destroyed_mob()
                
                # Signal sent to the Blast class object to let it 
                # know that the explosion can take place. The 
                # fire_mode() function of the Rotate Turret class 
                # will be responsible for launching it
                blast_anim.target_hit = True
                
                # Play blast sound
                if not sounds.in_playing("blast"):
                    sounds.play_sound("blast")
                    blast_anim.blast_sound_played+=1

projectile = Projectile()

class RotateTurret:
    """Turns the turret according to the different rotation modes 
    (sentinel, alert, fire). These modes are defined by the 
    Rotation class"""
    
    def __init__(self):
        self.turret_mode = None
        self.turret_image = None
        self.deploy_sound_played = 0
    
    def reset_states(self):
        """Reset all state variables when resuming sentinel mode"""
        
        # Blast class
        blast_anim.target_hit = False
        blast_anim.blast_played = 0
        blast_anim.blast_sound_played = 0
        
        # Projectile class
        projectile.bang_sound_played = 0
        projectile.vals_initialized = 0
        projectile.bang_played = 0
        
        self.deploy_sound_played = 0
        steam_anim.steam_played = 0 # WORK IN PROGRESS
        
    def sentinel_mode(self, turretObject, mobsObject):
        """The turret is searching for a target

        Args:
            turretObject: TurretSprites object (from display module)
            mobsObject: Mobs object (from display module)
        """
        self.reset_states() # Resetting all state variables
        mobsObject.in_target = None # No target 
        
        # Play sentinel sound
        if not sounds.in_playing("sentinel"):
            sounds.play_sound("sentinel")
        
        # Set turret sprite
        self.turret_image = turretObject.turret_sentinel
    
    def alert_mode(self, turretObject) -> None:
        """The turret laser has detected a mob

        Args:
            turretObject: TurretSprites object (from display module)
        """        
        sounds.stop_sound("sentinel") # Stop sentinel sound
        
        # Play alert sound
        if not sounds.in_playing("alert"):
            sounds.play_sound("alert")
        
        # Set turret sprite
        self.turret_image = turretObject.turret_alert
    
    def fire_mode(self, screen:pygame.surface.Surface, 
                  turretObject, mobsObject, refs:dict) -> None:
        """The turret cannon is aligned with the mob.
        
        The Rotation class sets the fire mode rotation speed 
        to 0.0, i.e. the turret is stationary. This mode launches 
        the projectile animation as well as the blast animation

        Args:
            screen: Main Pygame surface
            turretObject: TurretSprites object (from display module)
            mobsObject : Mobs object (from display module) 
            refs (dict): All referential points
        """
        # Sounds to stop
        sounds.stop_sound("alert")
        sounds.stop_sound("sentinel")
        
        # Set turret sprite
        self.turret_image = turretObject.turret_fire
        
        # Play deploy sound
        if self.deploy_sound_played < 1:
            sounds.play_sound("deploy")
            self.deploy_sound_played+=1
        
        # When the sound deploy is finished, the projectile 
        # animation is started
        if not sounds.in_playing("deploy"):
            #steam_jet(screen, refs, rotationObject) # WIP
            projectile.animate(screen, refs["cannon"], mobsObject.in_target, mobsObject)

        # The projectile has reached the coordinates of the mob, 
        # the blast animation can be started
        if blast_anim.target_hit and blast_anim.blast_played < 1:
            blast_launcher(screen)
        
    def rotate(self, screen:pygame.surface.Surface, 
               turretObject,rotationObject:Rotation, 
               mobsObject, refs:dict) -> None:
        """Rotates the turret according to the angle and speed 
        determined by the Rotation class

        Args:
            screen: Main Pygame surface
            turretObject: TurretSprites object (from display module)
            rotationObject: Rotation object
            mobsObject: Mobs object (from display module)
            refs: All referential points
        """        
        
        # Get the main surface size
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()
        
        # Get the rotation mode from the Rotation object
        self.turret_mode = rotationObject.mode
        
        # Launching the function according to the rotation mode
        if self.turret_mode == "sentinel":
            self.sentinel_mode(turretObject, mobsObject)
        
        if self.turret_mode == "alert":
            self.alert_mode(turretObject)
        
        if self.turret_mode == "fire":
            self.fire_mode(screen, turretObject,
                           mobsObject, refs)
        
        # Turret positioning
        turret_rect = self.turret_image.get_rect()
        turret_rect.center = (WIDTH//2, HEIGHT//2)
        
        # Turret surface and rect rotation
        rotated_surface = pygame.transform.rotate(self.turret_image, rotationObject.angle)
        rotated_rect = rotated_surface.get_rect(center=turret_rect.center)
        
        # Display
        screen.blit(rotated_surface, rotated_rect)
        
        # The angle value is incremented by a value defined by 
        # the actual Rotation class mode
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