from PPlay.gameimage import *
from PPlay.sprite import *
import os

# Obtém o diretório do script para construir caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class GameObject:
    pass

class Object(Sprite):
    def __init__(self, game_object_data):
        # Constrói o caminho absoluto para a imagem padrão
        image_path = os.path.join(BASE_DIR, "assets", "img", "bloco_transparente.png")
        super().__init__(image_path)
        self.x = game_object_data.get('x', 0)
        self.y = game_object_data.get('y', 0)
        self.width = game_object_data.get('width', 0)
        self.height = game_object_data.get('height', 0)
        self.id = game_object_data.get('id', 0)
        self.name = game_object_data.get('name', '')
        self.set_position(self.x, self.y)

        if 'properties' in game_object_data:
            for prop in game_object_data['properties']:
                setattr(self, prop['name'], prop['value'])    

class Inimigo(Object):
    """Esta classe representa um inimigo carregado do mapa."""
    pass

class Colisores(Object):
    pass

class Interaveis(Object):
    def __init__(self, game_object_data):
        super().__init__(game_object_data)

class Item(Interaveis):
    def __init__(self, game_object_data):
        super().__init__(game_object_data)
        self.coletado = False
        
    def interagir(self):
        if not self.coletado:
            self.coletado = True
            print(f"Item {self.name} coletado!")

class Portais(Interaveis):
    def __init__(self, game_object_data):
        super().__init__(game_object_data)
        self.locked = getattr(self, 'locked', False)

    def unlock(self):
        self.locked = False
        print(f"Portal {self.name} destrancado!")

class Puzzle(Interaveis):
    def __init__(self, game_object_data):
        super().__init__(game_object_data)
        self.portal_target_id = getattr(self, 'portal_target_id', None)
        self.concluido = False

    def interagir(self):
        if not self.concluido:
            return True
        return False
        
    def concluir(self):
        self.concluido = True
        print(f"Puzzle {self.name} concluído!")