import pygame
import heapq
import math

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 700))
clock = pygame.time.Clock()

# Colors
CHESSWHITE = (180, 146, 118)
CHESSBLACK = (80, 47, 30)
BLACK = (20, 20, 20)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Chessboard setup
BOARD_SIZE = 8
SQUARE_SIZE = 600 // BOARD_SIZE
board_graphic = pygame.image.load('assets/chessboard.jpg')
knight_graphic = pygame.image.load('assets/knight.png')
font = pygame.font.Font('assets/RobotoMono.ttf', 20)
user_text = ['Select a square to place the knight', 'Select another square to traverse to', 
             f'A* Implementation Cost: ', f'Dijkstra Implementation Cost: ', ' moves.']
user_input = 0

# Function to draw the chessboard
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = CHESSWHITE if (row + col) % 2 == 0 else CHESSBLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    screen.blit(font.render(user_text[user_input], True, 'white'), (85, 635))
    correct_board_graphic = pygame.transform.scale(board_graphic, (600,600))
    screen.blit(correct_board_graphic, (0,0))

# Positions for testing
knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
start_pos = (0, 0)
goal_pos = (7, 7)


# Function to draw the knight
def draw_knight(position, color):
    x, y = position
    correct_knight_graphic = pygame.transform.scale(knight_graphic, (75, 75))
    pygame.draw.circle(screen, color, (x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
    if color == RED:
        screen.blit(correct_knight_graphic, (x * SQUARE_SIZE + SQUARE_SIZE // 2 - 35, y * SQUARE_SIZE + SQUARE_SIZE // 2 - 40))


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

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current, start)
    path.append(start)
    path.reverse()
    return path, len(path)

# Dijkstra algorithm implementation
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

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current, start)
    path.append(start)
    path.reverse()
    return path, len(path)

# Main game loop
running = True
current_path = []
use_a_star = True  # Toggle between A* and Dijkstra

while running:
    screen.fill(BLACK)
    draw_board()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                user_input = 1
                # Switch between A* and Dijkstra
                use_a_star = not use_a_star
                if use_a_star:
                    user_input = 2
                    current_path, cost = a_star(start_pos, goal_pos)
                    screen.blit(font.render(user_text[user_input] + str(cost) + user_text[4], True, 'white'), (85, 635))
                else:
                    user_input  = 3
                    current_path, cost = dijkstra(start_pos, goal_pos)
                    screen.blit(font.render(user_text[user_input] + str(cost) + user_text[4], True, 'white'), (85, 635))

    # Draw knight and path
    if current_path:
        for pos in current_path:
            draw_knight(pos, GREEN)
        draw_knight(start_pos, RED)
        draw_knight(goal_pos, RED)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
