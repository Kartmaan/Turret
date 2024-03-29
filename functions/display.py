""" 
display.py - Display module

Module bringing together the classes and functions used 
to resize and display the different elements of the 
scene on the screen
Note : The Pygame module is only imported into this module, 
the other functions refer to this import to use the pygame 
functions
"""
import random
import os
import time
import pygame
from functions.geometry import get_distance
from functions.sound import SoundManager, get_sounds

start_time = time.time()
sounds = get_sounds()
class Mobs():
    """Class generating mobs, make them appear 
    on the screen when you click and make them disappear when 
    they are destroyed. All mobs displayed on the screen are 
    contained in a list self.living_mobs including their
    respective position and other informations. 
    The instantiated object of this class can be shared and 
    manipulated by all parties concerned so that they are 
    aware of the number of mobs present and their position
    """    
    def __init__(self):
        self.folder = "assets/images/sprites"
        self.size_reduction = 0.10
        self.potential_mobs = self.loading_sprites()
        self.living_mobs = []
        self.max_living_mobs = 10
        self.turret_base_proximity = 100
        self.in_target = None
    
    def how_many_sprites(self, folder:str) -> int:
        """Determines how many mob .png files are in the folder.
        
        Mob sprites must be .png files and respect the syntax: 
        'mob_<number>' (mob_1, mob_2,...)

        Args:
            folder : Path of the folder containing the mob sprites

        Returns:
            int: Number of mob sprites contained in the folder
        """        
        number_of_files = 0

        for file in os.listdir(folder):
            name = os.path.splitext(file)[0]
            extension = os.path.splitext(file)[1]

            if name.startswith('mob') and extension == ".png":
                number_of_files += 1
        
        return number_of_files
    
    def loading_sprites(self, coef:float = 0.10) -> list:
        """Loads all the mob sprites contained in the folder 
        which can potentially appear during a click. Sprites 
        are also resized by reducing their size by a 'coef' factor

        Args:
            coef : Reduction size factor

        Returns:
            list: All potential mobs
        """
        coef = self.size_reduction        
        mobs = []
        
        for i in range(1, self.how_many_sprites(self.folder)+1):
            path = self.folder + f"/mob_{i}.png"
            img = pygame.image.load(path)
            img = pygame.transform.smoothscale_by(img, coef)
            mobs.append(img)
        
        return mobs
    
    def mobs_gen(self) -> pygame.surface.Surface:
        """Generates mobs randomly so they can be displayed
        on click

        Returns:
            pygame.surface.Surface: A Surface containing the mob
        """    
        mobs = self.potential_mobs
        mob = random.choice(mobs)
    
        return mob
    
    def too_close_to_base(self, rect:pygame.Rect, pos:tuple) -> bool:
        """Checks if the mob's position isn't too close to the 
        turret base

        Args:
            rect : Turret base rect
            pos : Cursor position when clicked

        Returns:
            bool : True if too close, False otherwise
        """
        # The rect base is slightly inflated to also include 
        # its proximity
        proximity = self.turret_base_proximity
        rect = rect.inflate(proximity,proximity)
        
        if rect.collidepoint(pos[0], pos[1]):
            return True
        else:
            return False
    
    def too_close_to_mob(self, pos:tuple) -> bool:
        """Checks if the mob's position isn't too close to another
        mob position 

        Args:
            pos : Cursor position when clicked

        Returns:
            bool: True if too close, False otherwise
        """        
        proximity = 50
        if len(self.living_mobs) >= 1:
            for mob in self.living_mobs:
                rect = mob['rect'].inflate(proximity, proximity)
                if rect.collidepoint(pos[0], pos[1]):
                    return True
            return False
    
    def add_mob(self, screen:pygame.surface.Surface, pos:tuple,
                turret_base:pygame.surface.Surface, refs:dict):
        """Adds a mob to the list of mobs to display 
        (self.living_mobs). 

        Args:
            screen : The main surface on which to draw
            pos : Cursor position when clicked
            turret_base : Get the rect of the surface of the turret 
            base to ensure that no mob can appear on it or in its 
            direct vicinity
        """
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()
        
        turret_base_rect = turret_base.get_rect()
        turret_base_rect.center = (WIDTH//2, HEIGHT//2)
        close_to_base = self.too_close_to_base(turret_base_rect, pos)
        
        close_to_mob = self.too_close_to_mob(pos)
        
        # A new mob is added to the screen upon clicking if these 
        # conditions are met : 
        # 1) The number of mobs present on the screen must not 
        # exceed the value of self.max_living_mobs
        # 2) The mob must not be too close to the turret base
        # 3) The mob must not be too close to another mob
        if (len(self.living_mobs) < self.max_living_mobs and not 
            close_to_base and not close_to_mob):
            if not sounds.in_playing("spawn"):
                sounds.play_sound("spawn")
            mob = self.mobs_gen()
            pos_x, pos_y = pos
            dist = get_distance(refs["cannon"], (pos_x, pos_y))
            
            new_mob = {'image':mob, 
                       'rect':mob.get_rect(center=(pos_x, pos_y)),
                       'pos' : pygame.math.Vector2(pos_x, pos_y),
                       'dist' : int(dist)}
            
            self.living_mobs.append(new_mob)
    
    def destroyed_mob(self):
        """Replaces the image of the mob targeted by a destroyed 
        mob sprite, this allows the turret to remain aligned with 
        the target while the aniamtion of the explosion ends: 
        technically the target is not yet deleted 
        """
        # The size of the image of the destroyed mob is reduced by 
        # a factor identical to that of living mobs in order to 
        # preserve the coherence, the image also undergoes a random 
        # rotation so that the debrits seem different for each destruction
        for idx, mob in enumerate(self.living_mobs.copy()):
            if mob['pos'] == self.in_target:
                img = pygame.image.load("assets/images/sprites/destroyed.png")
                img = pygame.transform.smoothscale_by(img, self.size_reduction)
                img = pygame.transform.rotate(img, random.randint(1,270))
                self.living_mobs[idx]['image'] = img
    
    def kill_mob(self):
        """The targeted mob is definitely destroyed and deleted 
        from the display"""
        for idx, mob in enumerate(self.living_mobs.copy()):
            if mob['pos'] == self.in_target:
                del self.living_mobs[idx]

mobs = Mobs()
def get_mobs():
    return mobs

def turret_base_sprite(coef:float = 0.47) -> pygame.surface.Surface:
    """Loads and resizes the turret base sprite

    Args:
        coef : Reduction factor value. Defaults to 0.5.

    Returns:
        pygame.surface.Surface: _description_
    """    
    base_sprite = pygame.image.load("assets/images/sprites/turret_base.png").convert_alpha()
    base_sprite = pygame.transform.smoothscale_by(base_sprite, coef)
    
    return base_sprite

class TurretSprites():
    """Enables you to recover the surface of the turret sprite 
    which is suitable according to the different rotation modes: 
    sentinel, alert, fire.
    """    
    def __init__(self):
        self.turret_sprites = {
        "turret_sentinel" : pygame.image.load("assets/images/sprites/turret_sentinel.png").convert_alpha(),
        "turret_alert" : pygame.image.load("assets/images/sprites/turret_alert.png").convert_alpha(),
        "turret_fire" : pygame.image.load("assets/images/sprites/turret_fire.png").convert_alpha()}
        
        self.resize()
        
        self.turret_sentinel = self.turret_sprites["turret_sentinel"]
        self.turret_alert = self.turret_sprites["turret_alert"]
        self.turret_fire = self.turret_sprites["turret_fire"]
        
    def resize(self, coef:float = 0.65):
        """Resize sprites according to a factor value (coef)

        Args:
            coef : Reduction size factor
        """        
        for key, img in self.turret_sprites.copy().items():
            resized_sprite = pygame.transform.smoothscale_by(img, coef)
            self.turret_sprites[key] = resized_sprite

def laser(screen:pygame.surface.Surface, origin:tuple,
          angle:float) -> tuple:
    """Draw the detection laser following the rotation 
    of the turret. The function also returns the 
    coordinates of the two points of the laser segment 
    so that they can be exploited for the detection 
    of an intersection with the coordinates of a mob

    Args:
        screen: The main surface on which to draw
        origin: Coordinates of the laser origin
        angle: Angle of rotation at each loop pass

    Returns:
        tuple: The coordinates of the laser segment
    """    
    screen_width = screen.get_width()
    color=(255,0,0)
    thickness = 3
    length = pygame.math.Vector2(0,-screen_width).rotate(-angle)
    pygame.draw.line(screen, color, origin, origin+length, thickness)
    
    return origin, origin+length

def background() -> pygame.surface.Surface: 
    """Load background image

    Returns:
        pygame.surface.Surface: Background Surface
    """     
    background_img = pygame.image.load("assets/images/background_2.png")
    background_img = background_img.convert()
    
    return background_img

def seconds_to_hms(seconds:float) -> str:
    """Convert seconds to hh:mm:ss format

    Args:
        seconds: Seconds value (time.time())

    Returns:
        str: seconds in hh:mm:ss format
    """    
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Formating
    formatted_time = "{:02}:{:02}:{:06.3f}".format(int(hours), int(minutes), seconds)

    return formatted_time

def debug_mode(screen:pygame.surface.Surface, refs:dict,
               turret_base:pygame.rect.Rect, 
               rotationObject, mobsObject, 
               soundsObject:SoundManager,
               thunderObject, rainObject, 
               clock:pygame.time.Clock) -> None:
    """Shows on-screen information about animation states.
    Like highlighting reference points

    Args:
        screen: The main Pygame surface
        
        refs: Dictionary containing the coordinates of 
        all reference points
        
        turret_base : Allows you to visualize the perimeter 
        of the turret base as well as its proximity, an area 
        in which mobs cannot appear
        
        rotationObject : Collects information related to the 
        angular state of the turret
        
        mobsObject : Collects information related to the quantity 
        of mobs present on the screen
        
        cannon_detect :
        
        clock : Allows you to retrieve the effective fps value
    """
    global start_time
    
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    
    channels_busy = soundsObject.total_in_playing()
    duration_str = seconds_to_hms(time.time() - start_time)
    
    # Colors
    white = (255,255,255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    orange = (255, 165, 0)
    
    # Load texts
    font = pygame.font.Font(None, 20)
    
    duration = f"Duration : {duration_str}" 
    win_size = f"Window size : {WIDTH}x{HEIGHT}"
    fps = f"FPS : {round(clock.get_fps(), 2)}"
    turret_size = f"Turret size = {int(refs["small_side"])}x{int(refs["long_side"])}"
    angle_text = f"Turret angle : {rotationObject.get_angle()}"
    turret_speed = f"Turret speed : {rotationObject.current_speed}"
    turret_mode = f"Turret mode : {rotationObject.mode}"
    max_mob = f"Maximum mobs : {mobsObject.max_living_mobs}"
    living_mobs = f"Living mobs : {len(mobsObject.living_mobs)}"
    detected_mob = f"Detected mob : {mobsObject.in_target}"
    sounds_playing = f"Sounds playing : {channels_busy[0]}/{channels_busy[1]}"
    strong_wind = f"Strong wind : {rainObject.strong_wind_displayed}"
    lightning = f"Lightning : {thunderObject.lightning_displayed}"
    
    all_text = [duration, win_size, fps, turret_size, angle_text, 
                turret_speed, turret_mode, max_mob, living_mobs, 
                detected_mob, sounds_playing, strong_wind, lightning]
    
    # Displays texts
    pos_x = 20
    pos_y = 20
    offset = 20 # y axis offset
    
    for text in all_text:
        text_surface = font.render(text, True, white)
        text_rect = text_surface.get_rect(topleft=(pos_x, pos_y))
        screen.blit(text_surface, text_rect)
        pos_y += offset
    
    # Displays turret base rect and its proximity, areas in which 
    # mobs cannot appear
    
    proximity = mobsObject.turret_base_proximity
    turret_base_inflated = turret_base.inflate(proximity, proximity) 
    
    turret_base_inflated.center = (WIDTH//2, HEIGHT//2)
    turret_base.center = (WIDTH//2, HEIGHT//2)
    
    pygame.draw.rect(screen, green, turret_base, 2)
    pygame.draw.rect(screen, orange, turret_base_inflated, 2)
    
    # Displays referential points
    vertices = ["top_left", "top_right", "bottom_right", "bottom_left"]
    for key, pos in refs.items():
        if not isinstance(pos, float):
            if key in vertices:
                pygame.draw.circle(screen, white, (pos[0], pos[1]), 4)
            else: 
                pygame.draw.circle(screen, red, (pos[0], pos[1]), 4)
    
    # Displays cannon target line
    pygame.draw.line(screen, white, refs["cannon"], refs["target"], 2)