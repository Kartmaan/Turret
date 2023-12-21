import pygame
import sys

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
initial_rect = pygame.Rect(100, 100, 200, 100)

# Initial angle of rotation
angle = 0.0

# Rotation speed (degrees per frame)
rotation_speed = 0.5

# Circles radius
circle_radius = 5

# Create a surface from initial rect
# Add some padding so we can also draw the circles there
padded_rect = initial_rect.inflate((2*circle_radius, 2*circle_radius))
surface = pygame.Surface((padded_rect.width, padded_rect.height), pygame.SRCALPHA)

# Use rectangles with coords relative to the surface:
relative_rect = pygame.Rect(0, 0, initial_rect.width, initial_rect.height)

# ...and translate this one to make room for the circles
moved_rect = relative_rect.move(circle_radius, circle_radius)

# Draw our rectangle just once
pygame.draw.rect(surface, rect_color, moved_rect, 2)

# Circles: we draw them on surface, instead of on screen
# The cicrcle positions are the corners of moved_rect
top_left = moved_rect.topleft
top_right = moved_rect.topright
bottom_left = moved_rect.bottomleft
bottom_right = moved_rect.bottomright
circle_topleft = pygame.draw.circle(surface, circle_color, top_left, circle_radius)
circle_topright = pygame.draw.circle(surface, circle_color, top_right, circle_radius)
circle_bottomleft = pygame.draw.circle(surface, circle_color, bottom_left, circle_radius)
circle_bottomright = pygame.draw.circle(surface, circle_color, bottom_right, circle_radius)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear screen
    screen.fill((255, 255, 255))  # Fond blanc

    # Rotate the surface according to the angle
    rotated_surface = pygame.transform.rotate(surface, angle)

    # Obtain the rectangle surrounding the rotating surface.
    # We do this because pygame rotates around one of the corners of the surface
    # and we want our image centered.
    rotated_rect = rotated_surface.get_rect(center=padded_rect.center)

    # Draw the rotated rectangle
    screen.blit(rotated_surface, rotated_rect.topleft)

    # Display update
    pygame.display.flip()

    # Change the angle to simulate continuous rotation
    angle += rotation_speed

    # Limit loop speed
    pygame.time.Clock().tick(60)