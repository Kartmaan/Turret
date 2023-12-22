import pygame
import sys
import numpy as np

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
    
    # Translate to the origin, rotate, and translate back
    rotated_points = np.dot(rect_vertices - center, rotation_matrix) + center
    
    return rotated_points

# Initializing Pygame
pygame.init()

# Set window size
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Circles following the vertices of a rotating rect")

# rectangle color
rect_color = (0, 128, 255)  # Bleu

# circles color
circle_color = (255, 0, 0)  # Rouge

# Initial rectangle
initial_rect = pygame.Rect(screen_width//2, screen_height//2, 200, 100)

# Initial angle of rotation
angle = 0

# Rotation speed (degrees per frame)
rotation_speed = 0.5

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

    # ROTATION ARRAY
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

    # Display update
    pygame.display.flip()

    # Change the angle to simulate continuous rotation
    angle += rotation_speed

    # Limit loop speed
    pygame.time.Clock().tick(60)