import pygame, sys, random
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Set up fonts for title and score display
title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

# Define colors (RGB values)
GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

# Game grid settings - INCREASED SIZE FOR BETTER VISIBILITY
cell_size = 28  # Increased from 20 to 28 for larger cells
number_of_cells = 20  # Keep 20x20 grid

# Border offset from screen edges - INCREASED to make room for title
OFFSET = 80  # Increased from 50 to 80 to give more space at top

# Food class - manages food position and drawing
class Food:
    def __init__(self, snake_body):
        # Initialize food at a random position not occupied by snake
        self.position = self.generate_random_pos(snake_body)

    # Draw the food on screen
    def draw(self):
        # Create rectangle at food position
        food_rect = pygame.Rect(
            OFFSET + self.position.x * cell_size,  # Add OFFSET to x coordinate
            OFFSET + self.position.y * cell_size,  # Add OFFSET to y coordinate
            cell_size, 
            cell_size
        )
        screen.blit(food_surface, food_rect)

    # Generate random coordinates within grid
    def generate_random_cell(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        return Vector2(x, y)

    # Generate random position that is not in snake's body
    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        
        # Keep generating new positions until we find one not in snake body
        while position in snake_body:
            position = self.generate_random_cell()  # FIXED: Added parentheses to call the function
            
        return position

# Snake class - manages snake movement and drawing
class Snake:
    def __init__(self):
        # Initial snake body (3 segments)
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)  # Initial movement direction (right)
        self.add_segment = False  # Flag for when snake eats food
        self.eat_sound = pygame.mixer.Sound("sound/eat.mp3")
        self.wall_hit_sound = pygame.mixer.Sound("sound/wall.mp3")

    # Draw the snake on screen
    def draw(self):
        for segment in self.body:
            # Create rectangle for each segment with OFFSET
            segment_rect = (
                OFFSET + segment.x * cell_size,
                OFFSET + segment.y * cell_size,
                cell_size,
                cell_size
            )
            pygame.draw.rect(screen, DARK_GREEN, segment_rect)

    # Update snake position
    def update(self):
        # Add new head in direction of movement
        self.body.insert(0, self.body[0] + self.direction)

        # If snake ate food, keep the tail (grow), otherwise remove tail
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]  # Remove last segment
    
    # Reset snake to initial state (for game over)
    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)

# Game class - manages game state and collisions
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"  # Game state: RUNNING or STOP
        self.score = 0

    # Draw all game elements
    def draw(self):
        self.food.draw()
        self.snake.draw()
    
    # Update game logic
    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    # Check if snake head collides with food
    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            # Generate new food position
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True  # Snake will grow
            self.score += 1
            self.snake.eat_sound.play()

    # Check if snake hits the walls
    def check_collision_with_edges(self):
        # Check horizontal boundaries
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        
        # Check vertical boundaries
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    # Game over sequence
    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOP"  # Stop game until key press
        self.score = 0
        self.snake.wall_hit_sound.play()

    # Check if snake hits its own body
    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]  # All segments except head
        if self.snake.body[0] in headless_body:
            self.game_over()

# Set up the game window - RECALCULATED with new OFFSET
window_width = 2 * OFFSET + cell_size * number_of_cells
window_height = 2 * OFFSET + cell_size * number_of_cells
screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Retro Snake")

# Game clock for controlling frame rate
clock = pygame.time.Clock()

# Create game instance
game = Game()

# Load food image
food_surface = pygame.image.load("Graphics/food.png")

# Custom event for snake movement updates
SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)  # Trigger every 200ms

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        # Snake movement update
        if event.type == SNAKE_UPDATE:
            game.update()
        
        # Quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Keyboard input
        if event.type == pygame.KEYDOWN:
            # Restart game if stopped
            if game.state == "STOP":
                game.state = "RUNNING"

            # Direction controls (prevent reversing)
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)

    # Drawing section
    screen.fill(GREEN)  # Clear screen with background color
    
    # Draw border around game area
    pygame.draw.rect(
        screen, 
        DARK_GREEN, 
        (OFFSET - 5, OFFSET - 5, cell_size * number_of_cells + 10, cell_size * number_of_cells + 10), 
        5  # Border thickness
    )
    
    # Draw game elements (snake and food)
    game.draw()
    
    # Render and display title - POSITIONED HIGHER
    title_surface = title_font.render("Retro Snake", True, DARK_GREEN)
    title_rect = title_surface.get_rect(center=(window_width // 2, OFFSET // 2))
    screen.blit(title_surface, title_rect)
    
    # Render and display score - POSITIONED LOWER
    score_surface = score_font.render(f"Score: {game.score}", True, DARK_GREEN)
    score_rect = score_surface.get_rect(center=(window_width // 2, window_height - OFFSET // 2))
    screen.blit(score_surface, score_rect)
    
    # Update display
    pygame.display.update()
    
    # Control game speed (60 FPS)
    clock.tick(60)