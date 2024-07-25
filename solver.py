import pyautogui  

class Solver:
    def __init__(self, board):
        #inicializa o Solver com o tabuleiro fornecido
        self._board = board

    def move(self):
        for row in self._board.get_board():
            for piece in row:
                if not piece.get_clicked():
                    continue  # ignora peças que ainda não foram clicadas
                around = piece.get_num_around()  
                unknown = 0  #vizinhos desconhecidos
                flagged = 0  #vizinhos marcados com bandeira
                neighbors = piece.get_neighbors()  
                for p in neighbors:
                    if not p.get_clicked():
                        unknown += 1  #incrementa o contador de vizinhos desconhecidos
                    if p.get_flagged():
                        flagged += 1  #incrementa o contador de vizinhos com bandeira
                #se o número de bombas ao redor for igual ao número de vizinhos com bandeira, abre os vizinhos não marcados
                if around == flagged:
                    self._open_unflagged(neighbors)
                #se o número de bombas ao redor é igual ao número de vizinhos desconhecidos, marca todos os vizinhos
                if around == unknown:
                    self._flag_all(neighbors)

    def _open_unflagged(self, neighbors):
        #abre todas as peças vizinhas que não estão marcadas com bandeira
        for piece in neighbors:
            if not piece.get_flagged():
                self._board.handle_click(piece, False)  # Clique na peça para abri-la

    def _flag_all(self, neighbors):
        #marca todas as peças vizinhas que não estão marcadas com bandeira
        for piece in neighbors:
            if not piece.get_flagged():
                self._board.handle_click(piece, True)  # Adiciona uma bandeira à peça
