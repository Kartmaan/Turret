import os
from functions.display import pygame, random, turret_sprites
from functions.sound import sounds

sentinel_sound = sounds("sentinel")
alert_sound = sounds("alert")

deploy_sound = sounds("deploy")
deploy_played = 0

rain_sound = sounds("rain")
rain_played = 0

class SteamAnimation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.folder = "assets/images/sprites/anim/steam"
        self.number_of_sprites = self.how_many_sprites(self.folder)
        
        self.in_animation = False
        self.steam_played = 0
        self.sprites = []
        
        for i in range(0,self.number_of_sprites):
            path = self.folder + f"/steam_{i}.png"
            #path = f"assets/images/sprites/anim/steam/steam_{i}.png"
            img = pygame.image.load(path)
            img = pygame.transform.smoothscale_by(img, 0.5)
            self.sprites.append(img)
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.center = pygame.math.Vector2(100,100)
    
    def how_many_sprites(self, folder:str) -> int:
        number_of_files = 0

        for file in os.listdir(folder):
            extension = os.path.splitext(file)[1]

            if extension == ".png":
                number_of_files += 1
        
        return number_of_files
    
    def arrange(self, refs:dict):
        """ TODO : Arranger l'orientation du sprite selon les 
        coordonnées 'steam_origin' et 'steam_end' """
        self.sprites = []
        self.rect.center = refs["steam_origin"]
        for i in range(0,self.number_of_sprites):
            path = self.folder + f"/steam_{i}.png"
            #path = f"assets/images/sprites/anim/steam/steam_{i}.png"
            img = pygame.image.load(path)
            img = pygame.transform.smoothscale_by(img, 0.5)
            self.sprites.append(img)
            
    def animate(self, anim_bool:bool = True):
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

def steam_jet(screen:pygame.surface.Surface, refs:dict):
    steam_sprites.empty()
    steam_anim.arrange(refs)
    steam_sprites.add(steam_anim)
    
    steam_sprites.draw(screen)
    steam_sprites.update(refs, 0.16)
    
    if steam_anim.steam_played < 1:
        steam_anim.animate(anim_bool=True)

def rotate_turret(screen:pygame.surface.Surface, rotationObject,
                  refs:dict):
    """Rotates the turret

    Args:
        screen: The main surface on which to draw
        rotationObject: Rotation object
    """
    global deploy_played    
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    if rotationObject.mode == "sentinel":
        deploy_played = 0
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
        
        steam_jet(screen, refs)
        
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