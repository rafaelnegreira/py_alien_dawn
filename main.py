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
from menu import *

GAME_STATE = "menu"

janela = Window(800, 600)
teclado = Keyboard()
mouse = Mouse()

arma = Arma(1000, 200)

player = Player(
    tipo="Player",
    speed=100,
    sprite_stay="Apocalypse Character Pack\Player\iddle_front2.png",
    sprite_left="Apocalypse Character Pack\Player\walk_left2.png",
    sprite_right="Apocalypse Character Pack\Player\walk_right2.png",
    sprite_up="Apocalypse Character Pack\Player\walk_back2.png",
    sprite_down="Apocalypse Character Pack\Player\walk_front2.png",
    sprite_shoot_up="Apocalypse Character Pack\Player\shoot_up.png",
    sprite_shoot_down="Apocalypse Character Pack\Player\shoot_down.png",
    sprite_shoot_left="Apocalypse Character Pack\Player\shoot_left.png",
    sprite_shoot_right="Apocalypse Character Pack\Player\shoot_right.png",
    hp=5,
    arma=arma)

player.position(150,130)
tempo_atual = 0

mapa = Maps("laboratorio")
camera = Camera(janela.width, janela.height)

while True:
    if GAME_STATE == "sair":
        janela.close()

    if GAME_STATE == "menu":
        GAME_STATE = game_menu(janela, mouse)

    if GAME_STATE == "jogo":
        janela.set_background_color((0, 0, 0))
        
        delta = janela.delta_time()
        tempo_atual += delta

        player.atualizar_sprites()
        player.mover(teclado, mapa.colisores, janela)
        player.atirar(teclado, tempo_atual)
        arma.atualizar_projeteis(delta)
        camera.update(player.sprite)

        # --- DESENHAR TUDO NA TELA (com correção da câmera) ---
        
        camera.apply(mapa.background)
        mapa.background.draw()
        camera.undo(mapa.background)

        for bloco in mapa.colisores:
            camera.apply(bloco)
            # bloco.draw() # Descomente se quiser ver as caixas de colisão
            camera.undo(bloco)
            
        # Desenha o jogador
        camera.apply(player.sprite)
        player.desenhar()
        camera.undo(player.sprite)

        # Desenha os projéteis, aplicando a câmera a cada um
        for proj in arma.projeteis_ativos:
            sprite_proj = proj["sprite"]
            camera.apply(sprite_proj)
            sprite_proj.draw()
            camera.undo(sprite_proj)

        # Atualiza a janela
        janela.update()