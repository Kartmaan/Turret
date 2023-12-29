import pygame
import numpy as np

def get_distance(p1: tuple, p2: tuple) -> float:
  distance = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
  return distance

p1 = pygame.math.Vector2(1,3)
p2 = pygame.math.Vector2(5,6)

print(p1.distance_to(p2))
print(get_distance(p1, p2))
