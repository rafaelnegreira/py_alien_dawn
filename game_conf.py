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
from GameObjects import * 
from inimigo import *
from puzzles import *
from PPlay.sound import Sound
import os

# --- Caminho Absoluto para Assets ---
# Obtém o diretório absoluto do script atual e o define como a base para todos os caminhos.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(*path_parts):
    """Constrói um caminho absoluto para um asset."""
    return os.path.join(BASE_DIR, *path_parts)

class Camera:
    def __init__(self, window_width, window_height):
        self.x = 0
        self.y = 0
        self.window_width = window_width
        self.window_height = window_height

    def update(self, target, mapa_largura, mapa_altura):
        # Se o mapa for menor que a tela, centraliza o mapa inteiro
        if mapa_largura <= self.window_width:
            self.x = -(self.window_width - mapa_largura) / 2
        else:
            self.x = target.x - self.window_width / 2 + target.width / 2
            self.x = max(0, min(self.x, mapa_largura - self.window_width))

        if mapa_altura <= self.window_height:
            self.y = -(self.window_height - mapa_altura) / 2
        else:
            self.y = target.y - self.window_height / 2 + target.height / 2
            self.y = max(0, min(self.y, mapa_altura - self.window_height))


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
        
        self.final = False
        # Listas para guardar os objetos do mapa
        self.all_objects = []
        self.colisores = []
        self.portais = []
        self.puzzles = []
        self.itens = []
        self.inimigos_vivos = []

        self.puzzles_concluidos = {}  # Armazena quais puzzles foram concluídos por nome
        self.itens_coletados = {}  # Armazena os itens já coletados, por ID

        # Componentes do jogo
        self.arma = Arma(0, 200)

        self.player = Player(
            tipo="Player", speed=150, hp=4, arma=self.arma,
            sprite_stay=get_asset_path("assets", "Apocalypse Character Pack", "Player", "iddle_front2.png"),
            sprite_left=get_asset_path("assets", "Apocalypse Character Pack", "Player", "walk_left2.png"),
            sprite_right=get_asset_path("assets", "Apocalypse Character Pack", "Player", "walk_right2.png"),
            sprite_up=get_asset_path("assets", "Apocalypse Character Pack", "Player", "walk_back2.png"),
            sprite_down=get_asset_path("assets", "Apocalypse Character Pack", "Player", "walk_front2.png"),
            sprite_shoot_up=get_asset_path("assets", "Apocalypse Character Pack", "Player", "shoot_up.png"),
            sprite_shoot_down=get_asset_path("assets", "Apocalypse Character Pack", "Player", "shoot_down.png"),
            sprite_shoot_left=get_asset_path("assets", "Apocalypse Character Pack", "Player", "shoot_left.png"),
            sprite_shoot_right=get_asset_path("assets", "Apocalypse Character Pack", "Player", "shoot_right.png"),
        )
        self.camera = Camera(janela.width, janela.height)
        self.tempo_atual = 0
        self.player.arma_equip = False  # Desativa a arma no início

        #efeitos sonoros e sons ambientes
        self.som_acerto_inimigo = Sound(get_asset_path("assets", "sounds", "acerto_inimigo.wav"))
        self.som_acerto_inimigo.set_volume(30)
        self.som_acerto_parede = Sound(get_asset_path("assets", "sounds", "tiro_bate_parede.wav"))
        self.som_acerto_parede.set_volume(15)
        self.som_ganhar_vida = Sound(get_asset_path("assets", "sounds", "ganhar_vida.wav"))
        self.som_perder_vida = Sound(get_asset_path("assets", "sounds", "perder_vida.wav"))
        self.som_pegar_municao = Sound(get_asset_path("assets", "sounds", "municao.wav"))
        self.som_pegar_item = Sound(get_asset_path("assets", "sounds", "pegar_item.wav"))

        self.som_ambiente_cidade = Sound(get_asset_path("assets", "sounds", "ambiente_cidade1.wav"))
        self.som_ambiente_cidade.set_repeat(True)
        self.som_ambiente_cidade.set_volume(60)
        self.som_ambiente_cidade2 = Sound(get_asset_path("assets", "sounds", "ambiente_cidade2.wav"))
        self.som_ambiente_cidade2.set_repeat(True)
        self.som_ambiente_cidade2.set_volume(60)
        self.som_ambiente_escola = Sound(get_asset_path("assets", "sounds", "ambiente_escola.wav"))
        self.som_ambiente_escola.set_repeat(True)
        self.som_ambiente_escola.set_volume(60)
        self.som_ambiente_laboratorio = Sound(get_asset_path("assets", "sounds", "ambiente_laboratorio.wav"))
        self.som_ambiente_laboratorio.set_repeat(True)
        self.som_ambiente_laboratorio.set_volume(60)
        self.som_ambiente_supermercado = Sound(get_asset_path("assets", "sounds", "ambiente_supermercado.wav"))
        self.som_ambiente_supermercado.set_repeat(True)
        self.som_ambiente_supermercado.set_volume(60)
        self.som_ambiente_fabrica = Sound(get_asset_path("assets", "sounds", "ambiente_fabrica.wav"))
        self.som_ambiente_fabrica.set_repeat(True)
        self.som_ambiente_fabrica.set_volume(60)
        self.som_ambiente_hospital = Sound(get_asset_path("assets", "sounds", "ambiente_hospital.wav"))
        self.som_ambiente_hospital.set_repeat(True)
        self.som_ambiente_hospital.set_volume(60)

    def carregar_mapa(self, nome_mapa, spawn_x, spawn_y):
        self.all_objects = load_map_objects(nome_mapa)
        self.background = GameImage(get_asset_path("mapa", f"{nome_mapa}.png"))
        
        self.inimigos_vivos.clear() 

        self.colisores = [obj for obj in self.all_objects if isinstance(obj, Colisores)]
        self.portais = [obj for obj in self.all_objects if isinstance(obj, Portais)]
        self.puzzles = [obj for obj in self.all_objects if isinstance(obj, Puzzle)]
        
        for pz in self.puzzles:
            if self.puzzles_concluidos.get(pz.name.lower(), False):
                pz.concluido = True

        self.itens = [obj for obj in self.all_objects if isinstance(obj, Item)]

        for item in self.itens:
            if self.itens_coletados.get(str(item.id), False):
                item.coletado = True

        map_inimigos_spawners = [obj for obj in self.all_objects if isinstance(obj, Inimigo)]

        for spawner in map_inimigos_spawners:
            novo_inimigo = InimigoControlavel(
                tipo="alien", 
                hp=1, 
                speed=70,
                x=spawner.x,
                y=spawner.y
            )
            self.inimigos_vivos.append(novo_inimigo)

        self.player.position(spawn_x, spawn_y)

    def update_game(self, delta):
        self.tempo_atual += delta
        self.player.atualizar_sprites()
        self.player.mover(self.teclado, self.colisores, self.janela)
        self.player.atirar(self.teclado, self.tempo_atual)
        self.arma.atualizar_projeteis(delta)
        self.camera.update(self.player.sprite, self.background.width, self.background.height)
        self.player.atualizar_invulnerabilidade(delta)

        if self.teclado.key_pressed("E"):
            for portal in self.portais:
                if not portal.locked and self.player.sprite.collided(portal):
                    destino = getattr(portal, 'destino', None)
                    spawn_x = int(getattr(portal, 'spawn_x', 100))
                    spawn_y = int(getattr(portal, 'spawn_y', 100))

                    if destino == "laboratorio_dinamico":
                        self.som_ambiente_cidade.stop()
                        self.som_ambiente_cidade2.stop()
                        self.som_ambiente_laboratorio.play()
                        
                        if self.puzzles_concluidos.get("cofre_lab", False):
                            destino = "laboratorio"
                        else:
                            destino = "laboratorio_fechado"

                    if destino == "supermercado_dinamico":
                        self.som_ambiente_cidade.stop()
                        self.som_ambiente_cidade2.stop()
                        self.som_ambiente_supermercado.play()
                        
                        if self.puzzles_concluidos.get("lampadas", False):
                            destino = "supermercado"
                        else:
                            destino = "supermercado_fechado"

                    if destino == "fabrica_dinamico":
                        self.som_ambiente_cidade.stop()
                        self.som_ambiente_cidade2.stop()
                        self.som_ambiente_fabrica.play()
                        
                        if self.puzzles_concluidos.get("puzzle_fabrica", False):
                            destino = "fabrica"
                        else:
                            destino = "fabrica_fechado"

                    if destino == "hospital_dinamico":
                        self.som_ambiente_cidade.stop()
                        self.som_ambiente_cidade2.stop()
                        self.som_ambiente_hospital.play()

                        if self.puzzles_concluidos.get("puzzle_hospital", False):
                            destino = "hospital"
                        else:
                            destino = "hospital_fechado"
                    
                    if destino == "cidade":
                        self.som_ambiente_hospital.stop()
                        self.som_ambiente_fabrica.stop()
                        self.som_ambiente_escola.stop()
                        self.som_ambiente_supermercado.stop()
                        self.som_ambiente_laboratorio.stop()
                        self.som_ambiente_cidade.play()
                        self.som_ambiente_cidade2.play()

                    if destino == "escola":
                        self.som_ambiente_cidade.stop()
                        self.som_ambiente_cidade2.stop()
                        self.som_ambiente_escola.play()

                    if destino:
                        self.carregar_mapa(destino, spawn_x, spawn_y)
                        break

            for pz in self.puzzles:
                 if not pz.concluido and self.player.sprite.collided(pz):
                     if pz.interagir():
                         self.puzzle_ativo = pz
                         self.GAME_STATE = "puzzle"
                         break
        
            for item in self.itens:
                if not item.coletado and self.player.sprite.collided(item):
                    nome_item = item.name.lower()

                    if "vela_ignicao" in nome_item:
                        self.player.inventario.append(item.name)
                        self.som_pegar_item.play()
                        print(f"{item.name} adicionado ao inventário.")
                        self.cutscene([GameImage(get_asset_path("assets", "img", "historia", "H_vela.png"))])

                    if "combustivel" in nome_item:
                        self.player.inventario.append(item.name)
                        self.som_pegar_item.play()
                        print(f"{item.name} adicionado ao inventário.")
                        self.cutscene([GameImage(get_asset_path("assets", "img", "historia", "H_combustivel.png"))])

                    if "bateria" in nome_item:
                        self.player.inventario.append(item.name)
                        self.som_pegar_item.play()
                        print(f"{item.name} adicionado ao inventário.")
                        self.cutscene([GameImage(get_asset_path("assets", "img", "historia", "H_bateria.png"))])

                    if "vida" in nome_item:
                        self.player.hp += 1
                        self.som_ganhar_vida.play()
                        print("Vida +1")

                    if "municao" in nome_item:
                        self.arma.qtd_municao += 8
                        self.som_pegar_municao.play()
                        print(f"Munição +8 QTD = {self.arma.qtd_municao}")

                    if "final" in nome_item:
                        if "vela_ignicao" in self.player.inventario and \
                           "chave_roda" in self.player.inventario and \
                           "combustivel" in self.player.inventario and \
                           "bateria" in self.player.inventario:
                            self.GAME_STATE = "final"
                        else:
                            self.cutscene([GameImage(get_asset_path("assets", "img", "historia", "H_carro.png"))])

                    else:
                        item.interagir()
                        self.itens_coletados[str(item.id)] = True

        for inimigo in self.inimigos_vivos:
            inimigo.perseguir(self.player, self.colisores, delta)

            if self.player.sprite.collided(inimigo.sprite) and not self.player.invulneravel:
                self.player.hp -= 1
                self.player.invulneravel = True
                self.player.tempo_invulneravel = 2
                self.som_perder_vida.play()
                print(f"Jogador atingido! Vidas restantes: {self.player.hp}")

        if self.player.hp <= 0:
            self.cutscene([GameImage(get_asset_path("assets", "img", "historia", "H_morte1.png"))])
            self.resetar_jogo()
            return

        projeteis_para_remover = []
        inimigos_para_remover = []

        for proj in self.arma.projeteis_ativos:
            for bloco in self.colisores:
                if proj["sprite"].collided(bloco):
                    self.som_acerto_parede.play()
                    if proj not in projeteis_para_remover:
                        projeteis_para_remover.append(proj)
                    break 

        for proj in self.arma.projeteis_ativos:
            for inimigo in self.inimigos_vivos:
                if proj["sprite"].collided(inimigo.sprite):
                    self.som_acerto_inimigo.play()
                    if proj not in projeteis_para_remover:
                        projeteis_para_remover.append(proj)
                    if inimigo not in inimigos_para_remover:
                        inimigos_para_remover.append(inimigo)

        for proj in projeteis_para_remover:
            self.arma.projeteis_ativos.remove(proj)
            
        for inimigo in inimigos_para_remover:
            self.inimigos_vivos.remove(inimigo)

    def draw_game(self):
        self.janela.set_background_color((0, 0, 0))
        
        self.camera.apply(self.background)
        self.background.draw()
        self.camera.undo(self.background)

        if not self.player.invulneravel or int(self.tempo_atual * 10) % 2 == 0:
            self.camera.apply(self.player.sprite)
            self.player.desenhar()
            self.camera.undo(self.player.sprite)

        for proj in self.arma.projeteis_ativos:
            sprite_proj = proj["sprite"]
            self.camera.apply(sprite_proj)
            sprite_proj.draw()
            self.camera.undo(sprite_proj)

        for inimigo in self.inimigos_vivos:
            self.camera.apply(inimigo.sprite)
            inimigo.desenhar()
            self.camera.undo(inimigo.sprite)

        self.desenhar_interface()

    def desenhar_interface(self):
        coracao = GameImage(get_asset_path("assets", "ui", "coracao_cheio.png"))
        for i in range(self.player.hp):
            coracao.set_position(10 + i * (coracao.width + 5), 10)
            coracao.draw()

        icone_municao = GameImage(get_asset_path("assets", "ui", "icone_municao.png"))
        icone_municao.set_position(10, 60)
        icone_municao.draw()
        self.janela.draw_text(f"{self.arma.qtd_municao}", 50, 60, size=24, color=(255,255,255), bold=True)

        inventario_base_x = 10
        inventario_base_y = 110
        espacamento = 40

        for idx, item_nome in enumerate(self.player.inventario):
            try:
                item_img = GameImage(get_asset_path("assets", "ui", f"{item_nome}.png"))
                item_img.set_position(inventario_base_x + idx * espacamento, inventario_base_y)
                item_img.draw()
            except:
                pass

    def cutscene_inicial(self):
        imagens = [
            GameImage(get_asset_path("assets", "img", "historia", "H1.png")),
            GameImage(get_asset_path("assets", "img", "historia", "H2.png")),
            GameImage(get_asset_path("assets", "img", "historia", "H3.png"))
        ]
        self.cutscene(imagens)

    def cutscene(self, imagens):
        texto = "Pressione ESPAÇO para continuar"
        fonte = pygame.font.SysFont("Arial", 20)
        largura, altura = fonte.size(texto)

        for img in imagens:
            img.set_position(0, 0)
            tempo = 0

            while True:
                delta = self.janela.delta_time()
                tempo += delta
                img.draw()
                self.janela.draw_text(texto, self.janela.width/2 - largura/2, self.janela.height - 40, size=20, color=(255, 255, 255))
                if self.teclado.key_pressed("SPACE") and tempo > 0.5:
                    break
                self.janela.update()

    def tela_final(self):
        imagens = [
            GameImage(get_asset_path("assets", "img", "historia", "H_final1.png")),
            GameImage(get_asset_path("assets", "img", "historia", "H_final2.png"))
        ]
        self.cutscene(imagens)

    def resetar_jogo(self):
        self.player.hp = 4
        self.player.inventario.clear()
        self.player.invulneravel = False
        self.player.tempo_invulneravel = 0
        self.arma.qtd_municao = 0
        self.arma.projeteis_ativos.clear()
        self.player.arma_equip = False

        self.puzzles_concluidos.clear()
        self.itens_coletados.clear()

        for pz in self.puzzles:
            pz.concluido = False
        for item in self.itens:
            item.coletado = False

        self.inimigos_vivos.clear()
        self.all_objects.clear()
        self.portais.clear()
        self.puzzles.clear()
        self.itens.clear()
        self.colisores.clear()

        self.som_ambiente_escola.stop()
        self.som_ambiente_fabrica.stop()
        self.som_ambiente_supermercado.stop()
        self.som_ambiente_laboratorio.stop()
        self.som_ambiente_hospital.stop()
        self.som_ambiente_cidade.stop()
        self.som_ambiente_cidade2.stop()

        resetar_puzzle_lab()
        resetar_puzzle_cadeado()
        resetar_puzzle_lampadas()
        resetar_puzzle_hospital()
        resetar_puzzle_luzes()

        self.GAME_STATE = "menu"

    def run(self):
        while True:
            delta = self.janela.delta_time()

            if self.GAME_STATE == "menu":
                proximo_estado = game_menu(self.janela, self.mouse)
                if proximo_estado == "jogo":
                    self.som_ambiente_laboratorio.play()
                    self.cutscene_inicial()
                    self.carregar_mapa("laboratorio_fechado", 150, 130)
                    self.GAME_STATE = "jogo"
                elif proximo_estado == "sair":
                    self.GAME_STATE = "sair"
            
            elif self.GAME_STATE == "final":
                self.tela_final()
                self.resetar_jogo()
                continue

            elif self.GAME_STATE == "jogo":
                self.update_game(delta)
                self.draw_game()

            elif self.GAME_STATE == "puzzle":
                nome = self.puzzle_ativo.name.lower()
                completou = False

                if self.teclado.key_pressed("esc"):
                    self.GAME_STATE = "jogo"

                if nome == "cofre_lab":
                    completou = puzzle_lab(self.janela, self.teclado, self.janela.delta_time())
                elif nome == "cadeado":
                    completou = puzzle_cadeado(self.janela, self.teclado, self.mouse, delta)
                elif nome == "lampadas":
                    completou = puzzle_lampadas(self.janela, self.teclado, self.mouse, delta)
                elif nome == "puzzle_hospital":
                    completou = puzzle_hospital(self.janela, self.teclado, self.mouse)
                elif nome == "puzzle_fabrica":
                    completou = puzzle_luzes(self.janela, self.teclado, self.mouse)
                else:
                    self.janela.set_background_color((20, 0, 20))
                    self.janela.draw_text(f"PUZZLE: {self.puzzle_ativo.name}", 250, 250, 40, (255,255,255))
                    self.janela.draw_text("Pressione 'C' para completar", 250, 300, 20, (255,255,255))
                    if self.teclado.key_pressed("C"):
                        completou = True

                if completou:
                    self.puzzle_ativo.concluir()
                    self.puzzles_concluidos[self.puzzle_ativo.name.lower()] = True

                    if self.puzzle_ativo.name.lower() == "cofre_lab":
                        self.player.arma_equip = True
                        self.arma.qtd_municao += 8
                        self.carregar_mapa("laboratorio", self.player.get_position_x(), self.player.get_position_y())
                        self.som_pegar_item.play()
                        cutscene_images = [
                            GameImage(get_asset_path("assets", "img", "historia", "H_cofre_lab1.png")),
                            GameImage(get_asset_path("assets", "img", "historia", "H_cofre_lab2.png")),
                            GameImage(get_asset_path("assets", "img", "historia", "H_cofre_lab3.png"))
                        ]
                        self.cutscene(cutscene_images)

                    if self.puzzle_ativo.name.lower() == "lampadas":
                        self.carregar_mapa("supermercado", self.player.get_position_x(), self.player.get_position_y())
                    if self.puzzle_ativo.name.lower() == "puzzle_fabrica":
                        self.carregar_mapa("fabrica", self.player.get_position_x(), self.player.get_position_y())
                    if self.puzzle_ativo.name.lower() == "puzzle_hospital":
                        self.carregar_mapa("hospital", self.player.get_position_x(), self.player.get_position_y())
                    if self.puzzle_ativo.name.lower() == "cadeado":
                        self.player.inventario.append("chave_roda")
                        print(f"chave_roda adicionado ao inventário.")
                        self.carregar_mapa("escola", self.player.get_position_x(), self.player.get_position_y())
                        self.som_pegar_item.play()
                        self.cutscene([GameImage(get_asset_path("assets", "img", "historia", "H_chave_roda.png"))])

                    portal_id = getattr(self.puzzle_ativo, 'portal_target_id', None)
                    if portal_id:
                        for portal in self.portais:
                            if str(portal.id) == str(portal_id):
                                portal.unlock()
                                break
                    self.GAME_STATE = "jogo"

            elif self.GAME_STATE == "sair":
                break

            self.janela.update()
        
        self.janela.close()