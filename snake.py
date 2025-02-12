import pygame
import sys
import random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        # Initialize the snake in a straight line with no overlaps
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)  # Move to the right initially
        self.direction_queue = []  # Queue to store direction changes
        self.new_block = False
        self.speed_timer_active = False  # Track if speed effect is active
        self.speed_timer_end_time = 0  # Time when the speed effect should end
        self.inverted_timer_active = False  # Track if inverted controls effect is active
        self.inverted_timer_end_time = 0  # Time when inverted controls should end

    def draw_snake(self):
        for block in self.body:
            xPos = int(block.x * cell_size)
            yPos = int(block.y * cell_size)
            block_rect = pygame.Rect(xPos, yPos, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 255), block_rect)

    def double_speed(self):
        pygame.time.set_timer(SCREEN_UPDATE, 75)  # Set double speed
        self.speed_timer_active = True  # Activate the speed timer
        self.speed_timer_end_time = pygame.time.get_ticks() + 10000  # Set the timer to 10 seconds

    def revert_speed(self):
        pygame.time.set_timer(SCREEN_UPDATE, 150)  # Revert back to normal speed
        self.speed_timer_active = False  # Deactivate the timer

    def revert_invertedControls(self):
        # Revert to normal controls (stop inverting the controls)
        self.inverted_timer_active = False

    def double_length(self):
        current_length = len(self.body)
        last_block = self.body[-1]
        tail_direction = last_block - self.body[-2]
        for _ in range(current_length):
            new_block = last_block + tail_direction
            self.body.append(new_block)
            last_block = new_block
        pygame.time.set_timer(SCREEN_UPDATE, 150)

    def inverted_controls(self):
        # Activate the inverted controls timer
        self.inverted_timer_active = True
        self.inverted_timer_end_time = pygame.time.get_ticks() + 10000  # Set timer for 10 seconds

    def end_game(self):
        screen.fill((175, 215, 70))
        fail_surface = score_font.render('Dont gamble!', True, (56, 74, 12))
        fail_rect = fail_surface.get_rect(center=(cell_count * cell_size // 2, cell_count * cell_size // 2))
        screen.blit(fail_surface, fail_rect)
        pygame.display.update()
        pygame.time.wait(2000)  # Wait for 2 seconds before closing
        pygame.quit()
        sys.exit()

    def move_snake(self):
        # Apply all valid direction changes from the queue
        if self.direction_queue:
            new_direction = self.direction_queue.pop(0)
            # Avoid reversing into itself
            if new_direction.x != -self.direction.x or new_direction.y != -self.direction.y:
                self.direction = new_direction

        # Update snake body
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]

        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class FRUKT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (200, 0, 0), fruit_rect)

    def randomize(self, snake=None):
        while True:
            self.x = random.randint(0, cell_count - 1)
            self.y = random.randint(0, cell_count - 1)
            self.pos = Vector2(self.x, self.y)

            # Check if the fruit's position is on the snake's body
            if snake is None or self.pos not in snake.body:
                break


class SpecialBlock:
    def __init__(self):
        self.visible = False  # Special block is initially not visible
        self.randomize()

    def randomize(self, snake=None):
        self.effect = random.choice(['inverted_controls', 'end_game', 'double_speed', 'double_length'])  # Randomly select the effect
        while True:
            self.x = random.randint(0, cell_count - 1)
            self.y = random.randint(0, cell_count - 1)
            self.pos = Vector2(self.x, self.y)

            # Ensure the block doesn't spawn on the snake's body
            if snake is None or self.pos not in snake.body:
                break

    def draw_block(self):
        if self.visible:
            if self.effect == 'inverted_controls':
                color = (0,0,255)
            elif self.effect == 'double_speed':
                color = (255,255,0)
            elif self.effect == 'double_length' or self.effect == 'end_game':
                color = (0,255,0)
            block_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, color, block_rect)

    def apply_effect(self, snake):
        if self.effect == 'inverted_controls':
            snake.inverted_controls()
        elif self.effect == 'double_speed':
            snake.double_speed()
        elif self.effect == 'double_length':
            snake.double_length()
        elif self.effect == 'end_game':
            snake.end_game()


def check_collision():
    global score  # Use the global score variable
    if snake.body[0] == fruit.pos:
        fruit.randomize(snake)  # Pass the snake object to check its body
        snake.add_block()
        score += 1  # Increase the score when snake eats a fruit

    if special_block.visible and snake.body[0] == special_block.pos:
        special_block.visible = False  # Hide the block after collision
        special_block.apply_effect(snake)


