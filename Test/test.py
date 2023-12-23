import sys
import numpy as np
import pygame

def midpoint(point1: tuple, 
             point2: tuple,
             offset: float = 0.0) -> pygame.math.Vector2:
    """Returns the central point between two coordinates

    Args:
        point1 : Coordinates of the 1st point
        point2 : Coordinates of the 2nd point

    Returns:
        tuple: Coordinates of the center between point1 and point2
    """    
    x_mid = (point1[0] + point2[0]) / 2 + offset * (point2[0] - point1[0]) / np.linalg.norm([point2[0] - point1[0], point2[1] - point1[1]])
    y_mid = (point1[1] + point2[1]) / 2 + offset * (point2[1] - point1[1]) / np.linalg.norm([point2[0] - point1[0], point2[1] - point1[1]])
    
    return pygame.math.Vector2(x_mid, y_mid)

def matrix_rotation(rect: pygame.rect.Rect,
                    angle: float) -> np.ndarray:
    """Rotate the vertices coordinates of a rect at a given angle

    Args:
        rect : A pygame.rect.Rect object
        angle : The angle of rotation in degrees

    Returns:
        np.ndarray: Vertices coordinate array after rotation
    """

    center = np.array(rect.center)
    rect_vertices = np.array([
        rect.topleft, rect.topright, rect.bottomright, rect.bottomleft
    ])
    
    angle_rad = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ]) 
    
    rotated_points = np.dot(rect_vertices - center, rotation_matrix) + center
    
    return rotated_points

# Initializing Pygame
pygame.init()
clock = pygame.time.Clock()
fps = 60

# Set window size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circles following the vertices of a rotating rect")

# rectangle color
rect_color = (0, 128, 255)  # Blue

# circles color
circle_color = (255, 0, 0)  # Red

# Initial rectangle
initial_rect = pygame.Rect(WIDTH//2, HEIGHT//2, 200, 100)

# Initial angle of rotation (degrees)
angle = 0

# Rotation speed (degrees per frame)
rotation_speed = 0.3

# Circles radius
circle_radius = 5

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear screen
    screen.fill((255, 255, 255))  # Fond blanc

    # Create a surface from initial rect
    surface = pygame.Surface((initial_rect.width, initial_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(surface, rect_color, (0, 0, initial_rect.width, initial_rect.height), 2)

    # Rotate the surface according to the angle
    rotated_surface = pygame.transform.rotate(surface, angle)

    # Obtain the rectangle surrounding the rotating surface
    rotated_rect = rotated_surface.get_rect(center=initial_rect.center)

    # Draw the rectangle
    screen.blit(rotated_surface, rotated_rect)

    # Coordinates rotation
    # We use the rect of the initial static rectangle
    rotated_points = matrix_rotation(initial_rect, angle)

    # Get vertex coordinates
    top_left = tuple(rotated_points[0])
    top_right = tuple(rotated_points[1])
    bottom_right = tuple(rotated_points[2])
    bottom_left = tuple(rotated_points[3])

    # Create circles
    circle_topleft = pygame.draw.circle(screen, circle_color, top_left, circle_radius)
    circle_topright = pygame.draw.circle(screen, circle_color, top_right, circle_radius)
    circle_bottomleft = pygame.draw.circle(screen, circle_color, bottom_left, circle_radius)
    circle_bottomright = pygame.draw.circle(screen, circle_color, bottom_right, circle_radius)
    
    # Side circle
    center_point = midpoint(top_right, bottom_right, offset=-20)
    circle_center = pygame.draw.circle(screen, (0,20,0), center_point, circle_radius+2)

    # Laser
    rot = pygame.math.Vector2(WIDTH+10, 0).rotate(-angle)
    pygame.draw.line(screen, (255,0,0), center_point, center_point+rot, 2)

    # Display update
    pygame.display.flip()

    print(angle%360)
    
    # Change the angle to simulate continuous rotation
    """ if 185 <= angle%360 <= 180:
        rotation_speed = 0.1
    else:
        rotation_speed = 0.5 """
    angle += -rotation_speed

    # Limit loop speed
    clock.tick(fps)