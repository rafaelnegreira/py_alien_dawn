from GameObjects import *

import pygame
from PPlay.animation import *
from PPlay.collision import *
from PPlay.gameimage import *
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.window import *
from LevelManager import load_map_objects
from player import *
from menu import game_menu
from GameObjects import * # <--- ADICIONE ESTA LINHA


class Camera:
    # (A classe Camera está correta e permanece a mesma)
    def __init__(self, window_width, window_height):
        self.x = 0
        self.y = 0
        self.window_width = window_width
        self.window_height = window_height

    def update(self, target):
        self.x = target.x - self.window_width / 2 + target.width / 2
        self.y = target.y - self.window_height / 2 + target.height / 2

    def apply(self, obj):
        obj.set_position(obj.x - self.x, obj.y - self.y)

    def undo(self, obj):
        obj.set_position(obj.x + self.x, obj.y + self.y)

class Game_Manager:
    def __init__(self, janela):
        self.janela = janela
        self.teclado = janela.get_keyboard()
        self.mouse = janela.get_mouse()
        
        self.GAME_STATE = "menu"
        self.puzzle_ativo = None
        self.background = None
        
        # Listas para guardar os objetos do mapa
        self.all_objects = []
        self.colisores = []
        self.portais = []
        self.puzzles = []
        self.itens = []

        # Componentes do jogo
        self.arma = Arma(1000, 200)
        self.player = Player(
            tipo="Player", speed=150, hp=5, arma=self.arma,
            sprite_stay="assets/Apocalypse Character Pack/Player/iddle_front2.png",
            sprite_left="assets/Apocalypse Character Pack/Player/walk_left2.png",
            sprite_right="assets/Apocalypse Character Pack/Player/walk_right2.png",
            sprite_up="assets/Apocalypse Character Pack/Player/walk_back2.png",
            sprite_down="assets/Apocalypse Character Pack/Player/walk_front2.png",
            sprite_shoot_up="assets/Apocalypse Character Pack/Player/shoot_up.png",
            sprite_shoot_down="assets/Apocalypse Character Pack/Player/shoot_down.png",
            sprite_shoot_left="assets/Apocalypse Character Pack/Player/shoot_left.png",
            sprite_shoot_right="assets/Apocalypse Character Pack/Player/shoot_right.png",
        )
        self.camera = Camera(janela.width, janela.height)
        self.tempo_atual = 0

    def carregar_mapa(self, nome_mapa, spawn_x, spawn_y):
        self.all_objects = load_map_objects(nome_mapa)
        self.background = GameImage(f"mapa/{nome_mapa}.png")
        
        # Popula as listas de objetos para fácil acesso
        self.colisores = [obj for obj in self.all_objects if isinstance(obj, Colisores)]
        self.portais = [obj for obj in self.all_objects if isinstance(obj, Portais)]
        self.puzzles = [obj for obj in self.all_objects if isinstance(obj, Puzzle)]
        self.itens = [obj for obj in self.all_objects if isinstance(obj, Item)]
        
        self.player.position(spawn_x, spawn_y)

    def update_game(self, delta):
        self.tempo_atual += delta
        self.player.atualizar_sprites()
        self.player.mover(self.teclado, self.colisores, self.janela)
        self.player.atirar(self.teclado, self.tempo_atual)
        # CORREÇÃO: Passando a variável local 'delta'
        self.arma.atualizar_projeteis(delta)
        self.camera.update(self.player.sprite)

        # Lógica de interação
        if self.teclado.key_pressed("E"):
            # Interação com Portais
            for portal in self.portais:
                if not portal.locked and self.player.sprite.collided(portal):
                    destino = getattr(portal, 'destino', None)
                    spawn_x = int(getattr(portal, 'spawn_x', 100))
                    spawn_y = int(getattr(portal, 'spawn_y', 100))
                    if destino:
                        self.carregar_mapa(destino, spawn_x, spawn_y)
                        break
            # Interação com Puzzles
            for pz in self.puzzles:
                 if not pz.concluido and self.player.sprite.collided(pz):
                     if pz.interagir():
                         self.puzzle_ativo = pz
                         self.GAME_STATE = "puzzle"
                         break

    def draw_game(self):
        self.janela.set_background_color((0, 0, 0))
        
        self.camera.apply(self.background)
        self.background.draw()
        self.camera.undo(self.background)

        # (Opcional) Desenhar colisores para debug
        # for b in self.colisores:
        #     self.camera.apply(b)
        #     b.draw()
        #     self.camera.undo(b)

        self.camera.apply(self.player.sprite)
        self.player.desenhar()
        self.camera.undo(self.player.sprite)

        for proj in self.arma.projeteis_ativos:
            sprite_proj = proj["sprite"]
            self.camera.apply(sprite_proj)
            sprite_proj.draw()
            self.camera.undo(sprite_proj)

    def run(self):
        """O loop principal que controla todos os estados do jogo."""
        while True:
            delta = self.janela.delta_time()

            if self.GAME_STATE == "menu":
                # game_menu agora retorna para qual estado ir
                proximo_estado = game_menu(self.janela, self.mouse)
                if proximo_estado == "jogo":
                    self.carregar_mapa("laboratorio", 150, 130) # Carrega o mapa inicial
                    self.GAME_STATE = "jogo"
                elif proximo_estado == "sair":
                    self.GAME_STATE = "sair"

            elif self.GAME_STATE == "jogo":
                self.update_game(delta)
                self.draw_game()

            elif self.GAME_STATE == "puzzle":
                # Lógica de placeholder para um puzzle
                self.janela.set_background_color((20, 0, 20))
                self.janela.draw_text(f"PUZZLE: {self.puzzle_ativo.name}", 250, 250, 40, (255,255,255))
                self.janela.draw_text("Pressione 'C' para completar", 250, 300, 20, (255,255,255))
                if self.teclado.key_pressed("C"):
                    self.puzzle_ativo.concluir()
                    # Lógica para destravar o portal associado
                    portal_id = getattr(self.puzzle_ativo, 'portal_target_id', None)
                    if portal_id:
                        for portal in self.portais:
                            if str(portal.id) == str(portal_id):
                                portal.unlock()
                                break
                    self.GAME_STATE = "jogo"

            elif self.GAME_STATE == "sair":
                break # Sai do loop

            self.janela.update()
        
        self.janela.close()