def check_fail():
    # Check if snake hits the wall
    if not 0 <= snake.body[0].x < cell_count or not 0 <= snake.body[0].y < cell_count:
        print("Snake hit the wall")
        return True
    # Check if snake hits itself
    for block in snake.body[1:]:
        if block == snake.body[0]:
            print("Snake hit itself")
            return True
    return False


def draw_score():
    score_surface = score_font.render(f'Score: {score}', True, (56, 74, 12))
    score_rect = score_surface.get_rect(center=(cell_size * 1.5, cell_size * 0.5))
    screen.blit(score_surface, score_rect)


color1 = (170, 215, 81)
color2 = (162, 209, 73)


def draw_background():
    for row in range(cell_count):
        for col in range(cell_count):
            color = color1 if (row + col) % 2 == 0 else color2
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)


# Initialize Pygame
pygame.init()

cell_size = 40
cell_count = 15
screen = pygame.display.set_mode((cell_count * cell_size, cell_count * cell_size))
clock = pygame.time.Clock()

# Initialize the snake, fruit, and special block
snake = SNAKE()
fruit = FRUKT()
special_block = SpecialBlock()

fruit.randomize(snake)  # Ensure the fruit spawns in a valid position
special_block.randomize(snake)

# Initialize the score
score = len(snake.body)

# Font for displaying the score
score_font = pygame.font.Font(None, 36)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  # Update every 150 milliseconds

SPECIAL_BLOCK_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(SPECIAL_BLOCK_TIMER, 20000)  # Trigger every 20 seconds

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            # Move the snake based on the timer event
            snake.move_snake()
        if event.type == SPECIAL_BLOCK_TIMER:
            # Show and randomize the special block every 20 seconds
            special_block.visible = True
            special_block.randomize(snake)
        if event.type == pygame.KEYDOWN:
            # Check if inverted controls are active
            if snake.inverted_timer_active:
                # Inverted controls logic
                if event.key == pygame.K_UP:
                    if snake.direction != Vector2(0, -1):
                        snake.direction_queue.append(Vector2(0, 1))  # Inverted: up moves down
                if event.key == pygame.K_DOWN:
                    if snake.direction != Vector2(0, 1):
                        snake.direction_queue.append(Vector2(0, -1))  # Inverted: down moves up
                if event.key == pygame.K_RIGHT:
                    if snake.direction != Vector2(1, 0):
                        snake.direction_queue.append(Vector2(-1, 0))  # Inverted: right moves left
                if event.key == pygame.K_LEFT:
                    if snake.direction != Vector2(-1, 0):
                        snake.direction_queue.append(Vector2(1, 0))  # Inverted: left moves right
            else:
                # Normal controls logic
                if event.key == pygame.K_UP:
                    if snake.direction != Vector2(0, 1):
                        snake.direction_queue.append(Vector2(0, -1))
                if event.key == pygame.K_DOWN:
                    if snake.direction != Vector2(0, -1):
                        snake.direction_queue.append(Vector2(0, 1))
                if event.key == pygame.K_RIGHT:
                    if snake.direction != Vector2(-1, 0):
                        snake.direction_queue.append(Vector2(1, 0))
                if event.key == pygame.K_LEFT:
                    if snake.direction != Vector2(1, 0):
                        snake.direction_queue.append(Vector2(-1, 0))

            # Limit the direction queue size to avoid overfilling
            if len(snake.direction_queue) > 3:
                snake.direction_queue = snake.direction_queue[:3]

    # Check if the speed effect has expired
    if snake.speed_timer_active and pygame.time.get_ticks() > snake.speed_timer_end_time:
        snake.revert_speed()

    # Check if the inverted controls effect has expired
    if snake.inverted_timer_active and pygame.time.get_ticks() > snake.inverted_timer_end_time:
        snake.revert_invertedControls()

    # Check for collisions and failures
    check_collision()
    if check_fail():
        screen.fill((175, 215, 70))
        fail_surface = score_font.render('You hit the wall! Game Over!', True, (56, 74, 12))
        fail_rect = fail_surface.get_rect(center=(cell_count * cell_size // 2, cell_count * cell_size // 2))
        screen.blit(fail_surface, fail_rect)
        pygame.display.update()
        pygame.time.wait(2000)  # Wait for 2 seconds before closing
        pygame.quit()
        sys.exit()

    draw_background()  # Draw the checkerboard background
    fruit.draw_fruit()
    snake.draw_snake()
    special_block.draw_block()  # Draw the special block if visible
    draw_score()  # Draw the score on the screen
    pygame.display.update()

    clock.tick(60)  # Cap the frame rate to 60 FPS for smooth renderings
