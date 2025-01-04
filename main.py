import pygame
import sys

# Initialize pygame
pygame.init()

# Constraints of the game
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
MARKER_SIZE = 80
GRID_COLOR = (50, 50, 50)
CIRCLE_COLOR = (0, 0, 0)
CROSS_COLOR = (0, 0, 0)
BG_COLOR = (28, 170, 156)

# Create the screen for the game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
screen.fill(BG_COLOR)


# Start of Menu Code
def show_menu():
    screen.fill(BG_COLOR)
    font = pygame.font.Font(None, 60)
    title = font.render("Tic-Tac-Toe", True, (0, 0, 0))
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)

    font = pygame.font.Font(None, 40)
    multi_text = font.render("1. Multiplayer", True, (0, 0, 0))
    single_text = font.render("2. Play Against AI", True, (0, 0, 0))

    multi_rect = multi_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    single_rect = single_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))

    screen.blit(multi_text, multi_rect)
    screen.blit(single_text, single_rect)

    pygame.display.flip()

    # Wait for user to choose
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Multiplayer
                    return "multiplayer"
                elif event.key == pygame.K_2:  # Single Player
                    return "singleplayer"


# Show the menu and get the game mode
game_mode = show_menu()

screen.fill(BG_COLOR)
pygame.display.flip()


# Draw the grid
def draw_grid():
    for x in range(1, 3):
        pygame.draw.line(screen, GRID_COLOR, (0, x * HEIGHT // 3), (WIDTH, x * HEIGHT // 3), LINE_WIDTH)
        pygame.draw.line(screen, GRID_COLOR, (x * WIDTH // 3, 0), (x * WIDTH // 3, HEIGHT), LINE_WIDTH)


draw_grid()
pygame.display.flip()

# Define the state of the game, marks, and turn management
# Board state
board = [[None] * 3 for _ in range(3)]  # 3x3 grid of None

# Current player
current_player = "X"


def check_winner():
    # Check rows, columns, and diagonals for a win
    for row in board:
        if row.count(row[0]) == 3 and row[0] is not None:
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None


def is_draw():
    return all(all(row) for row in board) and check_winner() is None


# Takes the Players move and marks it on the board
def draw_marker(row, col, player):
    x = col * WIDTH // 3 + WIDTH // 6
    y = row * HEIGHT // 3 + HEIGHT // 6

    if player == "O":
        pygame.draw.circle(screen, CIRCLE_COLOR, (x, y), MARKER_SIZE, LINE_WIDTH)
    elif player == "X":
        # Draw an X
        offset = MARKER_SIZE // 2
        pygame.draw.line(screen, CROSS_COLOR, (x - offset, y - offset), (x + offset, y + offset), LINE_WIDTH)
        pygame.draw.line(screen, CROSS_COLOR, (x + offset, y - offset), (x - offset, y + offset), LINE_WIDTH)


# Handle the Input of the player
def get_cell(pos):
    x, y = pos
    col = x // (WIDTH // 3)
    row = y // (HEIGHT // 3)
    return row, col


# AI Logic (Minimax)
def minimax(board, depth, is_maximizing):
    winner = check_winner()
    if winner == "X":
        return -1
    if winner == "O":
        return 1
    if is_draw():
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score


def ai_move():
    best_score = float('-inf')
    move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                board[row][col] = "O"
                score = minimax(board, 0, False)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move


# Main game loop, integrating AI logic directly
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_mode == "multiplayer" or (game_mode == "singleplayer" and current_player == "X"):
                row, col = get_cell(event.pos)
                if board[row][col] is None:  # Place marker if cell is empty
                    board[row][col] = current_player
                    draw_marker(row, col, current_player)
                    winner = check_winner()
                    if winner:
                        print(f"{winner} wins!")
                        running = False
                    elif is_draw():
                        print("It's a draw!")
                        running = False
                    else:
                        current_player = "O" if current_player == "X" else "X"

    # Handle AI's move in "singleplayer" mode when it's AI's turn
    if game_mode == "singleplayer" and current_player == "O" and running:
        print("AI's turn")
        pygame.time.delay(500)  # Simulate AI thinking time
        row, col = ai_move()  # Get AI's move
        board[row][col] = "O"
        draw_marker(row, col, "O")
        print(f"AI placed marker at row {row}, col {col}")

        winner = check_winner()
        if winner:
            print(f"{winner} wins!")
            running = False
        elif is_draw():
            print("It's a draw!")
            running = False
        else:
            current_player = "X"  # Switch back to player for next turn

    pygame.display.flip()

pygame.quit()
sys.exit()

