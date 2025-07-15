import math
from PPlay.sprite import *
from player import Character
import os

# Obtém o diretório do script para construir caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class InimigoControlavel(Character):
    def __init__(self, tipo, hp, speed, x, y):
        super().__init__(tipo, hp)
        self.speed = speed
        
        # Caminho absoluto para o sprite do inimigo
        sprite_path = os.path.join(BASE_DIR, "assets", "inimigo", "inimigo_down.png")
        self.sprite_down = Sprite(sprite_path, 3)
        self.sprite_down.set_sequence_time(0, 3, 300)
        
        self.sprite = self.sprite_down
        self.sprite.set_position(x, y)

    def perseguir(self, player, colisores, delta_time):
        player_x = player.sprite.x
        player_y = player.sprite.y

        vetor_x = player_x - self.sprite.x
        vetor_y = player_y - self.sprite.y
        distancia = math.sqrt(vetor_x ** 2 + vetor_y ** 2)

        if distancia > 0:
            vetor_x_normalizado = vetor_x / distancia
            vetor_y_normalizado = vetor_y / distancia

            old_x = self.sprite.x
            old_y = self.sprite.y

            movimento_x = vetor_x_normalizado * self.speed * delta_time
            movimento_y = vetor_y_normalizado * self.speed * delta_time

            self.sprite.x += movimento_x
            for bloco in colisores:
                if self.sprite.collided(bloco):
                    self.sprite.x = old_x
                    break

            self.sprite.y += movimento_y
            for bloco in colisores:
                if self.sprite.collided(bloco):
                    self.sprite.y = old_y
                    break

    def desenhar(self):
        self.sprite.update()
        self.sprite.draw()