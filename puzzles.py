from PPlay.gameimage import *
from PPlay.sprite import *
from Puzzles.puzzle_fabrica import*
senha_digitada = ""
cofre_esta_aberto = False
senha_correta = "senha"
tempo_tecla = 0

def puzzle_lab(janela, teclado, delta):
    global senha_digitada, cofre_esta_aberto, tempo_tecla

    largura_janela = janela.width
    altura_janela = janela.height

    if not hasattr(puzzle_lab, "cofre_fechado"):
        puzzle_lab.cofre_fechado = GameImage("assets/img/cofre_fechado.png")
        puzzle_lab.cofre_aberto = GameImage("assets/img/cofre_aberto.png")
        puzzle_lab.cofre_fechado.set_position(largura_janela/2 - puzzle_lab.cofre_fechado.width/2, altura_janela/1.4 - puzzle_lab.cofre_fechado.height/2)
        puzzle_lab.cofre_aberto.set_position(largura_janela/2 - puzzle_lab.cofre_fechado.width/2, altura_janela/1.4 - puzzle_lab.cofre_fechado.height/2)

    tempo_tecla += delta

    janela.set_background_color((0, 0, 50))

    janela.draw_text("pressione esc para sair", 10, 5, size=15, color=(200, 250, 250), bold=True)   

    if cofre_esta_aberto:
        janela.draw_text("COFRE ABERTO", largura_janela/2.5, altura_janela/10, size=20, color=(200, 200, 100), bold=True)
        janela.draw_text("Uma arma foi adicionada ao seus itens", largura_janela/3.5, altura_janela/6, size=20, color=(255, 255, 255), bold=True)
        janela.draw_text("Use as teclas direcionais mais espaço para disparar", largura_janela/5, altura_janela/4, size=20, color=(0, 255, 0), bold=True)
        puzzle_lab.cofre_aberto.draw()

        if teclado.key_pressed("esc"):

            return True  # Puzzle completo
    
    else:
        puzzle_lab.cofre_fechado.draw()

        janela.draw_text("use enter para confirmar e seta para esquerda para apagar", 380, 5, size=15, color=(100, 250, 250), bold=True)   

        janela.draw_text("O cofre parece familiar... na lateral há um enigma para a senha", largura_janela/6.5, altura_janela/6.5, size=20, color=(150, 200, 150), bold=True)

        janela.draw_text("''Todos me pedem, mas ninguém devia dizer.", largura_janela/4.2, altura_janela/3.5, size=20, color=(0, 150, 0), bold=True)
        janela.draw_text("Mesmo assim, sou exatamente o que você vai escrever.''", largura_janela/6, altura_janela/3, size=20, color=(0, 150, 0), bold=True)
        
        janela.draw_text("Digite a senha para abrir o cofre:", largura_janela/3.2, altura_janela/2.25, size=20, color=(255, 255, 255), bold=True)
        janela.draw_text(">", largura_janela/2.8, altura_janela/2, size=20, color=(0, 255, 0), bold=True)
        janela.draw_text(senha_digitada, largura_janela/2.6, altura_janela/2, size=20, color=(0, 255, 0), bold=True)

        for tecla in range(65, 91):  # letras A-Z
            if teclado.key_pressed(chr(tecla).lower()) and tempo_tecla >= 0.2:
                senha_digitada += chr(tecla).lower()
                tempo_tecla = 0
                break
        
        if teclado.key_pressed("left") and len(senha_digitada) > 0 and tempo_tecla >= 0.2:
            senha_digitada = senha_digitada[:-1]
            tempo_tecla = 0

        if teclado.key_pressed("enter"):
            if senha_digitada == senha_correta:
                cofre_esta_aberto = True
            else:
                janela.draw_text("INCORRETO", largura_janela/2.5, altura_janela/2, size=18, color=(255, 55, 50), bold=True)
                senha_digitada = ""

    return False  # Ainda não terminou

