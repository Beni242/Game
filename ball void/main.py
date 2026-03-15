import pygame 
import sys 
import random
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREEN = (20,160,133)

#Ball Parameters 
ball_x = 400
ball_y = 300
ball_radius = 20
ball_x_speed = 0
ball_y_speed = 0
ball_color = pygame.Color("red")
# Create the game window

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("My first pygame Game")

# time and fast of game
clock = pygame.time.Clock()

# random color function

def random_color():
    return(random.randint(0,255), random.randint(0,255), random.randint(0,255))


# Game loop
while True:

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ball_x_speed = 3 # make the ball move right
            if event.key == pygame.K_LEFT:
                ball_x_speed = -3 # make the ball move left
            elif event.key == pygame.K_UP:
                ball_y_speed = -3 # make the ball move up
            elif event.key == pygame.K_DOWN:
                ball_y_speed = 3 # make the ball move down

                


    # updating positions
    ball_x += ball_x_speed
    ball_y += ball_y_speed

    # COLLISION DETECTION
    collision = False # this variable will be used to check if the ball has collided with any wall

    #right wall

    if ball_x + ball_radius > SCREEN_WIDTH:
        ball_x = SCREEN_WIDTH - ball_radius
        ball_x_speed = -ball_x_speed # reverse the x speed to bounce back
        collision = True


    #left wall
    if ball_x - ball_radius < 0:
        ball_x = ball_radius
        ball_x_speed = -ball_x_speed # reverse the x speed to bounce back
        collision = True


    #bottom wall
    if ball_y + ball_radius > SCREEN_HEIGHT:
        ball_y = SCREEN_HEIGHT - ball_radius
        ball_y_speed = -ball_y_speed # reverse the y speed to bounce back       
        collision = True


    #top wall
    if ball_y - ball_radius < 0:
        ball_y = ball_radius
        ball_y_speed = -ball_y_speed # reverse the y speed to bounce back
        collision = True
    
    # change color
    if collision:
        ball_color = random_color()

    # drawing
    window.fill(GREEN) # fill the background with GREEN
    pygame.draw.circle(window, ball_color, (ball_x, ball_y), ball_radius)

    pygame.display.update()
    clock.tick(60) # 60 frames per second
