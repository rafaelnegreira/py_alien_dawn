from PPlay.window import Window
from PPlay.mouse import Mouse
import pygame

# Inicializar PPlay e Pygame mixer
janela = Window(800, 600)
janela.set_title("Puzzle de Luzes 4x4")
mouse = Mouse()
pygame.mixer.init()

# Som de clique
som_click = pygame.mixer.Sound("assets\sounds\click.wav")

# Tamanho e grade
TAM = 100
GRID_SIZE = 4

# Offsets para centralizar a grade 4x4
OFFSET_X = (janela.width - (TAM * GRID_SIZE)) // 2  # (800 - 400) // 2 = 200
OFFSET_Y = (janela.height - (TAM * GRID_SIZE)) // 2  # (600 - 400) // 2 = 100

# Estado das luzes (1 = ligado, 0 = desligado)
grid = [[1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def desenhar_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = j * TAM + OFFSET_X
            y = i * TAM + OFFSET_Y
            cor = (255, 255, 0) if grid[i][j] else (100, 100, 100)
            pygame.draw.rect(janela.screen, cor, (x, y, TAM - 5, TAM - 5))

def alternar(i, j):
    if 0 <= i < GRID_SIZE and 0 <= j < GRID_SIZE:
        grid[i][j] = 1 - grid[i][j]

mensagem = ""

while True:
    janela.set_background_color((30, 30, 30))
    desenhar_grid()

    if all(cell == 0 for row in grid for cell in row):
        mensagem = "🎉 Puzzle resolvido!"

    janela.draw_text("Apague todas as luzes!", 280, 40, size=26, color=(255, 255, 255))
    if mensagem:
        janela.draw_text(mensagem, janela.width // 2 - 130, 550, size=30, color=(0, 255, 0))

    if mouse.is_button_pressed(1):
        mx, my = mouse.get_position()
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x = j * TAM + OFFSET_X
                y = i * TAM + OFFSET_Y
                if x <= mx <= x + TAM and y <= my <= y + TAM:
                    alternar(i, j)
                    alternar(i - 1, j)
                    alternar(i + 1, j)
                    alternar(i, j - 1)
                    alternar(i, j + 1)
                    som_click.play()
                    janela.delay(250)
                    break

    janela.update()
