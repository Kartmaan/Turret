import pygame
import random

def turret_sprites(coef:float = 0.67) -> dict:
    """Resize the initial size of turret images by multipling 
    its dimensions by a given value and returns their surface 
    in a dictionary

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