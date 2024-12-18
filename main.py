import pygame
import heapq
import math

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((600, 700))
clock = pygame.time.Clock()
pygame.display.set_caption("Knight's Travail")

# Define colors used in the game
CHESSWHITE = (180, 146, 118)
CHESSBLACK = (80, 47, 30)
BLACK = (20, 20, 20)
GRAY = (40, 40, 40, 128)
RED = (255, 0, 0)
HIGHLIGHT = (255, 255, 255)

# Constants for chessboard setup
BOARD_SIZE = 8
SQUARE_SIZE = 600 // BOARD_SIZE

# Load assets for graphics and fonts
board_graphic = pygame.image.load('assets/chessboard.jpg')
resized_board_graphic = pygame.transform.scale(board_graphic, (600,600))

knight_graphic = pygame.image.load('assets/knight.png')
resized_knight_graphic = pygame.transform.scale(knight_graphic, (75, 75))

pawn_graphic = pygame.image.load('assets/pawn.png')
resized_pawn_graphic = pygame.transform.scale(pawn_graphic, (65, 65))

font = pygame.font.Font('assets/RobotoMono.ttf', 20)

pygame.display.set_icon(knight_graphic)

# Text displayed for instructions and results
user_text = [
    'Select a square to place the knight',
    'Select another square to traverse to',
    '',  # A* result
    '',   # Dijkstra result
    'Press Left Shift to reset board'
]

# Function to render the chessboard and display user instructions
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = CHESSWHITE if (row + col) % 2 == 0 else CHESSBLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    font = pygame.font.Font('assets/RobotoMono.ttf', 12)
    screen.blit(font.render(user_text[4], True, 'white'), (5, 600)) # Left shift to reset board te
    font = pygame.font.Font('assets/RobotoMono.ttf', 20)
    
    # Display appropriate instructions or results based on the game state
    if current_path:
        text_to_show = user_text[2] if use_a_star else user_text[3]
        screen.blit(font.render(text_to_show, True, 'white'), (85, 635))
    else:
        screen.blit(font.render(user_text[0] if start_pos is None else user_text[1], True, 'white'), (85, 635))

    # Draw the scaled chessboard graphic over the board
    screen.blit(resized_board_graphic, (0, 0))

# Predefined moves for a knight in chess
knight_moves = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

# Variables for the starting position and goal position
start_pos = None
goal_pos = None


# Function to draw the knight
def draw_knight(position, color, move = 0):
    x, y = position

    if position == start_pos or position == goal_pos:
        pygame.draw.circle(screen, color, (x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 10)
        screen.blit(font.render(str(move), True, 'white'), (x * SQUARE_SIZE + SQUARE_SIZE // 2 - 6, y * SQUARE_SIZE + SQUARE_SIZE // 2 - 15))
        screen.blit(resized_knight_graphic, (x * SQUARE_SIZE + SQUARE_SIZE // 2 - 35, y * SQUARE_SIZE + SQUARE_SIZE // 2 - 40))
    else:
        pygame.draw.circle(screen, color, (x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 4)
        screen.blit(font.render(str(move), True, 'white'), (x * SQUARE_SIZE + SQUARE_SIZE // 2 - 6, y * SQUARE_SIZE + SQUARE_SIZE // 2 - 15))


# A* algorithm implementation
def a_star(start, goal):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            break

        for move in knight_moves:
            neighbor = (current[0] + move[0], current[1] + move[1])
            if 0 <= neighbor[0] < BOARD_SIZE and 0 <= neighbor[1] < BOARD_SIZE:
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (priority, neighbor))
                    came_from[neighbor] = current

    # Reconstruct the path from the goal to the start
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current, start)
    path.append(start)
    path.reverse()
    return path, len(path) - 1

# Dijkstra's algorithm for finding the shortest path
def dijkstra(start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_list:
        current_cost, current = heapq.heappop(open_list)

        if current == goal:
            break

        for move in knight_moves:
            neighbor = (current[0] + move[0], current[1] + move[1])
            if 0 <= neighbor[0] < BOARD_SIZE and 0 <= neighbor[1] < BOARD_SIZE:
                new_cost = current_cost + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(open_list, (new_cost, neighbor))
                    came_from[neighbor] = current

    # Reconstruct the path from the goal to the start
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current, start)
    path.append(start)
    path.reverse()
    return path, len(path) - 1

# Main game loop to handle interactions and rendering
running = True
current_path = []
use_a_star = True  # Toggle between A* and Dijkstra

while running:
    screen.fill(BLACK)
    draw_board()

    # Process events such as mouse clicks and key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            mouse_x, mouse_y = event.pos
            if mouse_y > 600:
                continue
            col = mouse_x // SQUARE_SIZE
            row = mouse_y // SQUARE_SIZE

            if start_pos is None:
                start_pos = (col, row)
            elif goal_pos is None:
                goal_pos = (col, row)
                

                if use_a_star:
                    current_path, cost = a_star(start_pos, goal_pos)
                    user_text[2] = f'A* Implementation Cost: {cost} moves'
                else:
                    current_path, cost = dijkstra(start_pos, goal_pos)
                    user_text[3] = f'Dijkstra Implementation Cost: {cost} moves'

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                # Reset the board and positions
                start_pos = None
                goal_pos = None
                current_path = []
                user_text[0] = 'Select a square to place the knight'
                user_text[2] = ''
                user_text[3] = ''
            elif event.key == pygame.K_SPACE:
                # Toggle between A* and Dijkstra algorithms
                use_a_star = not use_a_star
                if start_pos and goal_pos:
                    if use_a_star:
                        current_path, cost = a_star(start_pos, goal_pos)
                        user_text[2] = f'A* Implementation Cost: {cost} moves'
                    else:
                        current_path, cost = dijkstra(start_pos, goal_pos)
                        user_text[3] = f'Dijkstra Implementation Cost: {cost} moves'

    # Highlight the square under the mouse
    if start_pos is None or goal_pos is None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > 600:
            continue
        col = mouse_x // SQUARE_SIZE
        row = mouse_y // SQUARE_SIZE
        pygame.draw.rect(screen, HIGHLIGHT, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
    
    if start_pos is not None:
        start_col, start_row = start_pos
        pygame.draw.rect(screen, HIGHLIGHT, (start_col * SQUARE_SIZE, start_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

    # Render the knight and the calculated path
    if current_path:
        move = 0
        screen.blit(resized_board_graphic, (0, 0))
        for pos in current_path:
            draw_knight(pos, GRAY, move)
            move += 1
        draw_knight(start_pos, RED)
        draw_knight(goal_pos, RED)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
