from pplay.window import Window
from pzzlHosp_conf import*
janela = Window(640, 480)
janela.set_title("Terminal de Energia do Hospital")
terminal_puzzle = ManageTerminal(janela)
while True:    
    terminal_puzzle.update()
    terminal_puzzle.draw()
    janela.update()