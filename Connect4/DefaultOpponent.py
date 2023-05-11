import numpy as np

class DefaultOpponent:
    
    def __init__(self):
        self.player = 1
        
    def get_move(self, board):
        """Given the current board, return a move for the opponent."""
        cols = np.arange(board.shape[1])
        np.random.shuffle(cols)  # shuffle columns to add randomness
        for col in cols:
            # Check if opponent can win by placing a piece in the current column
            row = self._get_next_row(board, col)
            board[row][col] = self.player
            if self._is_winning_move(board, row, col):
                return col
            board[row][col] = 0  # undo move
            
        for col in cols:
            # Check if opponent needs to block the opponent's winning move
            row = self._get_next_row(board, col)
            board[row][col] = self.player % 2 + 1
            if self._is_winning_move(board, row, col):
                board[row][col] = self.player  # undo move
                return col
            board[row][col] = 0  # undo move
        
        # Otherwise, play a random move
        return np.random.choice(np.where(board[0] == 0)[0])
        
    def _get_next_row(self, board, col):
        """Given the current board and a column, return the next available row in that column."""
        return np.argmax(board[:,col] == 0)
    
    def _is_winning_move(self, board, row, col):
        """Check if the current move is a winning move."""
        player = board[row][col]
        # Check vertical direction
        if row >= 3 and np.all(board[row-3:row+1,col] == player):
            return True
        # Check horizontal direction
        for c in range(col-3, col+1):
            if c >= 0 and c+3 < board.shape[1]:
                if np.all(board[row,c:c+4] == player):
                    return True
        # Check diagonal direction (top-left to bottom-right)
        for r,c in zip(range(row-3,row+1), range(col-3,col+1)):
            if r >= 0 and r+3 < board.shape[0] and c >= 0 and c+3 < board.shape[1]:
                if np.all(board[r:r+4,c:c+4].diagonal() == player):
                    return True
        # Check diagonal direction (bottom-left to top-right)
        for r,c in zip(range(row+3,row-1,-1), range(col-3,col+1)):
            if r >= 0 and r-3 < board.shape[0] and c >= 0 and c+3 < board.shape[1]:
                if np.all(np.fliplr(board[r-3:r+1,c:c+4]).diagonal() == player):
                    return True
        return False
