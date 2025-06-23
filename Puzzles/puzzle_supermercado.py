from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.keyboard import *
from random import randint

janela = Window(800, 600)
janela.set_title("Puzzle das Lâmpadas")
teclado = Window.get_keyboard()
mouse = Window.get_mouse()

lampadas = [False] * 8

# Lâmpadas em duas linhas de 4
lamp_sprites = []
for i in range(8):
    sprite = Sprite("assets/img/lamp_apagada.png", 1)
    x = 125 + (i % 4) * 150
    y = 80 if i < 4 else 220
    sprite.set_position(x, y)
    lamp_sprites.append(sprite)

# Botões com sprites únicos
# Botões com sprites únicos organizados em 2 linhas de 3
botoes = []
for i in range(6):
    botao = Sprite(f"assets/img/botao_{i}.png", 1)
    x = 150 + (i % 3) * 170  # 3 colunas
    y = 400 + (i // 3) * 100  # 2 linhas
    botao.set_position(x, y)
    botoes.append(botao)


# Ações dos botões
acoes_botoes = [
    [0, 1, 2],      # boot_sequence: CPU, MEM, GPU
    [4, 6, 7],      # firmware_patch: PWR, BIOS, BUS
    [5, 6],         # power_cycle: PWR, BIOS
    [1, 3],         # diagnostic_check: MEM, NET
    [2, 3, 4],      # enable_peripherals: GPU, NET, SND
    [2, 7],         # reset_network: GPU, BUS
]

def alternar_lampadas(indices):
    for i in indices:
        lampadas[i] = not lampadas[i]

img_on = GameImage("assets/img/lamp_acesa.png").image
img_off = GameImage("assets/img/lamp_apagada.png").image

def atualizar_lampadas():
    for i, estado in enumerate(lampadas):
        lamp_sprites[i].image = img_on if estado else img_off

def todas_ligadas():
    return all(lampadas)

tempo_tecla = janela.time_elapsed()

fundo = GameImage("assets/img/puzzle.png")

while True:

    janela.set_background_color((230, 230, 230))
    fundo.draw()
    atualizar_lampadas()

    janela.draw_text("Cumpra a rotina de segurança para habilitar o sistema.", 50, 30, 24, (0, 100, 0), "Consolas", True)

    for lamp in lamp_sprites:
        lamp.draw()

    for botao in botoes:
        botao.draw()

    if todas_ligadas():
        janela.draw_text("Rotina completa! Portas de segurança destravadas.", 90, 345, 24, (210, 100, 30), "Consolas", True)

    if mouse.is_button_pressed(1) and janela.time_elapsed() - tempo_tecla >= 200:
        for i, botao in enumerate(botoes):
            if mouse.is_over_object(botao):
                alternar_lampadas(acoes_botoes[i])
                break
        tempo_tecla = janela.time_elapsed()

    if teclado.key_pressed("esc"):
        janela.close()

    janela.update()
