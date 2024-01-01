import dis
import numpy as np
import pygame

def matrix_rotation(rect: pygame.rect.Rect,angle: float) -> np.ndarray:
    
    center = np.array(rect.center)
    rect_vertices = np.array([
        rect.topleft, rect.topright, rect.bottomright, 
        rect.bottomleft])
    
    angle_rad = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ]) 
    rotated_points = np.dot(rect_vertices - center, rotation_matrix) + center
    
    return rotated_points

res = dis.dis(matrix_rotation)
print(res)