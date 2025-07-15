from PIL import Image

# Abrir imagem original
imagem = Image.open("C:/Users/vieir/OneDrive/Área de Trabalho/Labjogos/py_alien_dawn/assets/img/imagem_grande.jpg")  # substitua pelo nome da sua imagem

# Tamanho da imagem
largura, altura = imagem.size

# Tamanho de cada peça (assumindo corte 3x3)
largura_p = largura // 3
altura_p = altura // 3

# Cortar e salvar cada pedaço
contador = 1
for i in range(3):
    for j in range(3):
        esquerda = j * largura_p
        topo = i * altura_p
        direita = esquerda + largura_p
        inferior = topo + altura_p

        caixa = (esquerda, topo, direita, inferior)
        recorte = imagem.crop(caixa)
        recorte.save(f"p{contador}.png")
        contador += 1
