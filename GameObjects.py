from PPlay.gameimage import*
from PPlay.sprite import*
class GameObject:
    def __init__(self, janela, teclado, mouse):
        self.janela = janela
        self.teclado = teclado
        self.mouse = mouse
    def update(self):
        pass

    def draw(self):
        pass     
class Object(Sprite, GameObject):
    def __init__(self, game_object):
        super().__init__("assets/img/bloco_transparente.png")
        self.x = game_object.get('x', 0)
        self.y = game_object.get('y', 0)
        self.width = game_object.get('width', 0)
        self.height = game_object.get('height', 0)
        if 'properties' in game_object:
            for prop in game_object['properties']:
                setattr(self, prop['name'], prop['value'])    
class Colisores(Object):
    pass
class Interaveis(Object):
    def ler_id(self, game_object):
        super().__init__(game_object)
        self.id = game_object.get('id', '')       
class Item(Interaveis):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.coletado = False
    def interagir(self):
        if not self.coletado:
            self.coletado = True
class Portais(Interaveis):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.locked = False
    def interagir(self):
        if not self.locked:
            self.locked = True
class Puzzle(Interaveis):
    def __init__(self, game_object):
        super().__init__(game_object)
        self.area = game_object('id_area', 0)
        self.concluido = False
    def interagir(self):
        if not self.concluido:
            self.concluido = True
            Portais.interagir(self.area)
        return self.concluido