import random

def suggest_safe_move(board):
    # Given the current state of the Minesweeper board, suggest a safe move.
    safe_moves = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == ' ':
                # Check if revealing this cell is safe based on neighboring mines.
                if is_safe_move(board, row, col):
                    safe_moves.append((row, col))
    if safe_moves:
        return random.choice(safe_moves)
    else:
        return None  # No safe moves available

def is_safe_move(board, row, col):
    # Check if revealing the specified cell is safe based on neighboring mines.
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
                if board[nr][nc] == 'M':
                    return False
    return True


def initialize_board(rows, cols, num_mines):
    # Create an empty board with '0' representing untouched cells
    board = [['0' for _ in range(cols)] for _ in range(rows)]
    
    # Place mines randomly on the board
    placed_mines = 0
    while placed_mines < num_mines:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        if board[row][col] != 'M':
            board[row][col] = 'M'
            placed_mines += 1
            
            # Update the numbers around the placed mine
            update_numbers(board, row, col)
    
    return board

def update_numbers(board, row, col):
    # Update the adjacent numbers around the placed mine
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < len(board) and 0 <= nc < len(board[0]) and board[nr][nc] != 'M':
                board[nr][nc] = str(int(board[nr][nc]) + 1)

def print_board(board, revealed, flagged, game_over):
    for row in board:
        print(' '.join(row))

def print_board(board, revealed, flagged, game_over):
    if(game_over):
        for row in board:
            print(' '.join(row))
    else:
        for row in range(len(board)):
            row_str = ""
            for col in range(len(board[0])):
                if revealed[row][col]:
                    if board[row][col] == 'M':
                        row_str += "M "
                    else:
                        row_str += board[row][col] + " "
                else:
                    if flagged[row][col]:
                        row_str += "F "
                    else:
                        row_str += "X "
            print(row_str)



def get_player_move(board, revealed):
    print("Choose the cell:")
    while True:
        try:
            row = int(input("Enter row (0 to {}): ".format(len(board) - 1)))
            col = int(input("Enter column (0 to {}): ".format(len(board[0]) - 1)))

            if not (0 <= row < len(board)) or not (0 <= col < len(board[0])):
                print("Invalid row or column. Try again.")
            elif revealed[row][col]:
                print("Cell already revealed. Try again.")
            else:
                return row, col
        except ValueError:
            print("Invalid input. Please enter integers for row and column.")


def heuristic_suggest_safe_moves(board, revealed):
    safe_moves = []

    for row in range(len(board)):
        for col in range(len(board[0])):
            if revealed[row][col]:
                continue  # Skip already revealed cells

            neighbors = get_neighbors(row, col, len(board), len(board[0]))

            unrevealed_neighbors = [neighbor for neighbor in neighbors if not revealed[neighbor[0]][neighbor[1]]]
            try:
                num_mines = int(board[row][col])  # Number of adjacent mines
            except ValueError:
                pass
            num_unrevealed_neighbors = len(unrevealed_neighbors)

            # Calculate a safety score based on the number of mines and unrevealed neighbors
            safety_score = num_mines / (num_unrevealed_neighbors + 1)

            # If safety score is low, consider suggesting this cell as a safe move
            if safety_score < 0.5:
                safe_moves.append((row, col))

    return safe_moves


def get_neighbors(row, col, rows, cols):
    # Returns a list of neighboring cells' coordinates
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and (dr != 0 or dc != 0):
                neighbors.append((nr, nc))
    return neighbors


def reveal_adjacent_empty_cells(row, column, board, revealed):
    neighbors = get_neighbors(row, column, len(board), len(board[0]))
    
    for neighbor_row, neighbor_col in neighbors:
        if not revealed[neighbor_row][neighbor_col]:
            revealed[neighbor_row][neighbor_col] = True
            if board[neighbor_row][neighbor_col] == '0':
                reveal_adjacent_empty_cells(neighbor_row, neighbor_col, board, revealed)



def main():
    game_over = False
    # Initialize the Minesweeper board and other game elements.
    rows = 5  # Number of rows in the Minesweeper board
    cols = 5  # Number of columns in the Minesweeper board
    num_mines = 5  # Number of mines to place on the board
    
    board = initialize_board(rows, cols, num_mines)

    revealed = [[False for _ in range(cols)] for _ in range(rows)]  # Keep track of revealed cells
    flagged = [[False for _ in range(cols)] for _ in range(rows)]  # Keep track of flagged cells
    
    print("Welcome to Minesweeper!")
    print_board(board, revealed, flagged, game_over)
    
    while not game_over:
        # Player's turn
        action = input("\nReveal (R) or Flag (F) or AI's Hint(H)? ").upper()
        if(action != 'R' and action != 'F' and action != 'H'):
            action = input("Invalid action! Choose one of these- R, F, H: ")
        if(action == 'R' or action == 'F'):
            row, column = get_player_move(board, revealed)
            if(action == 'F'):
                flagged[row][column] = True
            elif(action == 'R'):
                if board[row][column] == 'M':
                    # Handle mine reveal, end game
                    game_over = True
                    print_board(board, revealed, flagged, game_over)
                    print("Oops! You hit a mine!")
                    print("___GAME OVER___")
                    break
                else:
                    # Update the revealed status
                    revealed[row][column] = True
                    
                    # If the revealed cell is '0', reveal adjacent cells recursively
                    if board[row][column] == '0':
                        reveal_adjacent_empty_cells(row, column, board, revealed)
                    
                    # Update the board display
                    print_board(board, revealed, flagged, game_over)
        else:
            #hint using AI(heuristic function)
            safe_moves = heuristic_suggest_safe_moves(board, revealed)
            print("AI's safe move suggestions(depending on the current state of the board):", safe_moves)
        
        # Continue the game loop
        
    # Print game outcome (win/loss) and final board

if __name__ == "__main__":
    main()
