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
        offset : Offset from center (-/+)

    Returns:
        tuple: The coordinates of the desired point
    """
    x = (point1[0] + point2[0]) / 2 + offset * (point2[0] - point1[0]) / np.linalg.norm([point2[0] - point1[0], point2[1] - point1[1]])
    y = (point1[1] + point2[1]) / 2 + offset * (point2[1] - point1[1]) / np.linalg.norm([point2[0] - point1[0], point2[1] - point1[1]])
    
    return pygame.math.Vector2(x, y)

def get_distance(p1: tuple, p2: tuple) -> float:
  """Returns the distance between two coordinates

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
    """Rotate the vertices coordinates of a rect at a given angle

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

def ref_points(rect: pygame.rect.Rect, angle:float) -> dict:
    """Sets turret reference points at each rotation angle.
    These points are used to precisely place different elements 
    such as the laser or projectiles

    Args:
        rect: A Rect object
        angle: Angle in degrees

    Returns:
        dict: A dictionary containing the coordinates 
        of all reference points
    """    
    rotated_points = matrix_rotation(rect, angle)
    
    # Verices
    top_left = tuple(rotated_points[0])
    top_right = tuple(rotated_points[1])
    bottom_right = tuple(rotated_points[2])
    bottom_left = tuple(rotated_points[3])
    
    # Cannon
    cannon_point = midpoint(top_left, top_right)
    
    # Get distances
    small_side = get_distance(top_left, cannon_point)
    long_side = get_distance(top_right, midpoint(top_right, bottom_right))
    
    # Laser referentials
    top_laser = midpoint(top_left, top_right, offset=-48)
    bottom_laser = midpoint(bottom_left, bottom_right, offset=-48)
    laser_start = midpoint(top_laser, bottom_laser, offset=20)
    
    # Sides
    steam_left = midpoint(top_left, bottom_left, offset=10)
    steam_right = midpoint(top_right, bottom_right, offset=10)
    
    refs = {
        "top_left" : top_left,
        "top_right" : top_right,
        "bottom_right" : bottom_right,
        "bottom_left" : bottom_left,
        "left_side" : steam_left,
        "right_side" : steam_right,
        "cannon" : cannon_point,
        "top_laser" : top_laser,
        "bottom_laser" : bottom_laser,
        "laser_start" : laser_start
    }
    
    return refs
    
def detection(origin:tuple, end:tuple, mob_sprites:list):
    for mob in mob_sprites:
        pos = mob['pos']
        form1 = np.sqrt((pos[0]-origin[0])**2 + (pos[1]-origin[1])**2)
        form2 = np.sqrt((pos[0]-end[0])**2 + (pos[1]-end[1])**2)
        form3 = np.sqrt((end[0]-origin[0])**2 + (end[1]-origin[1])**2)
        
        if int(form1+form2) == form3:
            #print("DETECTED!")
            return pos