def puzzle_cadeado(janela, teclado, mouse, delta):
    if not hasattr(puzzle_cadeado, "estado"):
        puzzle_cadeado.estado = {
            "numeros_jogador": [1, 1, 1],
            "jogo_finalizado": False,
            "mouse_pressionado_anterior": False,
            "cadeado_aberto": Sprite("assets/img/cadeado_aberto.png"),
            "cadeado_fechado": Sprite("assets/img/cadeado_fechado.png"),
            "sprites_numeros": [GameImage(f"assets/img/{i}.png") for i in range(1, 10)],
            "botoes_cima": [],
            "botoes_baixo": [],
            "botao_confirma": Sprite("assets/img/abrir.png"),
            "tempo_tecla": 0,
            "dicas": [
                "Dicas:",
                "           1 3 4     Nenhum número está correto.",
                "           7 8 1     Um número está correto e no lugar certo.",
                "           4 5 6     Um número está correto mas no lugar errado.",
                "           8 5 3     Dois números estão corretos mas nos lugares errados.",
                "           9 7 5     Um número está correto mas no lugar errado."
            ]
        }

        estado = puzzle_cadeado.estado
        largura = janela.width
        altura = janela.height

        # Posições
        slot_w = estado["sprites_numeros"][0].width
        espaco = slot_w + 40
        x_inicial = largura / 2 - (3 * slot_w + 2 * (espaco - slot_w)) / 2
        y_slots = 150

        estado["posicoes_slots"] = [
            (x_inicial + i * espaco, y_slots) for i in range(3)
        ]

        # Botões cima e baixo
        y_botoes = y_slots + estado["sprites_numeros"][0].height + 10
        for i in range(3):
            x = estado["posicoes_slots"][i][0] + slot_w / 2
            cima = Sprite("assets/img/seta_cima.png")
            baixo = Sprite("assets/img/seta_baixo.png")
            cima.set_position(x - cima.width/2, y_botoes)
            baixo.set_position(x - baixo.width/2, y_botoes + cima.height + 5)
            estado["botoes_cima"].append(cima)
            estado["botoes_baixo"].append(baixo)

        estado["botao_confirma"].set_position(cima.x + cima.width + 30, cima.y)
        estado["cadeado_aberto"].set_position(largura / 2 - estado["cadeado_aberto"].width / 2, 50)
        estado["cadeado_fechado"].set_position(largura / 2 - estado["cadeado_fechado"].width / 2, 50)

    # Desenha
    janela.set_background_color((55, 155, 155))
    estado = puzzle_cadeado.estado
    if estado["jogo_finalizado"]:
        estado["cadeado_aberto"].draw()
    else:
        janela.draw_text("pressione esc para sair", 10, 5, size=15, color=(200, 250, 250), bold=True)   
        estado["cadeado_fechado"].draw()

    # Números
    for i in range(3):
        sprite = estado["sprites_numeros"][estado["numeros_jogador"][i] - 1]
        x, y = estado["posicoes_slots"][i]
        sprite.set_position(x, y)
        sprite.draw()

    for btn in estado["botoes_cima"] + estado["botoes_baixo"]:
        btn.draw()

    estado["botao_confirma"].draw()

    # Dicas
    for i, dica in enumerate(estado["dicas"]):
        janela.draw_text(dica, 20, 300 + i*20, 18, (0,0,0))

    # Clique
    clique = mouse.is_button_pressed(1)
    if not estado["jogo_finalizado"] and clique and not estado["mouse_pressionado_anterior"]:
        for i in range(3):
            if mouse.is_over_object(estado["botoes_cima"][i]):
                estado["numeros_jogador"][i] = estado["numeros_jogador"][i] % 9 + 1
                break
            if mouse.is_over_object(estado["botoes_baixo"][i]):
                estado["numeros_jogador"][i] = 9 if estado["numeros_jogador"][i] == 1 else estado["numeros_jogador"][i] - 1
                break
        if mouse.is_over_object(estado["botao_confirma"]):
            if estado["numeros_jogador"] == [5, 8, 2]:
                estado["jogo_finalizado"] = True
                
    estado["mouse_pressionado_anterior"] = clique

    if estado["jogo_finalizado"]:
        janela.draw_text("Cadeado aberto! O código era 582", janela.width/3.3, 260, 20, (0,255,0))
        if teclado.key_pressed("esc"):
            return True

    return False

