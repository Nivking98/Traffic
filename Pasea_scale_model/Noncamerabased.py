import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Window Dimensions
screen_width, screen_height = 840, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Moving Vehicle Example')

# Load image from path
image_path = 'C:\\Users\\Nivan\\Desktop\\Dataset\\Pasea_scale_model\\Intersectionj2.png'
background_image = pygame.image.load(image_path).convert()  # Use convert() for faster blitting
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Scale image to fit screen

# Colors for current and future use:
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (180, 180, 0)

# Vehicle dimensions and speed in pixels
vehicle_width, vehicle_height = 37, 15
vehicle_x, vehicle_y = 0, 180  # Initial position
vehicle_speed = 55  # Speed in pixels per second

# Clock dor frame rate
clock = pygame.time.Clock()
fps = 60

# Fonts allocation
font = pygame.font.SysFont('Arial', 20)

# Simulation parameters
start_time = time.time()
simulation_duration = 20  # seconds

# Define the invisible rectangle for vehicle counting to simulate non camera based vehicle detection
invisible_rect_top_left = (286, 160)
invisible_rect_bottom_right = (356, 210)

# Main game program
running = True
vehicle_count = 0  # Initial vehicle count
while running:
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time > simulation_duration:
        break  # Exit program after simulation time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Physics of vehicle movement
    if vehicle_x + vehicle_speed / fps + vehicle_width < screen_width:
        vehicle_x += vehicle_speed / fps  # Update based on speed and frame rate

    # Check if the vehicle is within the non camera based detector denoted by invisible rectangle
    if (invisible_rect_top_left[0] <= vehicle_x <= invisible_rect_bottom_right[0] - vehicle_width) and \
       (invisible_rect_top_left[1] <= vehicle_y <= invisible_rect_bottom_right[1] - vehicle_height):
        vehicle_count = 1  # Vehicle is within the rectangle
    else:
        vehicle_count = 0  # Once vehicle is not within the rectangle

    # load background png
    screen.blit(background_image, (0, 0))

    # spawn vehicle
    pygame.draw.rect(screen, BLUE, (vehicle_x, vehicle_y, vehicle_width, vehicle_height))

    # Show FPS
    fps_text = font.render(f'FPS: {clock.get_fps():.2f}', True, pygame.Color('white'))
    screen.blit(fps_text, (10, 10))

    # Show simulation time
    sim_time_text = font.render(f'Time: {int(elapsed_time)}s', True, pygame.Color('white'))
    screen.blit(sim_time_text, (10, 35))

    # Show vehicle count
    vehicle_count_text = font.render(f'Vehicles: {vehicle_count}', True, pygame.Color('white'))
    screen.blit(vehicle_count_text, (10, 60))  # Displayed under the simulation time

    # Renew display
    pygame.display.flip()
 
    # FPS Capper
    clock.tick(fps)

# Quit Pygame
pygame.quit()
sys.exit()



