import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game states
START = 0
PLAY = 1
GAME_OVER = 2

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize Snake class
class Snake:
    def __init__(self):
        self.body = [((GRID_WIDTH // 2), (GRID_HEIGHT // 2))]
        self.direction = RIGHT

    def change_direction(self, new_direction):
        if (
                (new_direction == UP and not self.direction == DOWN)
                or (new_direction == DOWN and not self.direction == UP)
                or (new_direction == LEFT and not self.direction == RIGHT)
                or (new_direction == RIGHT and not self.direction == LEFT)
        ):
            self.direction = new_direction

    def move(self, food_position):
        new_head = (
            (self.body[0][0] + self.direction[0]) % GRID_WIDTH,
            (self.body[0][1] + self.direction[1]) % GRID_HEIGHT,
        )
        if new_head == food_position:
            self.body.insert(0, new_head)
            return True
        else:
            self.body.insert(0, new_head)
            self.body.pop()
            return False

    def check_collision(self):
        if self.body[0] in self.body[1:]:
            return True
        return False

    def get_head_position(self):
        return self.body[0]

    def get_body(self):
        return self.body

# Initialize Food class
class Food:
        def __init__(self):
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            self.is_food_on_screen = True

        def spawn_food(self):
            if not self.is_food_on_screen:
                self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                self.is_food_on_screen = True
            return self.position

        def set_food_on_screen(self, choice):
            self.is_food_on_screen = choice

# Initialize Game variables
score = 0
snake = Snake()
food = Food()
game_state = START

# Function to display text on the screen
def display_text(text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

# Function to draw the start page
def draw_start_page():
    screen.fill(WHITE)
    display_text("Snake Game", 36, WIDTH // 5, HEIGHT // 3, BLACK)
    display_text("Press SPACE to Start", 24, WIDTH // 5, (HEIGHT // 2) + 40, BLACK)

# Function to draw the game over screen
def draw_game_over():
    screen.fill(WHITE)
    display_text("Game Over", 36, WIDTH // 4, HEIGHT // 3, RED)
    display_text(f"Score: {score}", 24, WIDTH // 3, (HEIGHT // 2) + 40, BLACK)
    display_text("Press SPACE to Restart", 24, WIDTH // 5, (HEIGHT // 2) + 80, BLACK)
    display_text("Press Q to Quit", 24, WIDTH // 4, (HEIGHT // 2) + 120, BLACK)

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == START:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = PLAY
                score = 0
                snake = Snake()
                food = Food()

        if game_state == PLAY:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                if event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                if event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                if event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        if game_state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = PLAY
                    score = 0
                    snake = Snake()
                    food = Food()
                if event.key == pygame.K_q:
                    running = False

    if game_state == START:
        draw_start_page()

    if game_state == PLAY:
        food_position = food.spawn_food()
        if snake.move(food_position):
            food.set_food_on_screen(False)
            score += 1

        if snake.check_collision():
            game_state = GAME_OVER

        screen.fill(WHITE)
        for position in snake.get_body():
            pygame.draw.rect(
                screen, GREEN, (position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )
        pygame.draw.rect(
            screen, RED, (food_position[0] * GRID_SIZE, food_position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )
        display_text(f"Score: {score}", 24, 10, 10, BLACK)

    if game_state == GAME_OVER:
        draw_game_over()

    pygame.display.update()

    pygame.time.delay(150)  # Control game speed

# Quit Pygame
pygame.quit()
