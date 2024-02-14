import pygame
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Escape")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Player attributes
player_size = 20
player_x = 50
player_y = 50
player_speed = 20  # Increase speed for better visibility

# Maze attributes
maze_width = 20
maze_height = 15
maze_block_size = 40

# Maze generation using recursive backtracking algorithm
def generate_maze(width, height):
    maze = [[0 for _ in range(width)] for _ in range(height)]

    def create_maze(x, y):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + 2*dx, y + 2*dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 0:
                maze[y + dy][x + dx] = 1
                maze[ny][nx] = 1
                create_maze(nx, ny)

    create_maze(random.randint(0, width // 2 - 1) * 2, random.randint(0, height // 2 - 1) * 2)
    return maze

# Generate an escapable maze
maze = generate_maze(maze_width, maze_height)
maze[0][1] = 0
maze[maze_height-1][maze_width-2] = 0

# Introductory screen
intro = True
while intro:
    screen.fill(black)
    font = pygame.font.SysFont(None, 30)
    text = font.render("A MIGHTY FRIEND IS TRAPPED. YOU ARE HIS ONLY HOPE. HELP YOUR FRIEND ESCAPE HIS CHOICE!", True, white)
    screen.blit(text, (50, height/2))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            intro = False

# Main game loop
running = True
while running:
    screen.fill(white)

    # Handling events for player movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and maze[int((player_y - player_speed) / maze_block_size)][int(player_x / maze_block_size)] == 0:
                player_y -= player_speed
            elif event.key == pygame.K_DOWN and maze[int((player_y + player_speed + player_size) / maze_block_size)][int(player_x / maze_block_size)] == 0:
                player_y += player_speed
            elif event.key == pygame.K_LEFT and maze[int(player_y / maze_block_size)][int((player_x - player_speed) / maze_block_size)] == 0:
                player_x -= player_speed
            elif event.key == pygame.K_RIGHT and maze[int(player_y / maze_block_size)][int((player_x + player_speed + player_size) / maze_block_size)] == 0:
                player_x += player_speed

    # Draw the maze
    for i in range(maze_height):
        for j in range(maze_width):
            if maze[i][j]:
                pygame.draw.rect(screen, black, (j * maze_block_size, i * maze_block_size, maze_block_size, maze_block_size))

    # Draw the player
    pygame.draw.rect(screen, red, (player_x, player_y, player_size, player_size))

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(10)  # Reduce tick for smoother movement

pygame.quit()
