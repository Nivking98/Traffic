#Load Scale Model
'''Notes:
Phases Controlled by Signal Lights shown on intersectionj.png:
EastIncomingWestBound/ EastIncomingNorthBound = "A1A2" (4 lanes)
WestIncomingEastBound/ WestIncomingSouthBound = "B1B2" (3 lanes)
SouthIncomingNorthBound/ SIEastBound = "C"
NorthIncomingSouthBound/ NIWestBound = "D"

Meters to pixel scaling: 1m = 5pixels
Primary focus of scaling were the horizontal Phases whereby the red rectangle indicates the Queue area:
Whereby A1A2 Queue length = 50m or 250pixels for 1400x1000 resolution original interesectionj.png
And B1B2 Queue length = 30m or 150 pixels (1400x1000) resolution original intersectionj.png
*This Queue Length is important as it is fixed for intersection side A1A2 camera and B1B2 camera.
*A1A2 is Accurate and B1B2 is averaged as some images may not show entire 30m
'''
import pygame
import sys

# Initialize Pygame
pygame.init()

# Open display window resoltion 840x600
screen_width = 840
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Scale Image Example')


# Load the intersection png
image_path = 'C:\\GitHub Repositories\\Traffic\\Pasea_scale_model\\Intersectionj.png' 
image = pygame.image.load(image_path)

#From original res 1400 x 1000 scale factor 0.6
scaled_image = pygame.transform.scale(image, (840, 600))

# Inside Simulation Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Show image
    screen.blit(scaled_image, (0, 0))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

'''Further additions for testing that can be built with aid of GPT but not reproduced as my here:
4 signal lights for each of the 4 main phases
Simulation of non camera based detection of Side C and D for semi actuated control to detect if vehicles present:
Condition based statement: Vehicles present? Yes- Fixed time, No-No time
Lambda based vehicle generation on Phases: A1A2 and B1B2 for testing of #Vehicles passing intersection using:
Fixed Time, Algorithm2-Density Based, Algorithm3 - Time Based.
'''