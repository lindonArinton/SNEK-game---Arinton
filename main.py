import pygame
import time
import random
import json
import os

# Initialize Pygame
pygame.init()

#colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (139, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 128, 0)
BLUE = (50, 153, 213)
PURPLE = (128, 0, 128)

# Set the screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game by: Arinton')

# Set the clock and game parameters
clock = pygame.time.Clock()
SNAKE_BLOCK = 15
SNAKE_SPEED = 15

# Fonts
FONT_STYLE = pygame.font.SysFont("bahnschrift", 30)
SCORE_FONT = pygame.font.SysFont("comicsansms", 40)
TITLE_FONT = pygame.font.SysFont("comicsansms", 70)


LEADERBOARD_FILE = 'leaderboard.json'

def load_leaderboard():
    """Load leaderboard from a JSON file."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []

    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_leaderboard(leaderboard):
    """Save leaderboard to a JSON file."""
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    leaderboard = leaderboard[:10]  # Keep top 10 scores

    try:
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(leaderboard, f, indent=4)
    except IOError:
        print("Error saving leaderboard.")

def add_to_leaderboard(score):
    """Add a score to the leaderboard and save it."""
    leaderboard = load_leaderboard()

    name = get_player_name()

    leaderboard.append({
        'name': name,
        'score': score,
        'date': time.strftime("%Y-%m-%d %H:%M:%S")
    })

    save_leaderboard(leaderboard)

def get_player_name():
    """Get player name input."""
    name = ""
    input_active = True

    # Create input screen
    screen.fill(BLACK)  # Set background to black
    display_message("Enter Your Name", WHITE, -50)  # Text color to white
    pygame.display.update()

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    # Limit name length and allow only alphanumeric characters
                    if len(name) < 10 and event.unicode.isalnum():
                        name += event.unicode

                # Redraw input screen
                screen.fill(BLACK)  # Set background to black
                display_message("Enter Your Name", WHITE, -50)  # Text color to white
                name_surface = FONT_STYLE.render(name, True, WHITE)  # Text color to white
                name_rect = name_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))
                screen.blit(name_surface, name_rect)
                pygame.display.update()

    return name if name else "Anonymous"

def display_leaderboard():
    """Display the leaderboard screen."""
    leaderboard = load_leaderboard()

    while True:
        screen.fill(BLACK)  # Set background to black

        # Title
        title_text = TITLE_FONT.render('Leaderboard', True, WHITE)  # Text color to white
        title_rect = title_text.get_rect(center=(WIDTH / 2, 50))
        screen.blit(title_text, title_rect)

        # Display top scores
        for i, entry in enumerate(leaderboard, 1):
            text = f"{i}. {entry['name']} - {entry['score']} (Date: {entry['date']})"
            score_text = FONT_STYLE.render(text, True, WHITE)  # Text color to white
            score_rect = score_text.get_rect(center=(WIDTH / 2, 150 + i * 30))
            screen.blit(score_text, score_rect)

        # Instructions
        back_text = FONT_STYLE.render("Press SPACE to go back", True, WHITE)  # Text color to white
        back_rect = back_text.get_rect(center=(WIDTH / 2, HEIGHT - 50))
        screen.blit(back_text, back_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Go back to the main menu
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def display_score(score, color=WHITE):  # Default text color to white
    """Render the current score"""
    value = SCORE_FONT.render(f"Score: {score}", True, color)
    screen.blit(value, [10, 10])

def draw_snake(snake_block, snake_list, color=GREEN):
    """Draw the snake with a more interesting style"""
    for i, x in enumerate(snake_list):
        segment_color = (0, min(255, 100 + i * 5), 0) if color == GREEN else color
        pygame.draw.rect(screen, segment_color, [x[0], x[1], snake_block, snake_block])
        pygame.draw.rect(screen, DARK_GREEN, [x[0], x[1], snake_block, snake_block], 1)

def display_message(msg, color, y_displace=0):
    """Display game messages with more flexibility"""
    mesg = FONT_STYLE.render(msg, True, color)
    text_rect = mesg.get_rect(center=(WIDTH / 2, HEIGHT / 2 + y_displace))
    screen.blit(mesg, text_rect)

def is_collision(x1, y1, foodx, foody, snake_block):
    """Check if there's a collision between snake head and food"""
    return (x1 < foodx + snake_block and
            x1 + snake_block > foodx and
            y1 < foody + snake_block and
            y1 + snake_block > foody)

def game_intro():
    """Create an intro screen for the game"""
    intro = True
    while intro:
        screen.fill(BLACK)  # Set background to black
        title_text = TITLE_FONT.render('Snake Game', True, WHITE)  # Text color to white
        title_rect = title_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        screen.blit(title_text, title_rect)

        display_message("Press SPACE to Play", WHITE, 100)  # Text color to white
        display_message("Press L for Leaderboard", WHITE, 150)  # Text color to white
        display_message("Press Q to Quit", WHITE, 200)  # Text color to white

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_l:
                    display_leaderboard()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def gameLoop():
    """Main game loop"""
    game_over = False
    game_close = False

    # Initial snake position
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    # Snake tracking
    snake_List = []
    Length_of_snake = 1

    # Food placement
    foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 15.0) * 15.0
    foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 15.0) * 15.0

    while not game_over:
        # Game over screen
        while game_close:
            screen.fill(BLACK)  # Set background to black
            display_message("You Lost!", RED, -50)  # Text color to red
            display_message("Press C-Play Again or Q-Quit", WHITE, 0)  # Text color to white
            display_score(Length_of_snake - 1, WHITE)  # Score color to white

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # Boundary checks
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        # Move snake
        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)  # Set background to black

        # Draw food
        pygame.draw.rect(screen, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        # Snake head and body tracking
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Self-collision check
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Draw snake
        draw_snake(SNAKE_BLOCK, snake_List)
        display_score(Length_of_snake - 1, WHITE)  # Score color to white

        pygame.display.update()

        # Food eating mechanics
        if is_collision(x1, y1, foodx, foody, SNAKE_BLOCK):
            # Random food placement
            foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 15.0) * 15.0
            foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 15.0) * 15.0
            Length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    # Add score to leaderboard
    add_to_leaderboard(Length_of_snake - 1)
    pygame.quit()
    quit()

# Start with intro screen
game_intro()
gameLoop()
