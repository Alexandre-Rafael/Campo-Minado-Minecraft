import random
import time

class Board:
    def __init__(self, size, prob):
        self.size = size
        self.board = []
        self.won = False 
        self.lost = False
        for row in range(size[0]):
            row = []
            for col in range(size[1]):
                bomb = random.random() < prob
                piece = Piece(bomb)
                row.append(piece)
            self.board.append(row)
        self.setNeighbors()
        self.setNumAround()

    def print(self):
        for row in self.board:
            for piece in row:
                print(piece, end=" ")
            print()

    def getBoard(self):
        return self.board

    def getSize(self):
        return self.size
    
    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    def handleClick(self, piece, flag):
        if piece.getClicked() or (piece.getFlagged() and not flag):
            return
        if flag:
            piece.toggleFlag()
            return
        piece.handleClick()
        if piece.getNumAround() == 0:
            for neighbor in piece.getNeighbors():
                self.handleClick(neighbor, False)
        if piece.getHasBomb():
            self.lost = True
        else:
            self.won = self.checkWon()
    
    def checkWon(self):
        for row in self.board:
            for piece in row:
                if not piece.getHasBomb() and not piece.getClicked():
                    return False
        return True

    def getWon(self):
        return self.won

    def getLost(self):
        return self.lost

    def setNeighbors(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                piece = self.board[row][col]
                neighbors = []
                self.addToNeighborsList(neighbors, row, col)
                piece.setNeighbors(neighbors)
    
    def addToNeighborsList(self, neighbors, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    continue
                if r < 0 or r >= self.size[0] or c < 0 or c >= self.size[1]:
                    continue
                neighbors.append(self.board[r][c])
    
    def setNumAround(self):
        for row in self.board:
            for piece in row:
                piece.setNumAround()
        
        
class Piece:
    # States: Not clicked, clicked, flagged
    def __init__(self, hasBomb):
        self.hasBomb = hasBomb
        self.around = 0
        self.clicked = False
        self.flagged = False
        self.neighbors = []

    def __str__(self):
        return str(self.hasBomb)

    def getNumAround(self):
        return self.around

    def getHasBomb(self):
        return self.hasBomb

    def getClicked(self):
        return self.clicked

    def getFlagged(self):
        return self.flagged

    def toggleFlag(self):
        self.flagged = not self.flagged

    def handleClick(self):
        self.clicked = True

    def setNumAround(self):
        num = 0
        for neighbor in self.neighbors:
            if neighbor.getHasBomb():
                num += 1
        self.around = num

    def setNeighbors(self, neighbors):
        self.neighbors = neighbors
        
    def getNeighbors(self):
        return self.neighbors
 