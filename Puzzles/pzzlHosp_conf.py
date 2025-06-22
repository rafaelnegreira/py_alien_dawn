import random
from pplay.sprite import Sprite
class Terminal:
    def __init__(self, x, y, image_paths, solution_index, start_index):
        self.start_index = start_index
        self.image_paths = image_paths
        self.sprites = [Sprite(path) for path in image_paths]
        for sprite in self.sprites: 
            sprite.set_position(x, y)
        self.current_index = self.start_index
        self.solution_index = solution_index
    def cycle(self):
        self.current_index = (self.current_index + 1) % len(self.sprites)
    def is_correct(self): 
        return self.current_index == self.solution_index
    def draw(self):
        self.sprites[self.current_index].draw()
    def is_mouse_over(self, mouse):
        return mouse.is_over_object(self.sprites[self.current_index])

class ManageTerminal():
    def __init__(self, window, mouse):
        self.window = window
        self.mouse = mouse
        self.is_solved = False
        self.click_cooldown = 0.3
        self.click_timer = 0
        self.background = Sprite("assets/img/hosp_background1.png")
        self.victory_background = Sprite("assets/img/hosp_background0.png")
        self.font_path = "fonts/PressStart2P-Regular.ttf"
        self.buses = []
        
        self._setup_puzzle()

    def _setup_puzzle(self):
        puzzle_config = [
            {
                "position": (384, 176),
                "images": ["assets/img/hosp_bus1.png", "assets/img/hosp_bus2.png", "assets/img/hosp_bus3.png", "assets/img/hosp_bus1.png"],
                "solution": 0 
            },
            {
                "position": (256, 304),
                "images": ["assets/img/hosp_bus1.png", "assets/img/hosp_bus2.png", "assets/img/hosp_bus3.png", "assets/img/hosp_bus1.png"],
                "solution": 2 
            },
            {
                "position": (368, 304),
                "images": ["assets/img/hosp_bus1.png", "assets/img/hosp_bus2.png", "assets/img/hosp_bus3.png", "assets/img/hosp_bus1.png"],
                "solution": 3 
            },
            {
                "position": (512, 304),
                "images": ["assets/img/hospital_bus41.png", "assets/img/hospital_bus42.png", "assets/img/hospital_bus43.png", "assets/img/hospital_bus4.png"],
                "solution": 3 
            },
            {
                "position": (368, 528),
                "images": ["assets/img/hosp_bus51.png", "assets/img/hosp_bus5.png", "assets/img/hosp_bus52.png", "assets/img/hosp_bus53.png"],
                "solution": 1 
            }
        ]
        for config in puzzle_config:
            num_images = len(config["images"])
            random_start_index = random.randint(0, num_images - 1)            
            terminal = Terminal(
                x=config["position"][0],
                y=config["position"][1],
                image_paths = config["images"],
                solution_index = config["solution"],
                start_index = random_start_index
            )
            self.buses.append(terminal)
        if self.check_victory():
            if self.buses:
                self.buses[0].cycle()    
    def check_victory(self):
        return all(b.is_correct() for b in self.buses)
    def update(self, delta_time):
        if self.click_timer > 0:
            self.click_timer -= delta_time
        if self.is_solved:
            return
        if self.mouse.is_button_pressed(1) and self.click_timer <= 0:
            for bus in self.buses:
                if bus.is_mouse_over(self.mouse):
                    bus.cycle()
                    self.click_timer = self.click_cooldown
                    break
        if self.check_victory():
            self.is_solved = True
            print("PUZZLE SOLVED!")
            
    def draw(self):
        if not self.is_solved:
            self.background.draw()
            for bus in self.buses:
                bus.draw()
        #else:
        #    self.victory_background.draw()
        #    self.janela.draw_text("SOLVED", self.width / 2 - 150, self.height / 2 - 50, size=72, color=(255, 215, 0), font_name=self.font_path)