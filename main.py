# main.py

import easygui
from game import Game
from board import Board
from difficulty import choose_difficulty
from menu import show_menu

def main():
    while True:
        choice = show_menu()
        if choice == "Iniciar o Jogo":
            size, prob = choose_difficulty()
            game = Game(size, prob)
            game.run()
        elif choice == "Créditos":
            easygui.msgbox("Alexandre Rafael Rodrigues de Oliveira - Matrícula 7019", title="Créditos")
        else:
            break

if __name__ == "__main__":
    main()