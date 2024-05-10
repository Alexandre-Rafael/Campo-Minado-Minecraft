
import easygui

def choose_difficulty():
    difficulty_choices = ["Fácil", "Médio", "Difícil"]
    choice = easygui.buttonbox("Escolha a dificuldade:", choices=difficulty_choices)
    if choice == "Fácil":
        size = (9, 9)
        prob = 0.1
    elif choice == "Médio":
        size = (16, 16)
        prob = 0.2
    else:
        size = (16, 30)
        prob = 0.3
    return size, prob
