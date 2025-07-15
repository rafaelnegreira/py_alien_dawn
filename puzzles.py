from PPlay.gameimage import *
from PPlay.sprite import *
import pygame
import os
import random

# Obtém o diretório do script para construir caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(*path_parts):
    """Constrói um caminho absoluto para um asset."""
    return os.path.join(BASE_DIR, *path_parts)

senha_digitada = ""
cofre_esta_aberto = False
senha_correta = "senha"
tempo_tecla = 0

def puzzle_lab(janela, teclado, delta):
    
    largura_janela = janela.width
    altura_janela = janela.height
    
    global senha_digitada, cofre_esta_aberto, tempo_tecla

    if not hasattr(puzzle_lab, "cofre_fechado"):
        puzzle_lab.cofre_fechado = GameImage(get_asset_path("assets", "img", "cofre_fechado.png"))
        puzzle_lab.cofre_aberto = GameImage(get_asset_path("assets", "img", "cofre_aberto.png"))
        puzzle_lab.cofre_fechado.set_position(janela.width/2 - puzzle_lab.cofre_fechado.width/2, janela.height/1.4 - puzzle_lab.cofre_fechado.height/2)
        puzzle_lab.cofre_aberto.set_position(janela.width/2 - puzzle_lab.cofre_fechado.width/2, janela.height/1.4 - puzzle_lab.cofre_fechado.height/2)

    tempo_tecla += delta
    janela.set_background_color((0, 0, 50))
    janela.draw_text("pressione esc para sair", 10, 5, size=15, color=(200, 250, 250), bold=True)   

    if cofre_esta_aberto:
        janela.draw_text("COFRE ABERTO", janela.width/2.5, janela.height/10, size=20, color=(200, 200, 100), bold=True)
        janela.draw_text("Uma arma foi adicionada ao seus itens", janela.width/3.5, janela.height/6, size=20, color=(255, 255, 255), bold=True)
        janela.draw_text("Use as teclas direcionais mais espaço para disparar", janela.width/5, janela.height/4, size=20, color=(0, 255, 0), bold=True)
        puzzle_lab.cofre_aberto.draw()
        if teclado.key_pressed("esc"):
            return True
    else:
        puzzle_lab.cofre_fechado.draw()
        janela.draw_text("use enter para confirmar e seta para esquerda para apagar", 380, 5, size=15, color=(100, 250, 250), bold=True)   
        janela.draw_text("O cofre parece familiar... na lateral há um enigma para a senha", janela.width/6.5, janela.height/6.5, size=20, color=(150, 200, 150), bold=True)
        janela.draw_text("''Todos me pedem, mas ninguém devia dizer.", janela.width/4.2, janela.height/3.5, size=20, color=(0, 150, 0), bold=True)
        janela.draw_text("Mesmo assim, sou exatamente o que você vai escrever.''", janela.width/6, janela.height/3, size=20, color=(0, 150, 0), bold=True)
        janela.draw_text("Digite a senha para abrir o cofre:", janela.width/3.2, janela.height/2.25, size=20, color=(255, 255, 255), bold=True)
        janela.draw_text(">", janela.width/2.8, janela.height/2, size=20, color=(0, 255, 0), bold=True)
        janela.draw_text(senha_digitada, janela.width/2.6, janela.height/2, size=20, color=(0, 255, 0), bold=True)

        for tecla in range(ord('a'), ord('z') + 1):
            if teclado.key_pressed(chr(tecla)) and tempo_tecla >= 0.2:
                senha_digitada += chr(tecla)
                tempo_tecla = 0
                break
        
        if teclado.key_pressed("left") and len(senha_digitada) > 0 and tempo_tecla >= 0.2:
            senha_digitada = senha_digitada[:-1]
            tempo_tecla = 0

        if teclado.key_pressed("enter"):
            if senha_digitada == senha_correta:
                cofre_esta_aberto = True
            else:
                janela.draw_text("INCORRETO", janela.width/2.5, altura_janela/2, size=18, color=(255, 55, 50), bold=True)
                senha_digitada = ""

    return False

