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

    def perseguir(self, player, colisores, delta_time): # <-- ADICIONADO 'colisores'
        """Calcula a direção até o jogador e se move, evitando paredes."""
        player_x = player.sprite.x
        player_y = player.sprite.y

        vetor_x = player_x - self.sprite.x
        vetor_y = player_y - self.sprite.y
        distancia = math.sqrt(vetor_x ** 2 + vetor_y ** 2)

        if distancia > 0:
            vetor_x_normalizado = vetor_x / distancia
            vetor_y_normalizado = vetor_y / distancia

            # --- LÓGICA DE COLISÃO ---
            
        # 1. Salva a posição original antes de qualquer movimento neste frame
        old_x = self.sprite.x
        old_y = self.sprite.y

        # 2. Calcula o quanto mover em cada eixo
        movimento_x = vetor_x_normalizado * self.speed * delta_time
        movimento_y = vetor_y_normalizado * self.speed * delta_time

        # 3. Tenta mover no eixo X
        self.sprite.x += movimento_x
        # 4. Verifica colisão no eixo X
        for bloco in colisores:
            if self.sprite.collided(bloco):
                # Se colidiu, REVERTE a posição X para a que era antes.
                self.sprite.x = old_x
                break # Para o loop de colisores para este eixo

        # 5. Tenta mover no eixo Y
        self.sprite.y += movimento_y
        # 6. Verifica colisão no eixo Y
        for bloco in colisores:
            if self.sprite.collided(bloco):
                # Se colidiu, REVERTE a posição Y para a que era antes.
                self.sprite.y = old_y
                break # Para o loop de colisores para este eixo

    def desenhar(self):
        """Atualiza e desenha o sprite atual do inimigo."""
        self.sprite.update()
        self.sprite.draw()