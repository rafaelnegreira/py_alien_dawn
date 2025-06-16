# GameObjects.py (CORRIGIDO)

from PPlay.gameimage import*
from PPlay.sprite import*

class GameObject:
    # Esta classe pode ser removida se não tiver um uso específico.
    # A herança direta de Sprite é suficiente por enquanto.
    pass

class Object(Sprite): # Não precisa herdar de GameObject aqui
    def __init__(self, game_object_data):
        super().__init__("assets/img/bloco_transparente.png")
        self.x = game_object_data.get('x', 0)
        self.y = game_object_data.get('y', 0)
        self.width = game_object_data.get('width', 0)
        self.height = game_object_data.get('height', 0)
        self.id = game_object_data.get('id', 0) # Adicionado para referência
        self.name = game_object_data.get('name', '') # Adicionado para referência
        self.set_position(self.x, self.y)

        if 'properties' in game_object_data:
            for prop in game_object_data['properties']:
                setattr(self, prop['name'], prop['value'])    

class Colisores(Object):
    pass

class Interaveis(Object):
    # CORREÇÃO: Renomeado para __init__
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
        self.locked = getattr(self, 'locked', False) # Checa se a propriedade 'locked' existe

    def unlock(self):
        self.locked = False
        print(f"Portal {self.name} destrancado!")

class Puzzle(Interaveis):
    def __init__(self, game_object_data):
        super().__init__(game_object_data)
        # CORREÇÃO: usa getattr para buscar uma propriedade customizada 'portal_target_id'
        self.portal_target_id = getattr(self, 'portal_target_id', None)
        self.concluido = False

    def interagir(self):
        # Apenas sinaliza que o puzzle deve começar. A lógica de destravar
        # o portal fica no Game_Manager
        if not self.concluido:
            return True # Sinaliza para o Game_Manager que o puzzle pode começar
        return False
        
    def concluir(self):
        self.concluido = True
        print(f"Puzzle {self.name} concluído!")