def puzzle_cadeado(janela, teclado, mouse, delta):
    if not hasattr(puzzle_cadeado, "estado"):
        puzzle_cadeado.estado = {
            "numeros_jogador": [1, 1, 1], "jogo_finalizado": False, "mouse_pressionado_anterior": False,
            "cadeado_aberto": Sprite(get_asset_path("assets", "img", "cadeado_aberto.png")),
            "cadeado_fechado": Sprite(get_asset_path("assets", "img", "cadeado_fechado.png")),
            "sprites_numeros": [GameImage(get_asset_path("assets", "img", f"{i}.png")) for i in range(1, 10)],
            "botoes_cima": [], "botoes_baixo": [],
            "botao_confirma": Sprite(get_asset_path("assets", "img", "abrir.png")), "tempo_tecla": 0,
            "dicas": [
                "Dicas:", "           1 3 4     Nenhum número está correto.", "           7 8 1     Um número está correto e no lugar certo.",
                "           4 5 6     Um número está correto mas no lugar errado.", "           8 5 3     Dois números estão corretos mas nos lugares errados.",
                "           9 7 5     Um número está correto mas no lugar errado."
            ]
        }
        estado = puzzle_cadeado.estado
        slot_w = estado["sprites_numeros"][0].width; espaco = slot_w + 40
        x_inicial = janela.width / 2 - (3 * slot_w + 2 * (espaco - slot_w)) / 2; y_slots = 150
        estado["posicoes_slots"] = [(x_inicial + i * espaco, y_slots) for i in range(3)]
        y_botoes = y_slots + estado["sprites_numeros"][0].height + 10
        for i in range(3):
            x = estado["posicoes_slots"][i][0] + slot_w / 2
            cima = Sprite(get_asset_path("assets", "img", "seta_cima.png")); baixo = Sprite(get_asset_path("assets", "img", "seta_baixo.png"))
            cima.set_position(x - cima.width/2, y_botoes); baixo.set_position(x - baixo.width/2, y_botoes + cima.height + 5)
            estado["botoes_cima"].append(cima); estado["botoes_baixo"].append(baixo)
        estado["botao_confirma"].set_position(cima.x + cima.width + 30, cima.y)
        estado["cadeado_aberto"].set_position(janela.width / 2 - estado["cadeado_aberto"].width / 2, 50)
        estado["cadeado_fechado"].set_position(janela.width / 2 - estado["cadeado_fechado"].width / 2, 50)

    janela.set_background_color((55, 155, 155)); estado = puzzle_cadeado.estado
    if estado["jogo_finalizado"]: estado["cadeado_aberto"].draw()
    else:
        janela.draw_text("pressione esc para sair", 10, 5, size=15, color=(200, 250, 250), bold=True); estado["cadeado_fechado"].draw()
    for i in range(3):
        sprite = estado["sprites_numeros"][estado["numeros_jogador"][i] - 1]; x, y = estado["posicoes_slots"][i]
        sprite.set_position(x, y); sprite.draw()
    for btn in estado["botoes_cima"] + estado["botoes_baixo"]: btn.draw()
    estado["botao_confirma"].draw()
    for i, dica in enumerate(estado["dicas"]): janela.draw_text(dica, 20, 300 + i*20, 18, (0,0,0))

    clique = mouse.is_button_pressed(1)
    if not estado["jogo_finalizado"] and clique and not estado["mouse_pressionado_anterior"]:
        for i in range(3):
            if mouse.is_over_object(estado["botoes_cima"][i]): estado["numeros_jogador"][i] = estado["numeros_jogador"][i] % 9 + 1; break
            if mouse.is_over_object(estado["botoes_baixo"][i]): estado["numeros_jogador"][i] = 9 if estado["numeros_jogador"][i] == 1 else estado["numeros_jogador"][i] - 1; break
        if mouse.is_over_object(estado["botao_confirma"]):
            if estado["numeros_jogador"] == [5, 8, 2]: estado["jogo_finalizado"] = True
    estado["mouse_pressionado_anterior"] = clique

    if estado["jogo_finalizado"]:
        janela.draw_text("Cadeado aberto! O código era 582", janela.width/3.3, 260, 20, (0,255,0))
        if teclado.key_pressed("esc"): return True
    return False

