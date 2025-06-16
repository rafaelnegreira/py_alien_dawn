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
    def __init__(self, tipo, hp):
        self.tipo = tipo
        self.hp = hp

class Arma:
    def __init__(self, qtd_municao, speed):
        self.qtd_municao = qtd_municao
        self.speed = speed
        self.projeteis_ativos = []
        self.cooldown = 0.3  # segundos
        self.tempo_ultimo_disparo = 0

    def disparo(self, x, y, direcao, tempo_atual):
        if self.qtd_municao > 0 and tempo_atual - self.tempo_ultimo_disparo > self.cooldown:
            proj_sprite = None

            match direcao.upper():
                case "UP":
                    proj_sprite = Sprite("img/projetil_up.png", 1)
                    proj_sprite.set_position(x - proj_sprite.width / 2, y - proj_sprite.height)
                case "DOWN":
                    proj_sprite = Sprite("img/projetil_down.png", 1)
                    proj_sprite.set_position(x - proj_sprite.width / 2, y)
                case "LEFT":
                    proj_sprite = Sprite("img/projetil_left.png", 1)
                    proj_sprite.set_position(x - proj_sprite.width, y - proj_sprite.height / 2)
                case "RIGHT":
                    proj_sprite = Sprite("img/projetil_right.png", 1)
                    proj_sprite.set_position(x, y - proj_sprite.height / 2)

            if proj_sprite:
                self.projeteis_ativos.append({"sprite": proj_sprite, "direcao": direcao.upper()})
                self.qtd_municao -= 1
                self.tempo_ultimo_disparo = tempo_atual

    def atualizar_projeteis(self, delta_time):
        for proj in self.projeteis_ativos:
            match proj["direcao"]:
                case "UP":
                    proj["sprite"].y -= self.speed * delta_time
                case "DOWN":
                    proj["sprite"].y += self.speed * delta_time
                case "LEFT":
                    proj["sprite"].x -= self.speed * delta_time
                case "RIGHT":
                    proj["sprite"].x += self.speed * delta_time

        # Remove projéteis fora da tela
        self.projeteis_ativos = [
            p for p in self.projeteis_ativos
            if 0 <= p["sprite"].x <= 1800 and 0 <= p["sprite"].y <= 1600
        ]

    def desenhar_projeteis(self):
        for proj in self.projeteis_ativos:
            proj["sprite"].draw()


class Player(Character):
    def __init__(self, tipo, speed, hp,
                 sprite_stay, sprite_left, sprite_right, sprite_down, sprite_up, 
                 sprite_shoot_up,sprite_shoot_down, sprite_shoot_left, sprite_shoot_right,
                 arma):
        
        super().__init__(tipo, hp)
        self.speed = speed

        self.hp = hp

        self.arma_equip = True
    
        self.arma = arma

        self.inventario = []

        self.sprite_stay = Sprite(sprite_stay, 2)
        self.sprite_right = Sprite(sprite_right, 4)
        self.sprite_left = Sprite(sprite_left, 4)
        self.sprite_down = Sprite(sprite_down, 4)
        self.sprite_up = Sprite(sprite_up, 4)

        self.sprite_shoot_up = Sprite(sprite_shoot_up, 2)
        self.sprite_shoot_down = Sprite(sprite_shoot_down, 2)
        self.sprite_shoot_left = Sprite(sprite_shoot_left, 2)
        self.sprite_shoot_right = Sprite(sprite_shoot_right, 2)
    
        self.sprite_stay.set_sequence_time(0, 2, 220, True)
        self.sprite_left.set_sequence_time(0, 4, 220, True)
        self.sprite_right.set_sequence_time(0, 4, 220, True)
        self.sprite_down.set_sequence_time(0, 4, 220, True)
        self.sprite_up.set_sequence_time(0, 4, 220, True)
        
        self.sprite_shoot_up.set_sequence_time(0,1,200, True)
        self.sprite_shoot_down.set_sequence_time(0,1,200, True)
        self.sprite_shoot_left.set_sequence_time(0,1,200, True)
        self.sprite_shoot_right.set_sequence_time(0,1,200, True)

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

        self.sprite_shoot_up.x = self.sprite.x
        self.sprite_shoot_up.y = self.sprite.y

        self.sprite_shoot_down.x = self.sprite.x
        self.sprite_shoot_down.y = self.sprite.y

        self.sprite_shoot_left.x = self.sprite.x
        self.sprite_shoot_left.y = self.sprite.y

        self.sprite_shoot_right.x = self.sprite.x
        self.sprite_shoot_right.y = self.sprite.y

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

    def atirar(self, teclado, tempo_atual):
        if not self.arma_equip:
            return

        if teclado.key_pressed("SPACE"):
            if teclado.key_pressed("UP"):
                self.sprite = self.sprite_shoot_up
                self.arma.disparo(
                    self.sprite.x + self.sprite.width / 2,
                    self.sprite.y,
                    "up",
                    tempo_atual
                )
            elif teclado.key_pressed("DOWN"):
                self.sprite = self.sprite_shoot_down
                self.arma.disparo(
                    self.sprite.x + self.sprite.width / 2,
                    self.sprite.y + self.sprite.height,
                    "down",
                    tempo_atual
                )
            elif teclado.key_pressed("LEFT"):
                self.sprite = self.sprite_shoot_left
                self.arma.disparo(
                    self.sprite.x,
                    self.sprite.y + self.sprite.height / 2,
                    "left",
                    tempo_atual
                )
            elif teclado.key_pressed("RIGHT"):
                self.sprite = self.sprite_shoot_right
                self.arma.disparo(
                    self.sprite.x + self.sprite.width,
                    self.sprite.y + self.sprite.height / 2,
                    "right",
                    tempo_atual
                )

    def desenhar(self):
        self.sprite.update()
        self.sprite.draw()