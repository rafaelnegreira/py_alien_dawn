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
GAME_STATE = 0
janela = Window(800, 600)
teclado = Keyboard()
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
    hp=5
    )
player.position(100,300)

mapa = Maps("cidade")
camera = Camera(janela.width, janela.height)

while True:
    if GAME_STATE == 0:
        janela.set_background_color((0, 0, 0))

        camera.update(player.sprite)

        player.atualizar_sprites()

        player.mover(teclado, mapa.colisores, janela)
        # Blocos com offset de câmera
        for bloco in mapa.colisores:
            camera.apply(bloco)
            bloco.draw()
            camera.undo(bloco)
        player.atirar(teclado)

        camera.apply(mapa.background)
        mapa.background.draw()
        camera.undo(mapa.background)

        camera.apply(player.sprite)
        player.desenhar()
        camera.undo(player.sprite)

        janela.update()