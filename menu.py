import pygame
from PPlay.sprite import *
from PPlay.gameimage import *
import os

# Obtém o diretório do script para construir caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(*path_parts):
    """Constrói um caminho absoluto para um asset."""
    return os.path.join(BASE_DIR, *path_parts)

def game_menu(janela, mouse):
    # Caminhos absolutos para as imagens do menu
    fundo = GameImage(get_asset_path("assets", "img", "menu", "fundo_menu.png"))
    jogar = Sprite(get_asset_path("assets", "img", "menu", "jogar.png"))
    sair = Sprite(get_asset_path("assets", "img", "menu", "sair.png"))

    jogar.set_position(janela.width/2 - jogar.width/2, janela.height/2 - jogar.height/2)
    sair.set_position(janela.width/2 - jogar.width/2, janela.height/2 + jogar.height)

    while True:
        janela.set_background_color((0,0,0))
        fundo.draw()
        jogar.draw()
        sair.draw()

        if mouse.is_button_pressed(1):
            if mouse.is_over_object(jogar):
                return "jogo"
            if mouse.is_over_object(sair):
                return "sair"

        janela.update()