""" 
sound.py - Sound module

Module containing classes allowing you to load, manipulate 
and play sounds as well as background music.

All sounds were collected from the freesound.org platform and are 
royalty free, some of them have been modified on Audacity by myself.

Credits and thanks :
sentinel : Edited from a sound made by @newlocknew
alert : Edited from a sound made by @plasterbrain
deploy : Edited from a sound made by @Hybrid_V
retract : Edited from a sound made by @Hybrid_V
spawn : @pepingrillin
steam : Edited from a sound made by @reinsamba
fire : @V-ktor
blast : @EFlexMusic
rain : @Garuda1982
wind : @xxamoney27xx
strong wind : Edited from a sound made by @xxamoney27xx
thunder : @Kinoton
music : @SoundFlakes
"""
from functions.display import pygame

pygame.mixer.init()

class SoundManager():
    """Class loading all the sounds likely to be used, allowing 
    them to be manipulated and played via class functions.
    
    Each sound has its own channel and it's these channels that 
    are manipulated. This allows, among other things, to know if 
    a specific sound is being played by checking if its channel 
    is busy.
    """    
    def __init__(self):
        # Paths
        self.paths = {
            "sentinel" : "assets/sound/sentinel.ogg", # 
            "alert" : "assets/sound/alert.ogg",
            "deploy" : "assets/sound/deploy.ogg",
            "retract" : "assets/sound/retract.ogg",
            "spawn" : "assets/sound/spawn.ogg",
            "steam" : "assets/sound/steam.ogg",
            "fire" : "assets/sound/fire.ogg",
            "blast" : "assets/sound/blast.ogg",
            "rain" : "assets/sound/rain.ogg",
            "wind" : "assets/sound/wind.ogg",
            "strong_wind" : "assets/sound/strong_wind.ogg",
            "thunder" : "assets/sound/thunder.ogg"
            }
        
        self.sound_adjust = {
            "sentinel" : 0.44,
            "alert" : 0.33,
            "deploy" : 0.33,
            "fire" : 0.66,
            "blast" : 0.66,
            "rain" : 0.55,
            "wind" : 0.80,
            "strong_wind" : 0.85
        }
        
        # Sounds
        self.sounds = {}
        for key, path in self.paths.items():
            snd = pygame.mixer.Sound(path)
            if key in self.sound_adjust.keys():
                snd.set_volume(self.sound_adjust[key])
            self.sounds[key] = snd

        # Channels
        pygame.mixer.set_num_channels(len(self.paths))
        self.channels = {key: pygame.mixer.Channel(i) for i, key in enumerate(self.sounds)}

    def play_sound(self, sound_name:str) -> None:
        if sound_name in self.sounds and sound_name in self.channels:
            self.channels[sound_name].play(self.sounds[sound_name])

    def pause_sound(self, sound_name:str) -> None:
        if sound_name in self.channels:
            self.channels[sound_name].pause()
    
    def unpause_sound(self, sound_name:str) -> None:
        if sound_name in self.channels:
            self.channels[sound_name].unpause()
    
    def stop_sound(self, sound_name:str) -> None:
        """Stop playback of a channel immediatly

        Args:
            sound_name: The sound name
        """        
        if sound_name in self.channels:
            self.channels[sound_name].stop()
    
    def set_volume(self, sound_name:str, volume:float) -> None:
        if sound_name in self.channels:
            self.channels[sound_name].set_volume(volume)

    def get_volume(self, sound_name:str) -> float:
        if sound_name in self.channels:
            self.channels[sound_name].get_volume()
    
    def fadeout(self, sound_name:str, time:int) -> None:
        """Stop playback of a channel after fading out the sound 
        over the given time argument in milliseconds

        Args:
            sound_name: The sound name
            time: Fadout time in milliseconds
        """        
        if sound_name in self.channels:
            self.channels[sound_name].fadeout(time)

    def in_playing(self, sound_name:str) -> bool:
        if sound_name in self.channels:
            return self.channels[sound_name].get_busy()
    
    def total_in_playing(self) -> tuple:
        num = 0
        for channel in self.channels.values():
            if channel.get_busy():
                num+=1
        
        return num, len(self.channels)

sounds = SoundManager()
def get_sounds(soundManagerObject:SoundManager = sounds) -> SoundManager:
    return soundManagerObject

class MusicManager():
    """Class for loading, playing and pausing background music"""
    def __init__(self):
        # Paths
        self.music = pygame.mixer.music.load("assets/sound/atmosphere.mp3")
    
    def play_music(self, volume=0.66):
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
    
    def pause_music(self):
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        pygame.mixer.music.unpause()