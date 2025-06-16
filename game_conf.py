import pygame
from PPlay.animation import *
from PPlay.collision import *
from PPlay.gameobject import *
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.point import *
from PPlay.sound import *
from PPlay.window import *
from LevelManager import* 
from player import*
from menu import *
import importlib
#player.position(100,300)
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
class Puzzles(GameObject):
        def __init__(self, janela, teclado, mouse):
            self.caminho = f"puzzles.{self}"
            self = importlib.import_module(self.caminho)
            self.janela = janela
            self.teclado = teclado
            self.mouse = mouse
        def start_puzzle(self):
            return self
        def end_puzzle(self):
            self.concluido = True
            Game_Manager.puzzle_ativo = None
            Game_Manager.GAME_STATE = "jogo"           
        def draw(self):
            self.draw() 
        
class Game_Manager:
    def __init__(self, janela):
        self.janela = janela
        self.teclado = janela.get_keyboard()
        self.mouse = janela.get_mouse()
        self.game_obj = []
        self.GAME_STATE = "menu"
        self.puzzle_ativo = None        
        self.background = None
        self.arma = Arma(1000, 200)
        self.player = Player(tipo="Player", speed=100,
        sprite_stay="assets/Apocalypse Character Pack/Player/iddle_front2.png",
        sprite_left="assets/Apocalypse Character Pack/Player/walk_left2.png",
        sprite_right="assets/Apocalypse Character Pack/Player/walk_right2.png",
        sprite_up="assets/Apocalypse Character Pack/Player/walk_back2.png",
        sprite_down="assets/Apocalypse Character Pack/Player/walk_front2.png",
        sprite_shoot_up="assets/Apocalypse Character Pack/Player/shoot_up.png",
        sprite_shoot_down="assets/Apocalypse Character Pack/Player/shoot_down.png",
        sprite_shoot_left="assets/Apocalypse Character Pack/Player/shoot_left.png",
        sprite_shoot_right="assets/Apocalypse Character Pack/Player/shoot_right.png",
        hp=5, arma=self.arma)
        self.camera = Camera(janela.width, janela.height)
        self.tempo_atual = 0
        Game_Manager.estados_jogo(self)
    def estados_jogo(self):
        if self.GAME_STATE == "menu":
            game_menu(self.janela, self.mouse)
        elif self.GAME_STATE in ["jogo", "puzzle"]:
            Game_Manager.interagir_tipo(self)
        elif self.GAME_STATE == "sair":
            self.janela.close()
    def interagir_tipo(self):
        if isinstance(self, Portais) and Player.collided(self) and self.locked != True and self.teclado.key_pressed("E"):
                Game_Manager.carregar_mapa(self)
        elif isinstance(self, Puzzle)and Player.collided(self) and self.concluido != True and self.teclado.key_pressed("E"):
            self.GAME_STATE == "puzzle"
            self.puzzle_ativo = Puzzles.start_puzzle(self)               
        #elif isinstance(obj, Item) and  Player.collided(obj) and obj.concluido != True and teclado.key_pressed("E"):
            #Player.collect(obj.name)
    def carregar_mapa(self):
        if self.background == None:
            self.game_obj = [Objects_json("cidade")]
            self.background = GameImage("mapa/cidade.png")
            self.x =  150
            self.y = 130                 
        else:
            self.game_obj.clear()
            self.itens.clear()
            self.colisores.clear()
            self.game_obj = Objects_json(self.id)
            self.background = GameImage(f"mapa/{self.id}.png")
        self.itens = [obj for obj in self.game_obj if isinstance(obj, Item)]
        self.colisores = [obj for obj in self.game_obj if isinstance(obj, Colisores)]
        if self.player: self.player.set_position(self.x, self.y)
    def draw(self):
        if self.GAME_STATE == "jogo":
            self.janela.set_background_color((0, 0, 0))
            
            delta = self.janela.delta_time()
            self.tempo_atual += delta
                    
            # --- 1. ATUALIZAR A LÓGICA DO JOGO ---
            self.player.atualizar_sprites()
            self.player.mover(self.teclado, self.colisores, self.janela)
            self.player.atirar(self.teclado, self.tempo_atual)
            self.arma.atualizar_projeteis(self.delta) # Atualiza a posição dos projéteis no "mundo"
            self.camera.update(self.player.sprite) # Atualiza a posição da câmera para seguir o jogador

            # Desenha o fundo
            self.camera.apply(self.background)
            self.background.draw()
            self.camera.undo(self.background)

            # Desenha os colisores (para debug, se desejar)
            for bloco in self.colisores:
                self.camera.apply(bloco)
                # bloco.draw() # Descomente se quiser ver as caixas de colisão
                self.camera.undo(bloco)
            
            # Desenha o jogador
            self.camera.apply(self.player.sprite)
            self.player.desenhar()
            self.camera.undo(self.player.sprite)

            # >>> A CORREÇÃO ESTÁ AQUI <<<
            # Desenha os projéteis, aplicando a câmera a cada um
            for proj in self.arma.projeteis_ativos:
                sprite_proj = proj["sprite"]
                self.camera.apply(sprite_proj)
                sprite_proj.draw()
                self.camera.undo(sprite_proj)
        elif self.GAME_STATE == "puzzle":
            self.update()
            Puzzle.draw(self)    