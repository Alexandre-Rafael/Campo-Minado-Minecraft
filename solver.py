import pyautogui

class Solver:
    def __init__(self, board):
        self._board = board

    def move(self):
        for row in self._board.get_board():
            for piece in row:
                if not piece.get_clicked():
                    continue
                around = piece.get_num_around()
                unknown = 0
                flagged = 0
                neighbors = piece.get_neighbors()
                for p in neighbors:
                    if not p.get_clicked():
                        unknown += 1
                    if p.get_flagged():
                        flagged += 1
                if around == flagged:
                    self._open_unflagged(neighbors)
                if around == unknown:
                    self._flag_all(neighbors)

    def _open_unflagged(self, neighbors):
        for piece in neighbors:
            if not piece.get_flagged():
                self._board.handle_click(piece, False)

    def _flag_all(self, neighbors):
        for piece in neighbors:
            if not piece.get_flagged():
                self._board.handle_click(piece, True)
