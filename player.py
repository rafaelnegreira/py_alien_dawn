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

class Character:
    def __init__(self, tipo, jump, hp):
        self.tipo = tipo
        self.jump = jump
        self.hp = hp

class Player(Character):
    def __init__(self, tipo, jump, speed, hp,
                 sprite_stay, sprite_left, sprite_right, sprite_down, sprite_up):
        
        super().__init__(tipo, jump, hp)
        self.position(100,350)
        self.speed = speed
        self.vy = 0
        self.is_jumping = False
        self.gravity = 1800
        self.jump_force = -500

        self.sprite_stay = Sprite(sprite_stay, 2)
        self.sprite_right = Sprite(sprite_right, 4)
        self.sprite_left = Sprite(sprite_left, 4)
        self.sprite_down = Sprite(sprite_down, 4)
        self.sprite_up = Sprite(sprite_up, 4)

        self.sprite_stay.set_sequence_time(0, 2, 220, True)
        self.sprite_left.set_sequence_time(0, 4, 220, True)
        self.sprite_right.set_sequence_time(0, 4, 220, True)
        self.sprite_down.set_sequence_time(0, 4, 220, True)
        self.sprite_up.set_sequence_time(0, 4, 220, True)

        self.sprite = self.sprite_stay

    def position(self, x, y):
        self.sprite.set_position(x, y)

    def atualizar_sprites(self):
        self.sprite_left.x = self.sprite.x
        self.sprite_left.y = self.sprite.y

        self.sprite_right.x = self.sprite.x
        self.sprite_right.y = self.sprite.y

        self.sprite_stay.x = self.sprite.x
        self.sprite_stay.y = self.sprite.y

        self.sprite_up.x = self.sprite.x
        self.sprite_up.y = self.sprite.y

        self.sprite_down.x = self.sprite.x
        self.sprite_down.y = self.sprite.y

    def mover(self, teclado, colisores, janela):
        if teclado.key_pressed("LEFT"):
            self.sprite = self.sprite_left
            self.sprite.x -= self.speed * janela.delta_time()
            for bloco in colisores:
                if Collision.collided(self.sprite, bloco):
                    self.sprite.x = bloco.x + bloco.width + 5

        elif teclado.key_pressed("RIGHT"):
            self.sprite = self.sprite_right
            self.sprite.x += self.speed * janela.delta_time()

            for bloco in colisores:
                if Collision.collided(self.sprite, bloco):
                    self.sprite.x = bloco.x - self.sprite.width - 5

        elif teclado.key_pressed("UP"):
            self.sprite = self.sprite_up
            self.sprite.y -= self.speed * janela.delta_time()
            
            for bloco in colisores:
                if Collision.collided(self.sprite, bloco):
                    self.sprite.y = bloco.y + bloco.height + 5

        elif teclado.key_pressed("DOWN"):
            self.sprite = self.sprite_down
            self.sprite.y += self.speed * janela.delta_time()

            for bloco in colisores:
                if Collision.collided(self.sprite, bloco):
                    self.sprite.y = bloco.y - self.sprite.width - 10

        else:
            self.sprite = self.sprite_stay

    def desenhar(self):
        self.sprite.update()
        self.sprite.draw()