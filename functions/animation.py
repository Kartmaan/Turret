from functions.display import pygame, random, turret_sprites
from functions.sound import sounds

sentinel_sound = sounds("sentinel")
alert_sound = sounds("alert")
deploy_sound = sounds("deploy")
deploy_played = 0
rain_sound = sounds("rain")
rain_played = 0

def steam_animation():
    pass

def rotate_turret(screen:pygame.surface.Surface, rotationObject):
    """Rotates the turret

    Args:
        screen: The main surface on which to draw
        rotationObject: Rotation object
    """
    global deploy_played    
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    if rotationObject.mode == "sentinel":
        if not pygame.mixer.get_busy():
            sentinel_sound.play()
        turret_image = turret_sprites()["turret_on"]
        
    if rotationObject.mode == "alert":
        sentinel_sound.fadeout(10)
        if not pygame.mixer.get_busy():
            alert_sound.play()
        turret_image = turret_sprites()["turret_alert"]
    
    if rotationObject.mode == "fire":
        alert_sound.fadeout(10)
        sentinel_sound.stop()
        turret_image = turret_sprites()["turret_deploy"]
        if not pygame.mixer.get_busy() and deploy_played < 1:
            deploy_sound.play()
            deploy_played+=1
        
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
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    raindrop_color = (220, 220, 200)
    raindrop_intensity = 40
    raindrop_length = random.randint(2,10)
    #rain_speed = random.uniform(0.1,0.8)
    
    """ global rain_played
    if not rain_played < 1:
            rain_sound.play()
            rain_played+=1 """
            
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