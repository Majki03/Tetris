import pygame
import random

# Initialize Pygame
pygame.init()

# Set the screen dimensions and block size
screen_width = 350
screen_height = 700
block_size = 25

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)

# Define the shapes of the blocks
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# Define the colors of the blocks
shape_colors = [cyan, yellow, magenta, red, blue, green, white]

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

# Define the grid
grid_width = screen_width // block_size
grid_height = screen_height // block_size

# Create an empty grid
def create_grid():
    return [[black for _ in range(grid_width)] for _ in range(grid_height)]

grid = create_grid()

# Function to draw a block with a black border
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, pygame.Rect(x * block_size, y * block_size, block_size, block_size))
    pygame.draw.rect(screen, black, pygame.Rect(x * block_size, y * block_size, block_size, block_size), 1)

# Function to draw the grid
def draw_grid():
    for y in range(grid_height):
        for x in range(grid_width):
            draw_block(x, y, grid[y][x])

# Function to check if a position is valid
def valid_position(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                try:
                    if y + off_y < 0 or x + off_x < 0:
                        return False
                    if grid[y + off_y][x + off_x] != black:
                        return False
                except IndexError:
                    return False
    return True

# Function to join a shape to the grid
def join_shape(shape, offset, color):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + off_y][x + off_x] = color

# Function to clear lines and return the number of lines cleared
def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == black for cell in row)]
    lines_cleared = grid_height - len(new_grid)
    grid = [[black for _ in range(grid_width)] for _ in range(lines_cleared)] + new_grid
    return lines_cleared

# Function to rotate a shape
def rotate(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

# Function to display the title screen
def show_title_screen():
    screen.fill(black)
    font = pygame.font.SysFont(None, 55)
    title_text = font.render('Tetris', True, white)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))

    font = pygame.font.SysFont(None, 25)
    instructions = [
        "Left Arrow: Move Left",
        "Right Arrow: Move Right",
        "Down Arrow: Move Down",
        "Up Arrow: Rotate",
        "Spacebar: Pause/Unpause"
    ]
    for i, line in enumerate(instructions):
        instruction_text = font.render(line, True, white)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, screen_height // 2 + i * 30))

    font = pygame.font.SysFont(None, 25)
    start_text = font.render("Press Enter to start the game", True, white)
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2 + len(instructions) * 30 + 40))

    pygame.display.flip()

# Function to display the pause screen
def show_pause_screen():
    font = pygame.font.SysFont(None, 55)
    pause_text = font.render('Pause', True, white)
    screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2 - pause_text.get_height() // 2))
    pygame.display.flip()

# Function to display the game over screen
def show_game_over_screen(score):
    screen.fill(black)
    font = pygame.font.SysFont(None, 55)
    game_over_text = font.render('Game Over', True, white)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 4))

    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 3 + 40))

    font = pygame.font.SysFont(None, 25)
    try_again_text = font.render("Press Enter to Try Again", True, white)
    screen.blit(try_again_text, (screen_width // 2 - try_again_text.get_width() // 2, screen_height // 2))

    esc_text = font.render("Press ESC to Close the Game", True, white)
    screen.blit(esc_text, (screen_width // 2 - esc_text.get_width() // 2, screen_height // 2 + 30))

    pygame.display.flip()

# Main game loop
def game():
    global grid
    clock = pygame.time.Clock()
    last_move_down_time = pygame.time.get_ticks()
    current_shape = random.choice(shapes)
    current_color = shape_colors[shapes.index(current_shape)]
    current_position = [grid_width // 2 - len(current_shape[0]) // 2, 0]
    paused = False
    game_over = False
    score = 0
    move_down_time = 500
    move_side_time = 100  # Time interval for moving left or right when key is held down
    last_move_side_time = 0

    while True:
        if game_over:
            show_game_over_screen(score)
        elif not paused:
            screen.fill(black)
            draw_grid()

            # Move shape down automatically
            if pygame.time.get_ticks() - last_move_down_time > move_down_time:
                new_position = [current_position[0], current_position[1] + 1]
                if valid_position(current_shape, new_position):
                    current_position = new_position
                else:
                    join_shape(current_shape, current_position, current_color)
                    lines_cleared = clear_lines()
                    if lines_cleared > 0:
                        score += lines_cleared * 10 * lines_cleared  # Increase score with multiplier
                        # Increase speed after every 100 points
                        move_down_time = max(100, 500 - (score // 100) * 50)
                    current_shape = random.choice(shapes)
                    current_color = shape_colors[shapes.index(current_shape)]
                    current_position = [grid_width // 2 - len(current_shape[0]) // 2, 0]
                    if not valid_position(current_shape, current_position):
                        game_over = True
                last_move_down_time = pygame.time.get_ticks()

            # Draw the current shape
            for y, row in enumerate(current_shape):
                for x, cell in enumerate(row):
                    if cell:
                        draw_block(current_position[0] + x, current_position[1] + y, current_color)

            # Display the score
            font = pygame.font.SysFont(None, 35)
            score_text = font.render(f"Score: {score}", True, white)
            screen.blit(score_text, (10, 10))

            # Update the display
            pygame.display.flip()
            clock.tick(30)
        else:
            show_pause_screen()

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if not paused and not game_over:
            if keys[pygame.K_LEFT] and current_time - last_move_side_time > move_side_time:
                new_position = [current_position[0] - 1, current_position[1]]
                if valid_position(current_shape, new_position):
                    current_position = new_position
                last_move_side_time = current_time

            if keys[pygame.K_RIGHT] and current_time - last_move_side_time > move_side_time:
                new_position = [current_position[0] + 1, current_position[1]]
                if valid_position(current_shape, new_position):
                    current_position = new_position
                last_move_side_time = current_time

            if keys[pygame.K_DOWN] and current_time - last_move_side_time > move_side_time:
                new_position = [current_position[0], current_position[1] + 1]
                if valid_position(current_shape, new_position):
                    current_position = new_position
                last_move_side_time = current_time

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not paused and not game_over:
                    rotated_shape = rotate(current_shape)
                    if valid_position(rotated_shape, current_position):
                        current_shape = rotated_shape
                elif event.key == pygame.K_SPACE and not game_over:
                    paused = not paused
                    if paused:
                        show_pause_screen()
                elif event.key == pygame.K_RETURN and game_over:
                    grid = create_grid()
                    game_over = False
                    current_shape = random.choice(shapes)
                    current_color = shape_colors[shapes.index(current_shape)]
                    current_position = [grid_width // 2 - len(current_shape[0]) // 2, 0]
                    score = 0
                    move_down_time = 500
                elif event.key == pygame.K_ESCAPE and game_over:
                    pygame.quit()
                    return

# Show title screen and wait for Enter key to start
show_title_screen()
start_game = False
while not start_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start_game = True

# Start the game
game()