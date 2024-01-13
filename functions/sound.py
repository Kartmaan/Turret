from functions.display import pygame

pygame.mixer.init()

class SoundManager():
    def __init__(self):
        # Paths
        self.paths = {
            "sentinel" : "assets/sound/sentinel.ogg",
            "alert" : "assets/sound/alert.ogg",
            "deploy" : "assets/sound/deploy.wav",
            "steam" : "assets/sound/steam.wav",
            "fire" : "assets/sound/fire.wav",
            "destroy" : "assets/sound/destroy.mp3"}
        
        self.sound_adjust = {
            "alert" : 0.7,
            "deploy" : 0.15
        }
        
        self.rain_sound = pygame.mixer.music.load("assets/sound/rain.ogg")
        
        # Sounds
        self.sounds = {}
        for key, path in self.paths.items():
            snd = pygame.mixer.Sound(path)
            if key in self.sound_adjust.keys():
                snd.set_volume(self.sound_adjust[key])
            self.sounds[key] = snd

        # Channels
        self.channels = {key: pygame.mixer.Channel(i) for i, key in enumerate(self.sounds)}

    def play_sound(self, sound_name):
        if sound_name in self.sounds and sound_name in self.channels:
            self.channels[sound_name].play(self.sounds[sound_name])

    def stop_sound(self, sound_name):
        if sound_name in self.channels:
            self.channels[sound_name].stop()

    def is_sound_playing(self, sound_name):
        if sound_name in self.channels:
            return self.channels[sound_name].get_busy()
    
    def set_volume(self, sound_name, val):
        pass
    
    def play_rain(self):
        pygame.mixer.music.play(-1)