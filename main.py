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

janela = Window(600, 400)
teclado = Keyboard()

class Camera:
    def __init__(self, window_width, window_height):
        self.x = 0
        self.y = 0
        self.window_width = window_width
        self.window_height = window_height

    def update(self, target):
        self.x = target.x - self.window_width // 2 + target.width // 2
        self.y = target.y - self.window_height // 2 + target.height // 2

    def apply(self, obj):
        """Aplica o offset da câmera a um objeto PPlay (Sprite/GameImage)."""
        obj.set_position(obj.x - self.x, obj.y - self.y)

    def undo(self, obj):
        """Restaura a posição original após desenhar."""
        obj.set_position(obj.x + self.x, obj.y + self.y)

# Carrega colisores do JSON exportado do Tiled
with open("mapa\cidade.json") as f:
    mapa = json.load(f)

colisores = []
for layer in mapa["layers"]:
    if layer["type"] == "objectgroup" and layer["name"] == "solidos":
        for obj in layer["objects"]:
            bloco = GameImage("bloco_transparente.png")
            bloco.set_position(obj["x"], obj["y"])
            bloco.width = obj["width"]
            bloco.height = obj["height"]
            colisores.append(bloco)

class Character:
    def __init__(self, tipo, jump, hp):
        self.tipo = tipo
        self.jump = jump
        self.hp = hp

class Player(Character):
    def __init__(self, tipo, jump, speed, hp,
                 sprite_stay, sprite_left, sprite_right, sprite_down, sprite_up):
        
        super().__init__(tipo, jump, hp)
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

    def mover(self):
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

player = Player(
    tipo="Player",
    jump=False,
    speed=100,
    sprite_stay="Apocalypse Character Pack\Player\iddle_front2.png",
    sprite_left="Apocalypse Character Pack\Player\walk_left2.png",
    sprite_right="Apocalypse Character Pack\Player\walk_right2.png",
    sprite_up="Apocalypse Character Pack\Player\walk_back2.png",
    sprite_down="Apocalypse Character Pack\Player\walk_front2.png",
    hp=100
    )

player.position(100,350)

tile1 = GameImage("mapa\sem título.png")

camera = Camera(janela.width, janela.height)

while True:

    janela.set_background_color((0, 0, 0))

    camera.update(player.sprite)

    player.atualizar_sprites()
    player.mover()

    # Blocos com offset de câmera
    for bloco in colisores:
        camera.apply(bloco)
        bloco.draw()
        camera.undo(bloco)

    camera.apply(tile1)
    tile1.draw()
    camera.undo(tile1)

    # Player com offset de câmera
    camera.apply(player.sprite)
    player.desenhar()
    camera.undo(player.sprite)

    janela.update()