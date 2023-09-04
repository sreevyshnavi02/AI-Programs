class MancalaGame:
    def __init__(self):
        self.board = [4] * 14  # 14 pits in total, each initially with 4 stones
        self.current_player = 0  # 0 for player A, 1 for player B
        self.hint_counter = {'A': 3, 'B': 3}  # Initialize hint counters for both players

    def display_board(self):
        print(f"Player A: {self.board[6]}   {[str(self.board[i]) for i in range(5, -1, -1)]}")
        print(f"Player B: {self.board[13]}   {[str(self.board[i]) for i in range(7, 13)]}")
        
    def make_move(self, pit_index):
        if self.current_player == 0 and 1 <= pit_index <= 6:
            
            if self.board[pit_index] == 0:
                print("Invalid move. Choose a non-empty pit.")
                return
            stones_to_distribute = self.board[pit_index]
            self.board[pit_index] = 0
            while stones_to_distribute > 0:
                pit_index = (pit_index + 1) % 14
                if pit_index != 13:  # Skip player B's mancala
                    self.board[pit_index] += 1
                    stones_to_distribute -= 1
            self.check_game_over()
            self.switch_player()
        elif self.current_player == 1 and 7 <= pit_index <= 12:
            if self.board[pit_index] == 0:
                print("Invalid move. Choose a non-empty pit.")
                return
            stones_to_distribute = self.board[pit_index]
            self.board[pit_index] = 0
            while stones_to_distribute > 0:
                pit_index = (pit_index + 1) % 14
                if pit_index != 6:  # Skip player A's mancala
                    self.board[pit_index] += 1
                    stones_to_distribute -= 1
            self.check_game_over()
            self.switch_player()
        else:
            print("Invalid move. Choose a pit on your side (1-6 for Player A, 7-12 for Player B).")

    def check_game_over(self):
        # Check if one side is empty, and if so, end the game
        if all(self.board[i] == 0 for i in range(7)):
            self.board[13] += sum(self.board[7:13])
            for i in range(7, 13):
                self.board[i] = 0
            self.display_board()
            self.end_game()
        elif all(self.board[i] == 0 for i in range(7, 14)):
            self.board[6] += sum(self.board[0:6])
            for i in range(6):
                self.board[i] = 0
            self.display_board()
            self.end_game()

    def end_game(self):
        print("Game over!")
        if self.board[6] > self.board[13]:
            print("Player A wins!")
        elif self.board[13] > self.board[6]:
            print("Player B wins!")
        else:
            print("It's a tie!")

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def play(self):
        while True:
            self.display_board()
            player_letter = 'A' if self.current_player == 0 else 'B'
            print(f"Player {player_letter}'s turn")

            if self.hint_counter[player_letter] > 0:
                hint = input("Do you want a hint? (yes/no): ").strip().lower()
                if hint == 'yes':
                    self.provide_hint(player_letter)
                    self.hint_counter[player_letter] -= 1

            pit_index = int(input("Choose a pit (1-6 for Player A, 7-12 for Player B): "))
            self.make_move(pit_index)

    def provide_hint(self, player_letter):
        # Create a GuidingAI instance to suggest a move
        ai = GuidingAI(player_letter)

        # Clone the current board state
        cloned_board = [row[:] for row in self.board]

        # Get the suggested move from the AI
        suggested_move = ai.suggest_move(cloned_board)

        # Display the hint
        print(f"Suggested move for Player {player_letter}: Pit {suggested_move + 1}")


class GuidingAI:
    def __init__(self, player):
        self.player = player

    def heuristic_function(self, board):
        player_index = 0 if player == 'A' else 1
        opponent_index = 1 - player_index

        player_score = board[player_index][6]
        opponent_score = board[opponent_index][6]

        # Favor moves that capture opponent's stones
        capture_bonus = board[opponent_index][0:6].count(0)

        return player_score - opponent_score + capture_bonus

    def suggest_move(self, board):
        best_move = None
        best_score = float('-inf') if self.player == 'A' else float('inf')

        for move in range(6):
            if board[self.player][move] == 0:
                continue  # Skip empty pits

            # Clone the board to evaluate the move
            cloned_board = [row[:] for row in board]

            # Make the move and distribute the stones
            self.make_move(cloned_board, move)

            # Evaluate the board after the move
            score = self.heuristic_function(cloned_board)

            # Update the best move if a better one is found
            if (self.player == 'A' and score > best_score) or (self.player == 'B' and score < best_score):
                best_move = move
                best_score = score

        return best_move


if __name__ == "__main__":
    game = MancalaGame()
    game.play()
