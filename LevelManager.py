import json
from GameObjects import*
class Objects_json:
    def __init__(self, prox_mapa):
        self.obj_interaveis = []
        self.read_json(prox_mapa)
    def read_json(self, prox_mapa):
        self.obj_interaveis.clear()
        arq_json = f"mapa/{prox_mapa}.json"
        with open(arq_json, 'r') as f:
            game_objects = json.load(f)
        for layer in game_objects["layers"]:
            if layer["type"] == "objectgroup":
                layer_name = layer['name'].lower()
                for obj_data in layer['objects']:
                    new_obj = None
                if layer_name == 'portais': 
                    new_obj = Portais(self)
                elif layer_name == 'puzzle':
                    new_obj = Puzzle(self)
                elif layer_name in ['municao', 'interacao','vida']:
                    new_obj = Item(self)
                elif layer_name == 'solidos':
                    new_obj = Colisores(self)
                if new_obj is not None:
                        self.obj_interaveis.append(new_obj)