import pygame  # Importa o módulo pygame para desenvolver o jogo.
from board import Board  # Importa a classe Board do arquivo board.py.
import os  # Importa o módulo os para lidar com operações do sistema operacional.
from solver import Solver  # Importa a classe Solver do arquivo solver.py.
from time import sleep  # Importa a função sleep do módulo time para pausar o jogo.
import easygui  # Importa o módulo easygui para exibir caixas de diálogo.

class Game:
    def __init__(self, size, prob):
        # Inicializa a classe Game, que controla o fluxo do jogo.
        self.board = Board(size, prob)  # Cria uma instância da classe Board para representar o tabuleiro.
        pygame.init()  # Inicializa o pygame.
        self.sizeScreen = 1000, 1000  # Define o tamanho da tela do jogo.
        self.screen = pygame.display.set_mode(self.sizeScreen)  # Cria a janela do jogo com o tamanho especificado.
        self.pieceSize = (self.sizeScreen[0] / size[1], self.sizeScreen[1] / size[0])  # Calcula o tamanho de cada peça do tabuleiro.
        self.loadPictures()  # Carrega as imagens das peças do tabuleiro.
        self.solver = Solver(self.board)  # Cria uma instância da classe Solver para resolver o jogo.

    def loadPictures(self):
        # Carrega as imagens das peças do tabuleiro a partir dos arquivos de imagem.
        self.images = {}  # Cria um dicionário para armazenar as imagens das peças.
        imagesDirectory = "images"  # Define o diretório onde estão as imagens das peças.
        for fileName in os.listdir(imagesDirectory):  # Itera sobre os arquivos no diretório de imagens.
            if not fileName.endswith(".png"):  # Verifica se o arquivo não é uma imagem PNG.
                continue  # Pula para o próximo arquivo se não for uma imagem PNG.
            path = imagesDirectory + r"/" + fileName  # Obtém o caminho completo do arquivo de imagem.
            img = pygame.image.load(path)  # Carrega a imagem do arquivo.
            img = img.convert()  # Converte a imagem para o formato do pygame.
            img = pygame.transform.scale(img, (int(self.pieceSize[0]), int(self.pieceSize[1])))  # Redimensiona a imagem para o tamanho da peça.
            self.images[fileName.split(".")[0]] = img  # Armazena a imagem no dicionário usando o nome do arquivo como chave.

    def run(self):
        # Executa o loop principal do jogo.
        running = True  # Define uma variável para controlar o estado de execução do jogo.
        while running:  # Loop principal do jogo.
            for event in pygame.event.get():  # Itera sobre os eventos do pygame.
                if event.type == pygame.QUIT:  # Verifica se o evento é o fechamento da janela.
                    running = False  # Altera a variável para encerrar o loop do jogo.
                if event.type == pygame.MOUSEBUTTONDOWN and not (self.board.getWon() or self.board.getLost()):  # Verifica se o jogador clicou com o mouse e o jogo não terminou.
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]  # Verifica se foi um clique com o botão direito do mouse.
                    self.handleClick(pygame.mouse.get_pos(), rightClick)  # Manipula o clique do jogador.
                if event.type == pygame.KEYDOWN:  # Verifica se o jogador pressionou uma tecla do teclado.
                    self.solver.move()  # Executa a lógica do solver para mover no jogo.
            self.screen.fill((0, 0, 0))  # Preenche a tela com a cor preta.
            self.draw()  # Desenha o tabuleiro do jogo na tela.
            pygame.display.flip()  # Atualiza a tela.
            if self.board.getWon():  # Verifica se o jogador ganhou o jogo.
                self.show_message("Você Ganhou!")  # Exibe uma mensagem informando que o jogador ganhou o jogo.
                running = False  # Altera a variável para encerrar o loop do jogo.
            elif self.board.getLost():  # Verifica se o jogador perdeu o jogo.
                self.show_message("Você Perdeu!")  # Exibe uma mensagem informando que o jogador perdeu o jogo.
                running = False  # Altera a variável para encerrar o loop do jogo.
        pygame.quit()  # Finaliza o pygame após encerrar o jogo.

    def draw(self):
        # Desenha o tabuleiro do jogo na tela.
        topLeft = (0, 0)  # Define as coordenadas do canto superior esquerdo do tabuleiro.
        for row in self.board.getBoard():  # Itera sobre as linhas do tabuleiro.
            for piece in row:  # Itera sobre as peças em cada linha do tabuleiro.
                rect = pygame.Rect(topLeft, self.pieceSize)  # Cria um retângulo para a peça.
                image = self.images[self.getImageString(piece)]  # Obtém a imagem correspondente à peça.
                self.screen.blit(image, topLeft)  # Desenha a imagem da peça na tela.
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]  # Atualiza as coordenadas para a próxima peça na mesma linha.
            topLeft = (0, topLeft[1] + self.pieceSize[1])  # Atualiza as coordenadas para a próxima linha do tabuleiro.

    def getImageString(self, piece):
        # Obtém a string que representa a imagem da peça com base em seu estado.
        if piece.getClicked():  # Verifica se a peça foi clicada.
            return str(piece.getNumAround()) if not piece.getHasBomb() else 'bomb-at-clicked-block'  # Retorna a string com o número de bombas ao redor ou 'bomb-at-clicked-block' se a peça contém uma bomba.
        if (self.board.getLost()):  # Verifica se o jogo foi perdido.
            if (piece.getHasBomb()):  # Verifica se a peça contém uma bomba.
                return 'unclicked-bomb'  # Retorna a string 'unclicked-bomb' para indicar uma bomba não clicada.
            return 'wrong-flag' if piece.getFlagged() else 'empty-block'  # Retorna 'wrong-flag' se a peça estiver incorretamente marcada com uma bandeira, senão retorna 'empty-block'.
        return 'flag' if piece.getFlagged() else 'empty-block'  # Retorna 'flag' se a peça estiver marcada com uma bandeira, senão retorna 'empty-block'.

    def handleClick(self, position, flag):
        # Manipula o clique do jogador.
        index = tuple(int(pos // size) for pos, size in zip(position, self.pieceSize))[::-1]  # Calcula o índice da peça clicada no tabuleiro.
        self.board.handleClick(self.board.getPiece(index), flag)  # Chama o método para lidar com o clique da peça.

    def show_message(self, message):
        # Exibe uma mensagem pop-up com o resultado do jogo.
        easygui.msgbox(message, title="Resultado")  # Exibe a mensagem pop-up com o resultado do jogo.

    pygame.display.set_caption("Campo minecraftnado")  # Define o título da janela do jogo.
