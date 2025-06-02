from PPlay.window import *
from PPlay.gameimage import *
from PPlay.keyboard import *

janela = Window(600, 400)
janela.set_title("Cofre Secreto")
teclado = Window.get_keyboard()

largura_janela = janela.width
altura_janela = janela.height

cofre_fechado = GameImage("img\cofre_fechado.png")
cofre_aberto = GameImage("img\cofre_aberto.png")
cofre_fechado.set_position(largura_janela/2 - cofre_fechado.width/2, altura_janela/1.4 - cofre_fechado.height/2)
cofre_aberto.set_position(largura_janela/2 - cofre_fechado.width/2, altura_janela/1.4 - cofre_fechado.height/2)

senha_digitada = ""
senha_correta = "senha"
cofre_esta_aberto = False

tempo_tecla = janela.time_elapsed()

while True:
    janela.set_background_color((0, 0, 50))
    
    if cofre_esta_aberto:
        janela.draw_text("COFRE ABERTO", largura_janela/2.7, altura_janela/10, size=20, color=(200, 200, 100), bold=True)
        janela.draw_text("Uma arma foi adicionada ao seus itens", largura_janela/5, altura_janela/6, size=20, color=(255, 255, 255), bold=True)
        janela.draw_text("Use as teclas direcionais mais espaço para disparar", largura_janela/10, altura_janela/4, size=20, color=(0, 255, 0), bold=True)
        cofre_aberto.draw()

    else:
        cofre_fechado.draw()
        janela.draw_text("Todos me pedem, mas ninguém devia dizer.", largura_janela/6, altura_janela/10, size=20, color=(0, 150, 0), bold=True)
        janela.draw_text("Mesmo assim, sou exatamente o que você vai escrever.", largura_janela/16, altura_janela/6, size=20, color=(0, 150, 0), bold=True)
        
        janela.draw_text("Digite a senha para abrir o cofre:", largura_janela/4, altura_janela/2.8, size=20, color=(255, 255, 255), bold=True)
        janela.draw_text(">", largura_janela/2.8, altura_janela/2.3, size=20, color=(0, 255, 0), bold=True)
        janela.draw_text(senha_digitada, largura_janela/2.5, altura_janela/2.3, size=20, color=(0, 255, 0), bold=True)

        for tecla in range(65, 91):  # letras A-Z
            if teclado.key_pressed(chr(tecla).lower()) and janela.time_elapsed()-tempo_tecla >= 200 :
                senha_digitada += chr(tecla).lower()
                tempo_tecla = janela.time_elapsed()
                break
        
        if teclado.key_pressed("LEFT_CONTROL") and len(senha_digitada) > 0 and janela.time_elapsed()-tempo_tecla >= 200:  # Mudar tecla para backspace 
            senha_digitada = senha_digitada[:-1]
            tempo_tecla = janela.time_elapsed()
        
        if teclado.key_pressed("enter"):
            if senha_digitada == senha_correta:
                cofre_esta_aberto = True
            else:
                janela.draw_text("INCORRETO", largura_janela/2.4, altura_janela/2.29, size=18, color=(255, 55, 50), bold=True)
                senha_digitada = ""

    if teclado.key_pressed("esc"):
        janela.close()

    janela.update()
