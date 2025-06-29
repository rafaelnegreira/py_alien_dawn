import pygame
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.keyboard import *

# --- Configurações Iniciais ---
LARGURA_JANELA = 600
ALTURA_JANELA = 400

# Cores
BRANCO = (55, 155, 155)
PRETO = (0, 0, 0)
VERDE_CLARO = (150, 255, 150)

CODIGO_SECRETO = [5, 8, 2]

# Inicialização da Janela e Mouse
janela = Window(LARGURA_JANELA, ALTURA_JANELA)
mouse = Window.get_mouse()
teclado = Keyboard()

# --- Carregamento de Assets ---
# Imagem do Cadeado

cadeado_fechado = Sprite("assets/img/cadeado_fechado.png")
cadeado_fechado.set_position(LARGURA_JANELA / 2 - cadeado_fechado.width / 2, 50)

cadeado_aberto = Sprite("assets/img/cadeado_aberto.png")
cadeado_aberto.set_position(LARGURA_JANELA / 2 - cadeado_aberto.width / 2, 50)

cadeado_img = cadeado_fechado

# Imagens dos Números (1-9)
numeros_spritesheet = []
for i in range(1, 10):
    numeros_spritesheet.append(GameImage(f"assets/img/{i}.png"))

# --- Configuração dos Elementos do Jogo ---
# Posições dos slots dos números
espaco_entre_slots = numeros_spritesheet[0].width + 40
largura_total_slots = 3 * numeros_spritesheet[0].width + 2 * (espaco_entre_slots - numeros_spritesheet[0].width)
x_inicial_slots = LARGURA_JANELA / 2 - largura_total_slots / 2
y_slots = cadeado_img.y + cadeado_img.height + 30

posicoes_slots = [
    (x_inicial_slots, y_slots),
    (x_inicial_slots + espaco_entre_slots, y_slots),
    (x_inicial_slots + 2 * espaco_entre_slots, y_slots)
]

# Sprites dos Botões

botao_confirma = Sprite("assets/img/abrir.png")
botao_confirma.set_position(440, 165)

botoes_cima = []
botoes_baixo = []
y_offset_botao = numeros_spritesheet[0].height + 10 # Distância abaixo do número
largura_numero = numeros_spritesheet[0].width

for i in range(3):
    x_slot = posicoes_slots[i][0]
    y_base_botoes = posicoes_slots[i][1] + y_offset_botao

    # Botão Cima
    btn_c = Sprite("assets/img/seta_cima.png")
    btn_c.set_position(x_slot + largura_numero / 2 - btn_c.width / 2, y_base_botoes)
    botoes_cima.append(btn_c)

    # Botão Baixo
    btn_b = Sprite("assets/img/seta_baixo.png")
    btn_b.set_position(x_slot + largura_numero / 2 - btn_b.width / 2, y_base_botoes + btn_c.height + 5)
    botoes_baixo.append(btn_b)

# Estado inicial dos números do jogador
numeros_jogador = [1, 1, 1] # Começa com 1, 1, 1

# Controle de clique do mouse (para evitar múltiplos incrementos)
mouse_pressionado_anterior = False

# Estado do jogo
jogo_finalizado = False
mensagem_vitoria = "Cadeado aberto! O código era " + "".join(map(str, CODIGO_SECRETO))

# --- Textos das Dicas ---
dicas = [
    "Dicas:",
    "           1 3 4     Nenhum número está correto.",
    "           7 8 1     Um número está correto e no lugar certo.",
    "           4 5 6     Um número está correto mas no lugar errado.",
    "           8 5 3     Dois números estão corretos mas nos lugares errados.",
    "           9 7 5     Um número está correto mas no lugar errado."
]
y_dicas_inicio = botoes_baixo[0].y + botoes_baixo[0].height + 10
tamanho_fonte_dicas = 18
cor_dicas = PRETO
espacamento_dicas = 20

# --- Loop Principal do Jogo ---
while True:
    janela.set_background_color(BRANCO)

    # Desenhar cadeado
    cadeado_img.draw()
    
    botao_confirma.draw()

    # Desenhar os números atuais nos slots
    for i in range(3):
        num_atual = numeros_jogador[i]
        # Os sprites dos números são indexados de 0 a 8 (para números 1 a 9)
        sprite_num = numeros_spritesheet[num_atual - 1]
        sprite_num.set_position(posicoes_slots[i][0], posicoes_slots[i][1])
        sprite_num.draw()

    # Desenhar botões
    if not jogo_finalizado:
        for i in range(3):
            botoes_cima[i].draw()
            botoes_baixo[i].draw()

    # Desenhar dicas
    for i, dica_texto in enumerate(dicas):
        janela.draw_text(dica_texto, 20, y_dicas_inicio + i * espacamento_dicas,
                          size=tamanho_fonte_dicas, color=cor_dicas, font_name="Arial", bold=False)

    janela.draw_text("Pressione ESC para sair",
                        20,
                        10,
                        size=14, color=PRETO, font_name="Arial", bold=True)

    # Lógica de Interação com Botões (apenas se o jogo não terminou)
    if not jogo_finalizado:

        clique_mouse_atual = mouse.is_button_pressed(1) # Botão esquerdo

        if clique_mouse_atual and not mouse_pressionado_anterior:
            for i in range(3):
                # Botões de Cima
                if mouse.is_over_object(botoes_cima[i]):
                    numeros_jogador[i] += 1
                    if numeros_jogador[i] > 9:
                        numeros_jogador[i] = 1 # Volta para 1
                    break # Processa um botão por clique

                # Botões de Baixo
                if mouse.is_over_object(botoes_baixo[i]):
                    numeros_jogador[i] -= 1
                    if numeros_jogador[i] < 1:
                        numeros_jogador[i] = 9 # Volta para 9
                    break # Processa um botão por clique
                    
                if mouse.is_over_object(botao_confirma):
                    if numeros_jogador == CODIGO_SECRETO:
                        jogo_finalizado = True
                    
        mouse_pressionado_anterior = clique_mouse_atual

    # Exibir mensagem de vitória
    if jogo_finalizado:
        janela.draw_text(mensagem_vitoria,
                          LARGURA_JANELA / 4,
                          ALTURA_JANELA / 2.6 - 40 / 2,
                          size=19, color=VERDE_CLARO, font_name="Arial", bold=True)

        cadeado_img = cadeado_aberto

    if teclado.key_pressed("esc"):
        janela.close()

    janela.update()