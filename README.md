# Tetris Game

This is a simple Tetris game implemented in Python using the Pygame library. The game features a playable grid, falling tetrominoes (blocks), scoring based on clearing lines, and increasing difficulty as the score increases.

## Table of Contents
- [How the Code Works](#how-the-code-works)
  - [Initialization](#initialization)
  - [Tetromino Shapes and Colors](#tetromino-shapes-and-colors)
  - [Pygame Setup](#pygame-setup)
  - [Grid Setup](#grid-setup)
  - [Drawing Functions](#drawing-functions)
  - [Tetromino Movement and Rotation](#tetromino-movement-and-rotation)
  - [Game Screens](#game-screens)
  - [Main Game Loop](#main-game-loop)
  - [Event Handling](#event-handling)
- [Instructions](#instructions)
  - [How to Use the Code](#how-to-use-the-code)
  - [How to Play](#how-to-play)
  - [Scoring](#scoring)
- [Features](#features)
- [Requirements](#requirements)

## How the Code Works

### Initialization

- The code starts by importing the necessary libraries: 'pygame' and 'random'.
- Pygame is initialized using 'pygame.init()'.
- Screen dimensions and block size are defined:
  ```python
  screen_width = 300
  screen_height = 600
  block_size = 30
  ```

#### * Colors are defined for the blocks and the grid background:
```python
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
```

### Tetromino Shapes and Colors

#### * Tetromino shapes are defined as a list of 2D arrays, where each array represents a block shape:
```python
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]
```

#### * Corresponding colors for each shape are defined in 'shape_colors':
```python
shape_colors = [cyan, yellow, magenta, red, blue, green, white]
```

### Pygame Setup

#### * A Pygame screen is created using 'pygame.display.set_mode()':
```python
screen = pygame.display.set_mode((screen_width, screen_height))
```

#### * The screen title is set using 'pygame.display.set_caption()':
```python
pygame.display.set_caption('Tetris')
```

### Grid Setup

#### * The grid is defined based on the screen dimensions and block size:
```python
grid_width = screen_width // block_size
grid_height = screen_height // block_size
```

#### * An empty grid is created using a function 'create_grid()':
```python
def create_grid():
    return [[black for _ in range(grid_width)] for _ in range(grid_height)]
grid = create_grid()
```

### Drawing Functions

#### * 'draw_block()': Draws a single block with a black border:
```python
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, pygame.Rect(x * block_size, y * block_size, block_size, block_size))
    pygame.draw.rect(screen, black, pygame.Rect(x * block_size, y * block_size, block_size, block_size), 1)
```

#### * 'draw_grid()': Draws the entire grid:
```python
def draw_grid():
    for y in range(grid_height):
        for x in range(grid_width):
            draw_block(x, y, grid[y][x])
```

### Tetromino Movement and Rotation

#### * 'valid_position()': Checks if a given position for a shape is valid (i.e., within bounds and not colliding with other blocks):
```python
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
```

#### * 'join_shape()': Joins a shape to the grid at a specified position:
```python
def join_shape(shape, offset, color):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + off_y][x + off_x] = color
```

#### * 'clear_lines()': Clears complete lines from the grid and returns the number of lines cleared:
```python
def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == black for cell in row)]
    lines_cleared = grid_height - len(new_grid)
    grid = [[black for _ in range(grid_width)] for _ in range(lines_cleared)] + new_grid
    return lines_cleared
```

#### * 'rotate()': Rotates a shape:
```python
def rotate(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]
```

### Game Screens

#### * 'show_title_screen()': Displays the title screen with instructions:
```python
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

    start_text = font.render("Press Enter to start the game", True, white)
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2 + len(instructions) * 30 + 40))

    pygame.display.flip()
```

#### * 'show_pause_screen()': Displays the pause screen:
```python
def show_pause_screen():
    font = pygame.font.SysFont(None, 55)
    pause_text = font.render('Pause', True, white)
    screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2 - pause_text.get_height() // 2))
    pygame.display.flip()
```

#### * 'show_game_over_screen()': Displays the game over screen with the final score and options to restart or exit:
```python
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
```

### Main Game Loop

#### * The main game loop is contained within the 'game()' function:
```python
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
```

### Event Handling

#### * The event handling loop listens for keyboard events to control the game:
```python
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
```

## Instructions

### How to Use the Code

1. Ensure you have Python installed on your system.
2. Install Pygame by running:
    ```python
    pip install pygame
    ```
3. Save the provided code in a file named 'tetris.py'.
4. Run the game by executing:
    ```python
    python tetris.py
    ```

### How to Play
* **Move Left**: Press the Left Arrow key.
* **Move Right**: Press the Right Arrow key.
* **Move Down**: Press the Down Arrow key.
* **Rotate**: Press the Up Arrow key.
* **Pause/Unpause**: Press the Spacebar.
* **Start the Game**: Press Enter on the title screen.
* **Restart the Game**: Press Enter on the game over screen.
* **Exit the Game**: Press ESC on the game over screen.

### Scoring
* The score increases based on the number of lines cleared simultaneously.
* The formula is: 'score += lines_cleared * 10 * lines_cleared'.
* As the score increases, the speed of the falling tetrominoes increases, making the game progressively harder.

### Features
* Playable Tetris game with keyboard controls.
* Increasing difficulty based on score.
* Pause and resume functionality.
* Title screen with instructions.
* Game over screen with the final score and options to restart or exit.

### Requirements

* Python 3.x
* Pygame library ('pip install pygame')

---

## Enjoy playing Tetris!