def puzzle_lampadas(janela, teclado, mouse, delta):
    if not hasattr(puzzle_lampadas, "init"):
        puzzle_lampadas.estado = {
            "lampadas": [False]*8,
            "img_on": GameImage("assets/img/lamp_acesa.png").image,
            "img_off": GameImage("assets/img/lamp_apagada.png").image,
            "lamp_sprites": [],
            "botoes": [],
            "tempo_tecla": 0,
            "fundo": GameImage("assets/img/puzzle.png")
        }

        estado = puzzle_lampadas.estado

        for i in range(8):
            sprite = Sprite("assets/img/lamp_apagada.png", 1)
            x = 125 + (i % 4) * 150
            y = 80 if i < 4 else 220
            sprite.set_position(x, y)
            estado["lamp_sprites"].append(sprite)

        for i in range(6):
            botao = Sprite(f"assets/img/botao_{i}.png", 1)
            x = 150 + (i % 3) * 170
            y = 400 + (i // 3) * 100
            botao.set_position(x, y)
            estado["botoes"].append(botao)

        estado["acoes_botoes"] = [
            [0, 1, 2],
            [4, 6, 7],
            [5, 6],
            [1, 3],
            [2, 3, 4],
            [2, 7]
        ]

        puzzle_lampadas.init = True

    estado = puzzle_lampadas.estado
    estado["tempo_tecla"] += delta
    estado["fundo"].draw()

    for i, ligado in enumerate(estado["lampadas"]):
        estado["lamp_sprites"][i].image = estado["img_on"] if ligado else estado["img_off"]
        estado["lamp_sprites"][i].draw()

    for botao in estado["botoes"]:
        botao.draw()

    janela.draw_text("Cumpra a rotina de segurança para habilitar o sistema.", 50, 30, 24, (0, 100, 0), "Consolas", True)

    if all(estado["lampadas"]):
        janela.draw_text("Rotina completa! Portas destravadas.", 170, 345, 24, (210, 100, 30), "Consolas", True)
        if teclado.key_pressed("esc"):
            return True

    if mouse.is_button_pressed(1) and estado["tempo_tecla"] > 0.2:
        for i, botao in enumerate(estado["botoes"]):
            if mouse.is_over_object(botao):
                for idx in estado["acoes_botoes"][i]:
                    estado["lampadas"][idx] = not estado["lampadas"][idx]
                estado["tempo_tecla"] = 0
                break

    return False


def resetar_puzzle_lab():
    global senha_digitada, cofre_esta_aberto, tempo_tecla
    senha_digitada = ""
    cofre_esta_aberto = False
    tempo_tecla = 0
    if hasattr(puzzle_lab, "cofre_fechado"):
        del puzzle_lab.cofre_fechado
    if hasattr(puzzle_lab, "cofre_aberto"):
        del puzzle_lab.cofre_aberto

def resetar_puzzle_cadeado():
    if hasattr(puzzle_cadeado, "estado"):
        del puzzle_cadeado.estado

def resetar_puzzle_lampadas():
    if hasattr(puzzle_lampadas, "estado"):
        del puzzle_lampadas.estado
    if hasattr(puzzle_lampadas, "init"):
        del puzzle_lampadas.init

def puzzle_hosp():
    return False
def puzzle_fabrica(janela, mouse):
    puzzle_fb = SequencePuzzle(janela, mouse)
    while True:
        puzzle_fb.update()
        puzzle_fb.draw()
        janela.update()