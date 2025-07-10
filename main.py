from game_conf import Game_Manager
from PPlay.window import Window

# Cria a janela
janela = Window(800, 600)
janela.set_title("Alien Dawn")

# 1. Cria a instância principal do gerenciador do jogo
game_manager = Game_Manager(janela)

# 2. Inicia o loop principal do jogo, que agora está dentro do Game_Manager
game_manager.run()