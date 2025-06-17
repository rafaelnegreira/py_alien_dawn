import math
from PPlay.sprite import *
from player import Character # Herda de Character, que está em player.py

class InimigoControlavel(Character):
    def __init__(self, tipo, hp, speed, x, y):
        super().__init__(tipo, hp)
        self.speed = speed
        
        # Sprites (use os caminhos para seus assets)

        self.sprite_down = Sprite("assets\inimigo\inimigo_down.png", 3)
        self.sprite_down.set_sequence_time(0, 3, 300)
        
        # O sprite atual que será desenhado
        self.sprite = self.sprite_down
        self.sprite.set_position(x, y)

    def perseguir(self, player, delta_time):
        """Calcula a direção até o jogador e se move."""
        player_x = player.sprite.x
        player_y = player.sprite.y

        # 1. Calcula o vetor do inimigo para o jogador
        vetor_x = player_x - self.sprite.x
        vetor_y = player_y - self.sprite.y

        # 2. Calcula a distância (magnitude do vetor)
        distancia = math.sqrt(vetor_x ** 2 + vetor_y ** 2)

        if distancia > 0: # Evita divisão por zero se estiver no mesmo lugar
            # 3. Normaliza o vetor (transforma em um vetor de comprimento 1)
            vetor_x_normalizado = vetor_x / distancia
            vetor_y_normalizado = vetor_y / distancia

            # 4. Move o inimigo na direção normalizada, multiplicado pela velocidade
            self.sprite.x += vetor_x_normalizado * self.speed * delta_time
            self.sprite.y += vetor_y_normalizado * self.speed * delta_time

    def desenhar(self):
        """Atualiza e desenha o sprite atual do inimigo."""
        self.sprite.update()
        self.sprite.draw()