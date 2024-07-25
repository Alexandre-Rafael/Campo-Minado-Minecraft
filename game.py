import pygame  
from board import Board 
import os 
from solver import Solver  
import easygui  

class Game:
    def __init__(self, size, prob):
        self._board = Board(size, prob)
        pygame.init()  
        self._size_screen = (1000, 1000)  
        self._screen = pygame.display.set_mode(self._size_screen) 
        self._piece_size = (self._size_screen[0] / size[1], self._size_screen[1] / size[0]) #calcula tamanho peça com base na screen e no tabuleiro
        self._load_pictures()  
        self._solver = Solver(self._board)  

    def _load_pictures(self):
        # carrega as imagens PNG do diretório "images"
        self._images = {}  # dicionario imagens carregadas
        images_directory = "images"  
        for file_name in os.listdir(images_directory):  
            if not file_name.endswith(".png"):  
                continue
            path = os.path.join(images_directory, file_name)  
            img = pygame.image.load(path)  
            img = img.convert()  
            img = pygame.transform.scale(img, (int(self._piece_size[0]), int(self._piece_size[1])))
            self._images[file_name.split(".")[0]] = img

    def run(self):
        running = True  # variável para controlar o loop do jogo, pra continuar jogando
        while running:
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    running = False  
                if event.type == pygame.MOUSEBUTTONDOWN and not (self._board.get_won() or self._board.get_lost()):
                    right_click = pygame.mouse.get_pressed(num_buttons=3)[2] 
                    self._handle_click(pygame.mouse.get_pos(), right_click)
                if event.type == pygame.KEYDOWN:
                    self._solver.move()
            self._screen.fill((0, 0, 0))  #preenche a tela com a cor preta
            self._draw()  #desenha o tabuleiro na tela
            pygame.display.flip()  
            if self._board.get_won():  
                self._show_message("Você Ganhou!")  
                running = False  
            elif self._board.get_lost(): 
                self._show_message("Você Perdeu!") 
                running = False 
        pygame.quit()  

    def _draw(self):
        top_left = (0, 0) #primeira posição
        for row in self._board.get_board():  # itera sobre cada linha do tabuleiro
            for piece in row:  
                rect = pygame.Rect(top_left, self._piece_size)  
                image = self._images[self._get_image_string(piece)]  #obtem a imagem correspondente
                self._screen.blit(image, top_left)  
                top_left = (top_left[0] + self._piece_size[0], top_left[1])  #vai pra proxima
            top_left = (0, top_left[1] + self._piece_size[1])  # proxima linha

    def _get_image_string(self, piece):
        #determina a imagem com base no estado da peça e no estado geral do tabuleiro
        if piece.get_clicked():
            return str(piece.get_num_around()) if not piece.get_has_bomb() else 'bomb-at-clicked-block'
        if self._board.get_lost():
            # perdendo retorna bombas que nao foram clicadas ou bandeiras
            if piece.get_has_bomb():
                return 'unclicked-bomb'
            return 'wrong-flag' if piece.get_flagged() else 'empty-block'

        return 'flag' if piece.get_flagged() else 'empty-block'

    def _handle_click(self, position, flag):
        #converte a posição do clique para o índice da peça e lida com o clique
        index = tuple(int(pos // size) for pos, size in zip(position, self._piece_size))[::-1]
        self._board.handle_click(self._board.get_piece(index), flag)

    def _show_message(self, message):
        #exibe uma caixa de mensagem com o resultado do jogo
        easygui.msgbox(message, title="Resultado")

    pygame.display.set_caption("Campo Minecraftnado")  # define o título da janela do jogo
