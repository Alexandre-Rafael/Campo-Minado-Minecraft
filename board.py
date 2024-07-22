import random

class Board:
    def __init__(self, size, prob):
        self._size = size
        self._board = []
        self._won = False 
        self._lost = False
        self._initialize_board(prob)
        self._set_neighbors()
        self._set_num_around()

    def _initialize_board(self, prob):
        for row in range(self._size[0]):
            row_list = []
            for col in range(self._size[1]):
                bomb = random.random() < prob
                piece = Piece(bomb)
                row_list.append(piece)
            self._board.append(row_list)

    def _set_neighbors(self):
        for row in range(len(self._board)):
            for col in range(len(self._board[0])):
                piece = self._board[row][col]
                neighbors = []
                self._add_to_neighbors_list(neighbors, row, col)
                piece.set_neighbors(neighbors)
    
    def _add_to_neighbors_list(self, neighbors, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    continue
                if r < 0 or r >= self._size[0] or c < 0 or c >= self._size[1]:
                    continue
                neighbors.append(self._board[r][c])
    
    def _set_num_around(self):
        for row in self._board:
            for piece in row:
                piece.set_num_around()

    def print(self):
        for row in self._board:
            for piece in row:
                print(piece, end=" ")
            print()

    def get_board(self):
        return self._board

    def get_size(self):
        return self._size
    
    def get_piece(self, index):
        return self._board[index[0]][index[1]]

    def handle_click(self, piece, flag):
        if piece.get_clicked() or (piece.get_flagged() and not flag):
            return
        if flag:
            piece.toggle_flag()
            return
        piece.handle_click()
        if piece.get_num_around() == 0:
            for neighbor in piece.get_neighbors():
                self.handle_click(neighbor, False)
        if piece.get_has_bomb():
            self._lost = True
        else:
            self._won = self._check_won()
    
    def _check_won(self):
        for row in self._board:
            for piece in row:
                if not piece.get_has_bomb() and not piece.get_clicked():
                    return False
        return True

    def get_won(self):
        return self._won

    def get_lost(self):
        return self._lost

class Piece:
    def __init__(self, has_bomb):
        self._has_bomb = has_bomb
        self._around = 0
        self._clicked = False
        self._flagged = False
        self._neighbors = []

    def __str__(self):
        return str(self._has_bomb)

    def get_num_around(self):
        return self._around

    def get_has_bomb(self):
        return self._has_bomb

    def get_clicked(self):
        return self._clicked

    def get_flagged(self):
        return self._flagged

    def toggle_flag(self):
        self._flagged = not self._flagged

    def handle_click(self):
        self._clicked = True

    def set_num_around(self):
        num = 0
        for neighbor in self._neighbors:
            if neighbor.get_has_bomb():
                num += 1
        self._around = num

    def set_neighbors(self, neighbors):
        self._neighbors = neighbors

    def get_neighbors(self):
        return self._neighbors
