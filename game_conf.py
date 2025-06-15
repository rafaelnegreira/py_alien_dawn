import pygame
import json
from PPlay.animation import *
from PPlay.collision import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.keyboard import *
from PPlay.mouse import *
from PPlay.point import *
from PPlay.sound import *
from PPlay.sprite import *
from PPlay.window import *

class Camera:
    def __init__(self, window_width, window_height):
        self.x = 0
        self.y = 0
        self.window_width = window_width
        self.window_height = window_height

    def update(self, target):
        self.x = target.x - self.window_width // 2 + target.width // 2
        self.y = target.y - self.window_height // 2 + target.height // 2

    def apply(self, obj):
        """Aplica o offset da câmera a um objeto PPlay (Sprite/GameImage)."""
        obj.set_position(obj.x - self.x, obj.y - self.y)

    def undo(self, obj):
        """Restaura a posição original após desenhar."""
        obj.set_position(obj.x + self.x, obj.y + self.y)

        
class Maps:
    def __init__(self, mapa_cidade):
        self.background = None
        self.puzzle_triggers = []
        self.lifes = []
        self.ammo = []
        self.colisores = []
        self.portals = []
        self.infos = [] 
        self.carregar_mapa(mapa_cidade)
    def carregar_mapa(self, prox_mapa):
        self.portals.clear()
        self.puzzle_triggers.clear()
        self.colisores.clear()
        self.lifes.clear()
        self.ammo.clear()
        self.background = GameImage(f"mapa/{prox_mapa}.png")
        maps_json = f"mapa/{prox_mapa}.json"
        with open(maps_json, 'r') as f:
            game_objects = json.load(f)
        for layer in game_objects["layers"]:
            if layer["type"] == "objectgroup":
                obj_type = None
                if layer['name'] == 'portais':
                    obj_type = self.portals
                elif layer['name'] == 'puzzle':
                    obj_type = self.puzzle_triggers
                elif layer['name'] == 'vida':
                    obj_type = self.lifes
                elif layer['name'] == 'municao':
                    obj_type = self.ammo
                elif layer['name'] == 'interacao':
                    obj_type = self.infos
                elif layer['name'] == 'solidos':
                    obj_type = self.colisores

                if obj_type is not None:
                    for obj in layer['objects']:
                        bloco = Sprite("bloco_transparente.png") # Sprite invisível para colisão
                        bloco.set_position(obj['x'], obj['y'])
                        bloco.width = obj['width']
                        bloco.height = obj['height']
                        if 'properties' in obj:
                            for prop in obj['properties']:
                                setattr(bloco, prop['name'], prop['value'])
                        obj_type.append(bloco)