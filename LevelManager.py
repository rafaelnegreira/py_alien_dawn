# LevelManager.py (CORRIGIDO)

import json
from GameObjects import *

def load_map_objects(map_name):
    """Função que lê um arquivo JSON do mapa e retorna uma lista de objetos do jogo."""
    
    all_objects = []
    json_path = f"mapa/{map_name}.json"
    
    with open(json_path, 'r') as f:
        map_data = json.load(f)

    for layer in map_data["layers"]:
        if layer["type"] == "objectgroup":
            layer_name = layer['name'].lower()
            
            for obj_data in layer['objects']:
                new_obj = None
                
                # O bloco de decisão agora está DENTRO do loop de objetos
                if layer_name == 'portais': 
                    # Passa o dicionário 'obj_data', e não 'self'
                    new_obj = Portais(obj_data)
                elif layer_name == 'puzzle':
                    new_obj = Puzzle(obj_data)
                elif layer_name in ['municao', 'interacao', 'vida']:
                    new_obj = Item(obj_data)
                elif layer_name == 'solidos':
                    new_obj = Colisores(obj_data)
                
                elif layer_name == 'inimigos':
                    new_obj = Inimigo(obj_data) # Cria um objeto Inimigo com os dados do mapa
                
                if new_obj is not None:
                    all_objects.append(new_obj)
                    
    return all_objects