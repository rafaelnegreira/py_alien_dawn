from pplay.window import Window
from pplay.mouse import Mouse
from pzzlHosp_conf import*
janela = Window(800, 720)
janela.set_title("Terminal de Energia do Hospital")
mouse = Mouse()
terminal_puzzle = ManageTerminal(janela, mouse)
while True:
    terminal_puzzle.update(janela.delta_time())
    terminal_puzzle.draw()
    janela.update()