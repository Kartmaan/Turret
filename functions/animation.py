from functions.display import pygame, turret_sprites

pygame.mixer.init()
sentinel_sound = pygame.mixer.Sound("assets/sound/sentinel.mp3")

def steam_animation():
    pass

def rotate_turret(screen:pygame.surface.Surface, rotationObject):
    """Rotates the turret

    Args:
        screen: The main surface on which to draw
        rotationObject: Rotation object
    """    
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    if rotationObject.mode == "sentinel":
        if not pygame.mixer.get_busy():
            sentinel_sound.play()
        turret_image = turret_sprites()["turret_on"]
        
    if rotationObject.mode == "alert":
        sentinel_sound.stop()
        turret_image = turret_sprites()["turret_alert"]
        
    turret_rect = turret_image.get_rect()
    turret_rect.center = (WIDTH//2, HEIGHT//2)
    
    rotated_surface = pygame.transform.rotate(turret_image, rotationObject.angle)
    rotated_rect = rotated_surface.get_rect(center=turret_rect.center)
    
    screen.blit(rotated_surface, rotated_rect)
    
    rotationObject.rotate()