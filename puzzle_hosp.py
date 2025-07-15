from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
import random

janela = Window(800, 600)
janela.set_title("Puzzle de Arrastar")
mouse = Mouse()

# Classe da peça
class Peca:
    def __init__(self, imagem, pos_final):
        self.img = GameImage(imagem)
        self.pos_final = pos_final
        self.pos_atual = [0, 0]
        self.selecionada = False

    def desenhar(self):
        self.img.set_position(*self.pos_atual)
        self.img.draw()

    def esta_no_lugar(self):
        x, y = self.pos_atual
        xf, yf = self.pos_final
        return abs(x - xf) < 10 and abs(y - yf) < 10

# Centralizar grade 3x3 de peças 100x100
tamanho_peca = 100
margem_x = (janela.width - (tamanho_peca * 3)) // 2  # 800 - 300 = 250
margem_y = (janela.height - (tamanho_peca * 3)) // 2  # 600 - 300 = 150

pecas = []
for i in range(3):
    for j in range(3):
        idx = i * 3 + j + 1
        caminho = f"assets/img/p{idx}.png"
        pos_final = (j * tamanho_peca + margem_x, i * tamanho_peca + margem_y)
        pecas.append(Peca(caminho, pos_final))

# Embaralhar posições iniciais
posicoes_iniciais = [peca.pos_final for peca in pecas]
random.shuffle(posicoes_iniciais)
for i, peca in enumerate(pecas):
    peca.pos_atual = list(posicoes_iniciais[i])

peca_selecionada = None
mensagem = ""

while True:
    janela.set_background_color((245, 245, 245))

    # Texto de instrução
    janela.draw_text("Arraste as peças para montar a imagem!", 220, 20, size=26, color=(30, 30, 30))

    # Evento de clique
    if mouse.is_button_pressed(1):
        if not peca_selecionada:
            for peca in reversed(pecas):
                if mouse.is_over_object(peca.img):
                    peca_selecionada = peca
                    break
    else:
        if peca_selecionada:
            if peca_selecionada.esta_no_lugar():
                peca_selecionada.pos_atual = list(peca_selecionada.pos_final)
            peca_selecionada = None

    # Mover peça com o mouse
    if peca_selecionada:
        pos_mouse = mouse.get_position()
        peca_selecionada.pos_atual = [pos_mouse[0] - 50, pos_mouse[1] - 50]

    # Desenhar peças
    for peca in pecas:
        peca.desenhar()

    # Verificar resolução
    if all(p.esta_no_lugar() for p in pecas):
        mensagem = "Puzzle resolvido!"

    if mensagem:
        janela.draw_text(mensagem, janela.width // 2 - 120, janela.height - 40, size=28, color=(0, 128, 0))

    janela.update()
