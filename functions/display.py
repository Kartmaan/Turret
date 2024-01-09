import pygame
import random

def turret_sprites(coef:float = 0.67) -> dict:
    """Resize the initial size of turret images by multipling 
    its dimensions by a given value and returns their surface 
    in a dictionary.
    
    The function can be called to directly acquire the desired 
    resized turret sprite as a Surface object. 
    Example : turret_sprites()["turret_alert"]

    Args:
        coef: Value at which the dimensions will be multiplied

    Returns:
        dict: A dictionary containing the Surface of each turret
    """    
    images = {
        "turret_on" : pygame.image.load("assets/images/sprites/turret_on.png"),
        "turret_alert" : pygame.image.load("assets/images/sprites/turret_alert.png"),
        "turret_deploy" : pygame.image.load("assets/images/sprites/turret_deploy.png")
    }
    
    resized_sprites = {}
    
    for key, img in images.items():
        rect = img.get_rect()
        new_size = (rect.width*coef, rect.height*coef)
        resized = pygame.transform.smoothscale(img, new_size)
        resized_sprites[key] = resized
    
    return resized_sprites

def mobs_gen(coef:float = 0.10) -> pygame.surface.Surface:
    """Resize mobs and generates them randomly so they can be displayed
    on click

    Args:
        coef: Value at which the dimensions will be multiplied

    Returns:
        pygame.surface.Surface: A Surface containing the mob
    """    
    mobs = [
        pygame.image.load("assets/images/sprites/mob_1.png"),
        pygame.image.load("assets/images/sprites/mob_2.png"),
        pygame.image.load("assets/images/sprites/mob_3.png")
    ]
    
    mob = random.choice(mobs)
    rect = mob.get_rect()
    new_size = (rect.width*coef, rect.height*coef)
    resized_mod = pygame.transform.smoothscale(mob, new_size)
    
    return resized_mod

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
    thickness = 4
    length = pygame.math.Vector2(0,-screen_width).rotate(-angle)
    pygame.draw.line(screen, color, origin, origin+length, thickness)
    
    return origin, origin+length

def background(screen:pygame.surface.Surface):
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    background_img = pygame.image.load("assets/images/background.png")
    background_img = background_img.convert()
    screen.blit(background_img, (0,0))

def debug_mode(screen:pygame.surface.Surface, refs:dict, 
               rotationObject):
    """Shows on-screen information about animation states.
    Like highlighting reference points

    Args:
        screen: The main surface on which to draw
        refs: Dictionary containing the coordinates of 
        all reference points
    """
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    for key, pos in refs.items():
        pygame.draw.circle(screen, (255,0,0), (pos[0], pos[1]), 5)
    
    # Cannon target line
    pygame.draw.line(screen, (255,255,255), refs["cannon"], refs["target"], 2)