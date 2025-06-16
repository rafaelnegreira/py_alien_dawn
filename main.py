from game_conf import *

janela = Window(800, 600)
teclado = Keyboard()
janela.set_title("Alien Dawn")
game_manager = Portais(Game_Manager(janela))

while True:
    game_manager.draw()
    # Atualiza a janela
    janela.update()