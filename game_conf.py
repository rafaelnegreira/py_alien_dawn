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
        self.arma = Arma(1, 200)

        self.player = Player(
            tipo="Player", speed=300, hp=5, arma=self.arma,
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
        self.player.arma_equip = False  # Desativa a arma no início

        #efeitos sonoros e sons ambientes
        self.som_acerto_inimigo = Sound("assets/sounds/acerto_inimigo.wav")
        self.som_acerto_inimigo.set_volume(10)
        self.som_acerto_parede = Sound("assets/sounds/tiro_bate_parede.wav")
        self.som_acerto_parede.set_volume(5)
        self.som_ganhar_vida = Sound("assets/sounds/ganhar_vida.wav")
        self.som_perder_vida = Sound("assets/sounds/perder_vida.wav")
        self.som_pegar_municao = Sound("assets/sounds/municao.wav")
        self.som_pegar_item = Sound("assets/sounds/pegar_item.wav")

        self.som_ambiente_cidade = Sound("assets/sounds/ambiente_cidade.wav")
        self.som_ambiente_cidade.set_repeat(True)
        self.som_ambiente_cidade.set_volume(50)
        self.som_ambiente_escola = Sound("assets/sounds/ambiente_escola.wav")
        self.som_ambiente_escola.set_repeat(True)
        self.som_ambiente_escola.set_volume(50)
        self.som_ambiente_laboratorio = Sound("assets/sounds/ambiente_laboratorio.wav")
        self.som_ambiente_laboratorio.set_repeat(True)
        self.som_ambiente_laboratorio.set_volume(50)
        self.som_ambiente_supermercado = Sound("assets/sounds/ambiente_supermercado.wav")
        self.som_ambiente_supermercado.set_repeat(True)
        self.som_ambiente_supermercado.set_volume(50)
        self.som_ambiente_fabrica = Sound("assets/sounds/ambiente_fabrica.wav")
        self.som_ambiente_fabrica.set_repeat(True)
        self.som_ambiente_fabrica.set_volume(50)
        self.som_ambiente_hospital = Sound("assets/sounds/ambiente_hospital.wav")
        self.som_ambiente_hospital.set_repeat(True)
        self.som_ambiente_hospital.set_volume(50)

    def carregar_mapa(self, nome_mapa, spawn_x, spawn_y):
        self.all_objects = load_map_objects(nome_mapa)
        self.background = GameImage(f"mapa/{nome_mapa}.png")
        
        #Limpar a lista de inimigos do mapa anterior
        # É importante para garantir que inimigos não passem de uma fase para outra.
        self.inimigos_vivos.clear() 

        self.colisores = [obj for obj in self.all_objects if isinstance(obj, Colisores)]
        self.portais = [obj for obj in self.all_objects if isinstance(obj, Portais)]
        self.puzzles = [obj for obj in self.all_objects if isinstance(obj, Puzzle)]
        # Atualiza os puzzles com o estado salvo
        for pz in self.puzzles:
            if self.puzzles_concluidos.get(pz.name.lower(), False):
                pz.concluido = True

        self.itens = [obj for obj in self.all_objects if isinstance(obj, Item)]

        # Marca os itens como coletados com base no progresso salvo
        for item in self.itens:
            if self.itens_coletados.get(str(item.id), False):
                item.coletado = True

        
        #Encontrar os "spawners" de inimigos carregados do mapa
        #filtramos os objetos que foram marcados como 'Inimigo' no Tiled.
        map_inimigos_spawners = [obj for obj in self.all_objects if isinstance(obj, Inimigo)]

        #Criar os inimigos 'vivos' a partir dos spawners
        # Para cada marcador encontrado no mapa, criamos um inimigo real e controlável
        # e o adicionamos na lista de inimigos ativos da fase.
        for spawner in map_inimigos_spawners:
            novo_inimigo = InimigoControlavel(
                tipo="alien", 
                hp=3, 
                speed=60,
                x=spawner.x,  # Usa a posição X definida no mapa
                y=spawner.y   # Usa a posição Y definida no mapa
            )
            self.inimigos_vivos.append(novo_inimigo)

        # Esta linha continua no final para posicionar o jogador corretamente
        self.player.position(spawn_x, spawn_y)

    def update_game(self, delta):
        self.tempo_atual += delta
        self.player.atualizar_sprites()
        self.player.mover(self.teclado, self.colisores, self.janela)
        self.player.atirar(self.teclado, self.tempo_atual)
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

                    # Lógica para mudar o destino com base no puzzle "cofre_lab"
                    if destino == "laboratorio_dinamico":
                        self.som_ambiente_cidade.stop()
                        self.som_ambiente_laboratorio.play()
                        
                        if self.puzzles_concluidos.get("cofre_lab", False):
                            destino = "laboratorio"
                        else:
                            destino = "laboratorio_fechado"

                    if destino == "supermercado_dinamico":
                        self.som_ambiente_cidade.stop()
                        self.som_ambiente_supermercado.play()
                        
                        if self.puzzles_concluidos.get("lampadas", False):
                            destino = "supermercado"
                        else:
                            destino = "supermercado_fechado"

                    if destino == "fabrica_dinamico":
                        self.som_ambiente_cidade.stop()
                        self.som_ambiente_fabrica.play()
                        
                        if self.puzzles_concluidos.get("puzzle_fabrica", False):
                            destino = "fabrica"
                        else:
                            destino = "fabrica_fechado"

                    if destino == "hospital_dinamico":
                        self.som_ambiente_cidade.stop()
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

                    if destino == "escola":
                        self.som_ambiente_cidade.stop()
                        self.som_ambiente_escola.play()

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
        
            # Coleta de itens
            for item in self.itens:
                if not item.coletado and self.player.sprite.collided(item):
                    nome_item = item.name.lower()

                    if "vida" in nome_item:
                        self.player.hp += 1
                        self.som_ganhar_vida.play()
                        print("Vida +1")

                    if "municao" in nome_item:
                        self.arma.qtd_municao += 10
                        self.som_pegar_municao.play()
                        print(f"Munição +10 QTD = {self.arma.qtd_municao}")

                    if "vela_ignicao" in nome_item:
                        self.player.inventario.append(item.name)
                        self.som_pegar_item.play()
                        print(f"{item.name} adicionado ao inventário.")

                    if "combustivel" in nome_item:
                        self.player.inventario.append(item.name)
                        self.som_pegar_item.play()
                        print(f"{item.name} adicionado ao inventário.")

                    if "bateria" in nome_item:
                        self.player.inventario.append(item.name)
                        self.som_pegar_item.play()
                        print(f"{item.name} adicionado ao inventário.")
                    
                    if "final" in nome_item:
                        if "vela_ignicao" in self.player.inventario:
                            if "chave_roda" in self.player.inventario:
                                if "combustivel" in self.player.inventario:
                                    if "bateria" in self.player.inventario:
                                        self.GAME_STATE = "final"
                    else:
                        item.interagir()
                        self.itens_coletados[str(item.id)] = True  # Marca como coletado permanentemente

        for inimigo in self.inimigos_vivos:
            inimigo.perseguir(self.player, self.colisores, delta)

        projeteis_para_remover = []
        inimigos_para_remover = []

        for proj in self.arma.projeteis_ativos:
            for bloco in self.colisores:
                # Se um projétil colidiu com um bloco sólido...
                if proj["sprite"].collided(bloco):
                    self.som_acerto_parede.play()
                    # ...e ainda não foi marcado para remoção...
                    if proj not in projeteis_para_remover:
                        # ...marque-o para ser removido.
                        projeteis_para_remover.append(proj)
                    break # Otimização: se o projétil já bateu, não precisa checar outras paredes.

        # Loop aninhado para testar cada projétil contra cada inimigo
        for proj in self.arma.projeteis_ativos:
            for inimigo in self.inimigos_vivos:
                # Usamos a colisão da própria PPlay
                if proj["sprite"].collided(inimigo.sprite):
                    self.som_acerto_inimigo.play()
                    # Adiciona ambos às listas de remoção
                    if proj not in projeteis_para_remover:
                        projeteis_para_remover.append(proj)
                    if inimigo not in inimigos_para_remover:
                        inimigos_para_remover.append(inimigo)

        # Agora, remove os itens marcados de suas listas originais
        for proj in projeteis_para_remover:
            self.arma.projeteis_ativos.remove(proj)
            
        for inimigo in inimigos_para_remover:
            self.inimigos_vivos.remove(inimigo)

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

        for inimigo in self.inimigos_vivos:
            self.camera.apply(inimigo.sprite)
            inimigo.desenhar()
            self.camera.undo(inimigo.sprite)

        self.desenhar_interface()


    def desenhar_interface(self):
        # --- VIDA ---
        coracao = GameImage("assets/ui/coracao_cheio.png")
        for i in range(self.player.hp):
            coracao.set_position(10 + i * (coracao.width + 5), 10)
            coracao.draw()

        # --- MUNIÇÃO ---
        icone_municao = GameImage("assets/ui/icone_municao.png")
        icone_municao.set_position(10, 60)
        icone_municao.draw()
        self.janela.draw_text(f"{self.arma.qtd_municao}", 50, 60, size=24, color=(255,255,255), bold=True)

        # --- INVENTÁRIO ---
        inventario_base_x = 10
        inventario_base_y = 110
        espacamento = 40

        for idx, item_nome in enumerate(self.player.inventario):
            try:
                item_img = GameImage(f"assets/ui/{item_nome}.png")
                item_img.set_position(inventario_base_x + idx * espacamento, inventario_base_y)
                item_img.draw()
            except:
                # Caso o arquivo do item não exista, ignora
                pass

    def run(self):
        """O loop principal que controla todos os estados do jogo."""
        while True:
            delta = self.janela.delta_time()

            if self.GAME_STATE == "menu":
                # game_menu agora retorna para qual estado ir
                proximo_estado = game_menu(self.janela, self.mouse)
                if proximo_estado == "jogo":
                    self.carregar_mapa("laboratorio_fechado", 667, 130) # Carrega o mapa inicial
                    # self.carregar_mapa("laboratorio_fechado", 150, 130) # Carrega o mapa inicial
                    self.GAME_STATE = "jogo"
                elif proximo_estado == "sair":
                    self.GAME_STATE = "sair"
            
            elif self.GAME_STATE == "final":
                self.GAME_STATE = "jogo"
                self.carregar_mapa("laboratorio_fechado", 667, 130) # Carrega o mapa inicial

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

                else:
                    # fallback para puzzle genérico
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
                        self.carregar_mapa("laboratorio", self.player.get_position_x(), self.player.get_position_y())
                        self.som_pegar_item.play()

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