def puzzle_lampadas(janela, teclado, mouse, delta):
    if not hasattr(puzzle_lampadas, "init"):
        puzzle_lampadas.estado = {
            "lampadas": [False]*8, "img_on": GameImage(get_asset_path("assets", "img", "lamp_acesa.png")).image,
            "img_off": GameImage(get_asset_path("assets", "img", "lamp_apagada.png")).image, "lamp_sprites": [],
            "botoes": [], "tempo_tecla": 0, "fundo": GameImage(get_asset_path("assets", "img", "puzzle.png"))
        }
        estado = puzzle_lampadas.estado
        for i in range(8):
            sprite = Sprite(get_asset_path("assets", "img", "lamp_apagada.png"), 1); x = 125 + (i % 4) * 150; y = 80 if i < 4 else 220
            sprite.set_position(x, y); estado["lamp_sprites"].append(sprite)
        for i in range(6):
            botao = Sprite(get_asset_path("assets", "img", f"botao_{i}.png"), 1); x = 150 + (i % 3) * 170; y = 400 + (i // 3) * 100
            botao.set_position(x, y); estado["botoes"].append(botao)
        estado["acoes_botoes"] = [[0, 1, 2], [4, 6, 7], [5, 6], [1, 3], [2, 3, 4], [2, 7]]
        puzzle_lampadas.init = True

    estado = puzzle_lampadas.estado; estado["tempo_tecla"] += delta; estado["fundo"].draw()
    for i, ligado in enumerate(estado["lampadas"]):
        estado["lamp_sprites"][i].image = estado["img_on"] if ligado else estado["img_off"]; estado["lamp_sprites"][i].draw()
    for botao in estado["botoes"]: botao.draw()
    janela.draw_text("Cumpra a rotina de segurança para habilitar o sistema.", 50, 30, 24, (0, 100, 0), "Consolas", True)

    if all(estado["lampadas"]):
        janela.draw_text("Rotina completa! Portas destravadas.", 170, 345, 24, (210, 100, 30), "Consolas", True)
        if teclado.key_pressed("esc"): return True

    if mouse.is_button_pressed(1) and estado["tempo_tecla"] > 0.2:
        for i, botao in enumerate(estado["botoes"]):
            if mouse.is_over_object(botao):
                for idx in estado["acoes_botoes"][i]: estado["lampadas"][idx] = not estado["lampadas"][idx]
                estado["tempo_tecla"] = 0; break
    return False

def resetar_puzzle_lab():
    global senha_digitada, cofre_esta_aberto, tempo_tecla
    senha_digitada = ""; cofre_esta_aberto = False; tempo_tecla = 0
    if hasattr(puzzle_lab, "cofre_fechado"): del puzzle_lab.cofre_fechado
    if hasattr(puzzle_lab, "cofre_aberto"): del puzzle_lab.cofre_aberto

def resetar_puzzle_cadeado():
    if hasattr(puzzle_cadeado, "estado"): del puzzle_cadeado.estado

def resetar_puzzle_lampadas():
    if hasattr(puzzle_lampadas, "init"): del puzzle_lampadas.init

def puzzle_hospital(janela, teclado, mouse):
    if not hasattr(puzzle_hospital, "pecas"):
        class Peca:
            def __init__(self, imagem, pos_final):
                self.img = GameImage(imagem); self.pos_final = pos_final
                self.pos_atual = [0, 0]; self.selecionada = False
            def desenhar(self): self.img.set_position(*self.pos_atual); self.img.draw()
            def esta_no_lugar(self):
                return abs(self.pos_atual[0] - self.pos_final[0]) < 10 and abs(self.pos_atual[1] - self.pos_final[1]) < 10

        tamanho_peca = 100
        margem_x = (janela.width - (tamanho_peca * 3)) // 2; margem_y = (janela.height - (tamanho_peca * 3)) // 2
        pecas = []
        for i in range(3):
            for j in range(3):
                caminho = get_asset_path("assets", "img", f"p{i * 3 + j + 1}.png")
                pos_final = (j * tamanho_peca + margem_x, i * tamanho_peca + margem_y)
                pecas.append(Peca(caminho, pos_final))
        
        posicoes_iniciais = [p.pos_final for p in pecas]; random.shuffle(posicoes_iniciais)
        for i, peca in enumerate(pecas): peca.pos_atual = list(posicoes_iniciais[i])
        puzzle_hospital.pecas = pecas; puzzle_hospital.peca_selecionada = None; puzzle_hospital.mensagem = ""

    janela.set_background_color((245, 245, 245))
    janela.draw_text("Arraste as peças para montar a imagem!", 220, 20, size=26, color=(30, 30, 30))
    janela.draw_text("pressione ESC para sair", 10, 5, size=15, color=(100, 100, 100))

    if mouse.is_button_pressed(1):
        if not puzzle_hospital.peca_selecionada:
            for peca in reversed(puzzle_hospital.pecas):
                if mouse.is_over_object(peca.img): puzzle_hospital.peca_selecionada = peca; break
    else:
        if puzzle_hospital.peca_selecionada:
            if puzzle_hospital.peca_selecionada.esta_no_lugar(): puzzle_hospital.peca_selecionada.pos_atual = list(puzzle_hospital.peca_selecionada.pos_final)
            puzzle_hospital.peca_selecionada = None

    if puzzle_hospital.peca_selecionada:
        pos_mouse = mouse.get_position()
        puzzle_hospital.peca_selecionada.pos_atual = [pos_mouse[0] - 50, pos_mouse[1] - 50]

    for p in puzzle_hospital.pecas: p.desenhar()

    if all(p.esta_no_lugar() for p in puzzle_hospital.pecas): puzzle_hospital.finalizado = True

    if hasattr(puzzle_hospital, "finalizado") and puzzle_hospital.finalizado:
        janela.draw_text("Puzzle resolvido! Pressione ESC para sair.", janela.width // 2 - 200, janela.height - 40, size=28, color=(0, 128, 0))
        if teclado.key_pressed("esc"): return True

    return False

def resetar_puzzle_hospital():
    attrs_to_del = ["pecas", "peca_selecionada", "mensagem", "finalizado"]
    for attr in attrs_to_del:
        if hasattr(puzzle_hospital, attr): delattr(puzzle_hospital, attr)

def puzzle_luzes(janela, teclado, mouse):
    if not hasattr(puzzle_luzes, "grid"):
        pygame.mixer.init()
        puzzle_luzes.som_click = pygame.mixer.Sound(get_asset_path("assets", "sounds", "click.wav"))
        puzzle_luzes.GRID_SIZE = 4; puzzle_luzes.TAM = 100
        puzzle_luzes.OFFSET_X = (janela.width - (puzzle_luzes.TAM * puzzle_luzes.GRID_SIZE)) // 2
        puzzle_luzes.OFFSET_Y = (janela.height - (puzzle_luzes.TAM * puzzle_luzes.GRID_SIZE)) // 2
        puzzle_luzes.grid = [[1 for _ in range(puzzle_luzes.GRID_SIZE)] for _ in range(puzzle_luzes.GRID_SIZE)]
        puzzle_luzes.mensagem = ""; puzzle_luzes.resolvido = False

    GRID_SIZE, TAM, OFFSET_X, OFFSET_Y, grid = puzzle_luzes.GRID_SIZE, puzzle_luzes.TAM, puzzle_luzes.OFFSET_X, puzzle_luzes.OFFSET_Y, puzzle_luzes.grid

    def alternar(i, j):
        if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE: grid[i][j] = 1 - grid[i][j]

    janela.set_background_color((30, 30, 30))
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cor = (255, 255, 0) if grid[i][j] else (100, 100, 100)
            pygame.draw.rect(janela.screen, cor, (j * TAM + OFFSET_X, i * TAM + OFFSET_Y, TAM - 5, TAM - 5))

    if not puzzle_luzes.resolvido and all(cell == 0 for row in grid for cell in row):
        puzzle_luzes.mensagem = "Puzzle resolvido!"; puzzle_luzes.resolvido = True

    janela.draw_text("Apague todas as luzes!", 280, 40, size=26, color=(255, 255, 255))
    if puzzle_luzes.mensagem: janela.draw_text(puzzle_luzes.mensagem, janela.width // 2 - 110, 550, size=30, color=(0, 255, 0))

    if mouse.is_button_pressed(1) and not puzzle_luzes.resolvido:
        mx, my = mouse.get_position()
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if (j * TAM + OFFSET_X) <= mx <= (j * TAM + OFFSET_X + TAM) and (i * TAM + OFFSET_Y) <= my <= (i * TAM + OFFSET_Y + TAM):
                    alternar(i, j); alternar(i - 1, j); alternar(i + 1, j); alternar(i, j - 1); alternar(i, j + 1)
                    puzzle_luzes.som_click.play(); janela.delay(250); break
    
    if puzzle_luzes.resolvido and teclado.key_pressed("esc"): return True
    return False

def resetar_puzzle_luzes():
    attrs_to_del = ["grid", "mensagem", "resolvido", "som_click"]
    for attr in attrs_to_del:
        if hasattr(puzzle_luzes, attr): delattr(puzzle_luzes, attr)