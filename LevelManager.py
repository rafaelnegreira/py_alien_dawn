import json
from GameObjects import *
import os

# Obtém o diretório do script para construir caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_map_objects(map_name):
    """Função que lê um arquivo JSON do mapa e retorna uma lista de objetos do jogo."""
    
    all_objects = []
    # Constrói o caminho absoluto para o arquivo JSON do mapa
    json_path = os.path.join(BASE_DIR, "mapa", f"{map_name}.json")
    
    with open(json_path, 'r') as f:
        map_data = json.load(f)

    for layer in map_data["layers"]:
        if layer["type"] == "objectgroup":
            layer_name = layer['name'].lower()
            
            for obj_data in layer['objects']:
                new_obj = None
                
                if layer_name == 'portais': 
                    new_obj = Portais(obj_data)
                elif layer_name == 'puzzle':
                    new_obj = Puzzle(obj_data)
                elif layer_name in ['municao', 'interacao', 'vida']:
                    new_obj = Item(obj_data)
                elif layer_name == 'solidos':
                    new_obj = Colisores(obj_data)
                elif layer_name == 'inimigos':
                    new_obj = Inimigo(obj_data)
                
                if new_obj is not None:
                    all_objects.append(new_obj)
                    
    return all_objects