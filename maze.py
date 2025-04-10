import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 21, 21  # Ensuring odd dimensions for proper maze generation
CELL_SIZE = WIDTH // COLS
WHITE, BLACK, BLUE, RED, GREEN = (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Maze grid
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]

# Player position
player_x, player_y = 0, 0
# End point position
end_x, end_y = COLS - 1, ROWS - 1

def generate_maze():
    stack = [(0, 0)]
    visited = set()
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Move by 2 cells to create walls between paths

    # Mark all cells as walls initially
    for row in range(ROWS):
        for col in range(COLS):
            maze[row][col] = 1  # 1 = wall

    maze[0][0] = 0  # Start position
    maze[ROWS-1][COLS-1] = 0  # End position

    while stack:
        x, y = stack[-1]
        visited.add((x, y))

        # Get valid neighbors
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and (nx, ny) not in visited:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            mx, my = (x + nx) // 2, (y + ny) // 2  # Midpoint to remove wall
            maze[mx][my] = 0  # Remove wall
            maze[nx][ny] = 0  # Mark new path
            stack.append((nx, ny))
        else:
            stack.pop()

def draw_maze():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw player
    pygame.draw.rect(screen, RED, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw end point
    pygame.draw.rect(screen, GREEN, (end_x * CELL_SIZE, end_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()  # Force update

def move_player(dx, dy):
    global player_x, player_y
    new_x, new_y = player_x + dx, player_y + dy
    
    # Check if the new position is within bounds and not a wall
    if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
        player_x, player_y = new_x, new_y

def main():
    global player_x, player_y
    generate_maze()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    move_player(0, 1)
                elif event.key == pygame.K_LEFT:
                    move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    move_player(1, 0)
        
        draw_maze()
        
        # Check if player reaches the end point
        if player_x == end_x and player_y == end_y:
            print("Congratulations! You solved the maze!")
            pygame.quit()
            return

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    # Set initial player position
    player_x, player_y = 0, 0
    # Generate maze
    generate_maze()
    # Draw the initial maze
    draw_maze()
    # Start the game loop
    main()