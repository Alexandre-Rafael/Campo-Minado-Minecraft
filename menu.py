import easygui

def show_menu():
    menu_choices = ["Iniciar o Jogo", "Créditos", "Sair"]
    choice = easygui.buttonbox("Selecione uma opção:", choices=menu_choices)
    return choice
