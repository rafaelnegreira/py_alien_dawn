from PPlay.gameimage import *

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

    if cofre_esta_aberto:
        janela.draw_text("COFRE ABERTO", largura_janela/2.7, altura_janela/10, size=20, color=(200, 200, 100), bold=True)
        janela.draw_text("Uma arma foi adicionada ao seus itens", largura_janela/5, altura_janela/6, size=20, color=(255, 255, 255), bold=True)
        janela.draw_text("Use as teclas direcionais mais espaço para disparar", largura_janela/10, altura_janela/4, size=20, color=(0, 255, 0), bold=True)
        puzzle_lab.cofre_aberto.draw()
        return True  # Puzzle completo
    else:
        puzzle_lab.cofre_fechado.draw()
        janela.draw_text("Todos me pedem, mas ninguém devia dizer.", largura_janela/4.5, altura_janela/10, size=20, color=(0, 150, 0), bold=True)
        janela.draw_text("Mesmo assim, sou exatamente o que você vai escrever.", largura_janela/6, altura_janela/6, size=20, color=(0, 150, 0), bold=True)
        
        janela.draw_text("Digite a senha para abrir o cofre:", largura_janela/3.5, altura_janela/2.8, size=20, color=(255, 255, 255), bold=True)
        janela.draw_text(">", largura_janela/2.8, altura_janela/2.3, size=20, color=(0, 255, 0), bold=True)
        janela.draw_text(senha_digitada, largura_janela/2.5, altura_janela/2.3, size=20, color=(0, 255, 0), bold=True)

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
                janela.draw_text("INCORRETO", largura_janela/2.4, altura_janela/2.29, size=18, color=(255, 55, 50), bold=True)
                senha_digitada = ""

    return False  # Ainda não terminou
