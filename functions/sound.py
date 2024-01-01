from functions.display import pygame

pygame.mixer.init()
sentinel_sound = pygame.mixer.Sound("assets/sound/sentinel.ogg")

alert_sound = pygame.mixer.Sound("assets/sound/alert.ogg")
alert_sound.set_volume(0.7)

deploy_sound = pygame.mixer.Sound("assets/sound/deploy.wav")
deploy_sound.set_volume(0.4)

rain_sound = pygame.mixer.music.load("assets/sound/rain.ogg")

def sounds(sound_name:str) -> pygame.mixer.Sound:
    """ Returns the desired sound """
    sounds_dict = {
        "sentinel": sentinel_sound,
        "alert" : alert_sound,
        "deploy" : deploy_sound,
        "rain" : rain_sound
    }
    
    return sounds_dict[sound_name]