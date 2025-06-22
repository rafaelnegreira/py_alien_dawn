import pygame
import json
from PPlay.animation import *
from PPlay.collision import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.point import *
from PPlay.sound import *
from PPlay.sprite import *
from PPlay.window import *
from player import *
from game_conf import *

def game_menu(janela, mouse):

    fundo = GameImage("img/fundo_menu.png")

    jogar = Sprite("img/jogar.png")
    jogar.set_position(janela.width/2 - jogar.width/2, janela.height/2 - jogar.height/2)

    sair = Sprite("img/sair.png")
    sair.set_position(janela.width/2 - jogar.width/2, janela.height/2 + jogar.height)

    while True:

        janela.set_background_color((0,0,0))

        fundo.draw()

        if mouse.is_button_pressed(1):
            if(mouse.is_over_object(jogar)):
                return "jogo"
        
            if(mouse.is_over_object(sair)):
                return "sair"

        jogar.draw()
        sair.draw()

        janela.update()
