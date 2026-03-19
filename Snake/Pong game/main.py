import pygame 
import sys
import random


def reset_ball():
    global ball_speed_x, ball_speed_y

    ball.x = screen_width/2 - 10
    ball.y = random.randint(10,100)

    ball_speed_x *= random.choice([1,-1]) # Randomly choose to start the ball moving left or right
    ball_speed_y *= random.choice([1,-1]) # Randomly choose to start the ball moving up or down

def points_won(winner):
    global cpu_points, player_points

    if winner == "cpu":
        cpu_points += 1 # Increment the CPU score by 1
    if winner == "player":
        player_points += 1 # Increment the player score by 1

    reset_ball() # Reset the ball to the center of the screen after a point is scored
    

def animate_ball():
    global ball_speed_x, ball_speed_y

    ball.x += ball_speed_x
    ball.y += ball_speed_y


    if ball.bottom >= screen_height or ball.top <= 0:
        ball_speed_y *= -1 # Reverse the vertical speed of the ball if it hits the top or bottom of the screen

    if ball.right >= screen_width:
        points_won("cpu") # Call the function to update the score when the ball hits the right side of the screen

    if ball.left <= 0:
        points_won("player") # Call the function to update the score when the ball hits the left side of the screen 

    if ball.colliderect(player) or ball.colliderect(cpu):
        ball_speed_x *= -1 # Reverse the horizontal speed of the ball if it hits the player or CPU paddle


def animate_player():
    player.y += player_speed

    if player.top <= 0 :
        player.top = 0 # Prevent the player paddle from going above the top of the screen
    if player.bottom >= screen_height:
        player.bottom = screen_height # Prevent the player paddle from going below the bottom of the screen


def animated_cpu():
    global cpu_speed
    cpu.y += cpu_speed

    if ball.centery <= cpu.centery:
        cpu_speed = -6 # Move the CPU paddle up if the ball is above it
    if ball.centery >= cpu.centery:
        cpu_speed = 6 # Move the CPU paddle down if the ball is below it

    if cpu.top <= 0:
        cpu.top = 0 # Prevent the CPU paddle from going above the top of the screen
    if cpu.bottom >= screen_height:
        cpu.bottom = screen_height # Prevent the CPU paddle from going below the bottom of the screen


pygame.init() # Initialize Pygame

screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height)) # Create the game window
pygame.display.set_caption("Ping Pong Game") # Set the window title

clock = pygame.time.Clock() # Create a clock object to control the frame rate


# ball and players parameters

ball = pygame.Rect(0,0,30,30) # Create a rectangle for the ball
ball.center = (screen_width/2, screen_height/2) # Set the initial position of the ball to the center of the screen

cpu = pygame.Rect(0,0,20,100) # Create a rectangle for the CPU paddle
cpu.centery = screen_height/2 # Set the initial position of the CPU paddle to the center of the screen

player = pygame.Rect(0,0,20,100)    # Create a rectangle for the player paddle
player.midright = (screen_width, screen_height/2) # Set the initial position of the player paddle to the right side of the screen

ball_speed_x = 6 # Set the initial horizontal speed of the ball
ball_speed_y = 6 # Set the initial vertical speed of the ball
player_speed = 0 # Set the initial speed of the player paddle to 0
cpu_speed = 6 # Set the speed of the CPU paddle

cpu_points = 0 # Initialize the CPU score
player_points = 0 # Initialize the player score

# score font
score_font = pygame.font.Font(None, 100) # Create a font object for displaying the score

while True:
    #Check for events
    for event in pygame.event.get(): # Loop through all events
        if event.type == pygame.QUIT: # If the user clicks the close button
            pygame.quit() # Quit Pygame
            sys.exit() # Exit the program

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -6 # Move the player paddle up
            if event.key == pygame.K_DOWN:
                player_speed = 6 # Move the player paddle down

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_speed = 0 # Stop the player paddle when the key is released



   
   
    # Change the position of the objects
    animate_ball() # Call the function to animate the ball
    animate_player() # Call the function to animate the player paddle
    animated_cpu() # Call the function to animate the CPU paddle
   

    #Drawing the game objects
    screen.fill("black") # Fill the screen with black color

    cpu_score_surface = score_font.render(str(cpu_points), True, "white")
    player_score_surface = score_font.render(str(player_points), True, "white")

    screen.blit(cpu_score_surface,(screen_width/4, 20)) # Draw the CPU score on the screen
    screen.blit(player_score_surface,(3*screen_width/4, 20)) # Draw the player score on the screen

    pygame.draw.aaline(screen, "white", (screen_width/2, 0),(screen_width/2, screen_height)) # Draw a line in the middle of the screen
    pygame.draw.ellipse(screen,"white", ball)
    pygame.draw.rect(screen,"white", cpu)
    pygame.draw.rect(screen,"white", player)
    #Update the display 
    pygame.display.update() 
    clock.tick(65) # Limit the frame rate to 60 frames per second
