""" 
geometry.py - Geometric functions module

This module provides functions to perform geometric operations 
useful in the context of this project.
"""
import numpy as np
from functions.display import pygame

def midpoint(point1: tuple, 
             point2: tuple,
             offset: float = 0.0) -> pygame.math.Vector2:
    """Returns the central point between two coordinates or a 
    point offset from this center

    Args:
        point1 : Coordinates of the 1st point
        point2 : Coordinates of the 2nd point
        offset : Offset from center (-/+) (default = 0.0)

    Returns:
        tuple: The coordinates of the desired point
    """
    x = (point1[0] + point2[0]) / 2 + offset * (point2[0] - point1[0]) / np.linalg.norm([point2[0] - point1[0], point2[1] - point1[1]])
    y = (point1[1] + point2[1]) / 2 + offset * (point2[1] - point1[1]) / np.linalg.norm([point2[0] - point1[0], point2[1] - point1[1]])
    
    return pygame.math.Vector2(x, y)

def get_distance(p1: tuple, p2: tuple) -> float:
  """Returns the Euclidean distance between two coordinates

  Args:
  p1 : First coordinates
  p2 : Second coordinates

  Returns:
  The distance between the two coordinates 
  """
  distance = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
  return distance

def matrix_rotation(rect: pygame.rect.Rect,
                    angle: float) -> np.ndarray:
    """Rotate the vertices coordinates of a rect at a given angle.
    
    The function allows you to locate the coordinates of the 4 vertices 
    of the initial rect of the turret (i.e. before the start of its rotation), 
    after an angle of rotation centered on the center of the rect. 
    These 4 coordinates will be the bases from which all the reference 
    points of the turret will be calculated in the ref_points() function.
    These points rotate independently of the turret, but because they 
    share the same Rotation object, they rotate together in sync

    Args:
        rect : A pygame.rect.Rect object
        angle : The angle of rotation in degrees

    Returns:
        np.ndarray: Vertices coordinate array after rotation
    """
    # - We retrieve the coordinates of the center of the rectangle 
    # so that rotations can be done around this point.
    # - We then retrieve the coordinates of the 4 static rectangle 
    # vertices in the form of a numpy array
    center = np.array(rect.center)
    rect_vertices = np.array([
        rect.topleft, rect.topright, rect.bottomright, rect.bottomleft
    ])
    
    # - Since most trigonometric functions in math and science 
    # libraries, including Numpy, expect angles in radians, 
    # we convert the angle to that unit.
    # - We create a rotation matrix that defines the desired 
    # rotation angle for each of the coordinates. 
    # In this code the rectangle and the coordinates 
    # of these points share the same angle value ('angle') 
    # so that they rotate in sync
    angle_rad = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ]) 
    
    # We calculate the dot product of the two matrices including 
    # the bias of the 'center' value. 
    # This gives us a new matrix representing the coordinates 
    # of the points after 1 angle of rotation. 
    # It is this matrix that we return.
    rotated_points = np.dot(rect_vertices - center, rotation_matrix) + center
    
    return rotated_points

def ref_points(screen:pygame.surface.Surface, rect: pygame.rect.Rect, 
               angle:float) -> dict:
    """Sets turret reference points at each rotation angle.
    
    These points are used to precisely place different elements 
    such as the laser or projectiles. All points have as base 
    reference the coordinates of the 4 vertices after an angle 
    of rotation, coordinates provided by matrix_roatation()

    Args:
        rect: A Rect object
        angle: Angle in degrees

    Returns:
        dict: A dictionary containing the coordinates 
        of all reference points
    """    
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    rotated_points = matrix_rotation(rect, angle)
    
    # Rect vertices - BASE REFERENTIAL
    top_left = tuple(rotated_points[0])
    top_right = tuple(rotated_points[1])
    bottom_right = tuple(rotated_points[2])
    bottom_left = tuple(rotated_points[3])
    
    # Sides
    left_side = midpoint(top_left, bottom_left)
    right_side = midpoint(top_right, bottom_right)
    bottom = midpoint(bottom_left, bottom_right)
    
    # Get distances
    small_side = get_distance(top_left, top_right)
    long_side = get_distance(top_right, bottom_right)
    #print(small_side, long_side)
    
    # Cannon
    cannon_point = midpoint(top_left, top_right)
    cannon_target = cannon_point+pygame.math.Vector2(0,-WIDTH).rotate(-angle)
    
    # Laser referentials
    top_laser = midpoint(top_left, top_right, offset=-48)
    bottom_laser = midpoint(bottom_left, bottom_right, offset=-48)
    laser_start = midpoint(top_laser, bottom_laser, offset=20)
    
    # Steam referentials
    steam_right_alignment = midpoint(top_right, bottom_right, offset=10)
    steam_left_alignment = midpoint(top_left, bottom_left, offset=10)
    steam_origin = midpoint(steam_left_alignment, steam_right_alignment, offset=40)
    steam_end = steam_origin+pygame.math.Vector2(250,0).rotate(-angle)
    
    refs = {
        # Turret rect referentials
        "top_left" : top_left,
        "top_right" : top_right,
        "bottom_right" : bottom_right,
        "bottom_left" : bottom_left,
        "left_side" : left_side,
        "right_side" : right_side,
        "bottom" : bottom,
        
        # Sizes
        "long_side" : long_side,
        "small_side" : small_side,
        
        # Cannon
        "cannon" : cannon_point,
        "target" : cannon_target,
        
        # Laser
        "top_laser" : top_laser,
        "bottom_laser" : bottom_laser,
        "laser_start" : laser_start,
        
        # Steam
        "steam_origin" : steam_origin,
        "steam_end" : steam_end
    }
    
    return refs
    
def detection(origin:tuple, end:tuple, mob_sprites:list,
              tolerance:float=0.2) -> pygame.math.Vector2:
    """Detects when a mob's coordinates intersect the laser segment.
    
    A-------------M-----B
    If points AB represent the coordinates of the laser segment 
    and point M the coordinates of the mob, we can determine 
    that M is on the segment if the distance AM + MB = AB.
    The function goes through the coordinates of the mobs in 
    mob_sprites, checking for each of them if this equality is 
    respected. If this is the case the function returns 
    the coordinates of the detected mob else it returns None.

    Args:
        origin: Coordinates of the laser segment's origin point
        end: Laser segment end point coordinates
        mob_sprites: Mobs list
        tolerance: Tolerance value for mob detection
    Returns:
        tuple: Coordinates of the detected mob
    """
    val_round = 1    
    for mob in mob_sprites:        
        pos = mob['pos'] # pygame.math.Vector2
        dist1 = round(get_distance(origin, pos), val_round)
        dist2 = round(get_distance(pos, end), val_round)
        dist3 = round(get_distance(origin, end), val_round)
        
        # The sum of the distances dist1 and dist2 can result 
        # in floating values which, depending on the rotation 
        # speed or fps, may never precisely reach equality with 
        # dist 3 (value jump). To remedy this we round the 
        # distance values to 1 decimal place and add a tolerance 
        # value so that a mob is detected even if the laser 
        # is not precisely in its center.
        diff = dist1 + dist2 - dist3
        if abs(diff) <= tolerance:
            return pos