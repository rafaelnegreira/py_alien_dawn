from pplay.sprite import Sprite
class Terminal:
    def __init__(self, x, y, image_paths, solution_index, start_index = 0):
        self.start_index = start_index
        self.image_paths = image_paths
        self.sprites = [Sprite(path) for path in image_paths]
        for sprite in self.sprites: 
            sprite.set_position(x, y)
        self.current_index = start_index
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
    def __init__(self, janela):
        self.janela = janela
        self.mouse = janela.get_mouse()
        self.teclado = janela.get_keyboard()
        self.is_solved = False
        self.click_cooldown = 0.3
        self.click_timer = 0
        self.key_press_timer = 0
        self.key_press_cooldown = 0.3
        self.background_playing = Sprite("assets/img/hosp_background0.png")
        self.background_text = Sprite("assets/img/hosp_background1.png")
        self.font_path = "fonts/PressStart2P-Regular.ttf"
        self.buses = []
        self.internal_state = "BRIEFING"
        self._setup_puzzle()
    def _setup_puzzle(self):
        puzzle_config = [
            {
                "position": (144, 240),
                "images": ["assets/img/hosp_bus1.png", "assets/img/hosp_bus2.png", "assets/img/hosp_bus1.png", "assets/img/hosp_bus2.png"],
                "solution": 1, 
                "start_index": 0
            },
            {
                "position": (240, 160),
                "images": ["assets/img/hosp_bus1.png", "assets/img/hosp_bus2.png", "assets/img/hosp_bus1.png", "assets/img/hosp_bus2.png"],
                "solution": 0,
                "start_index": 1
            },
            {
                "position": (240, 320),
                "images": ["assets/img/hosp_bus1.png", "assets/img/hosp_bus2.png", "assets/img/hosp_bus1.png", "assets/img/hosp_bus2.png"],
                "solution": 2,
                "start_index": 3 
            },
            {
                "position": (336, 240),
                "images": ["assets/img/hosp_bus1.png", "assets/img/hosp_bus2.png", "assets/img/hosp_bus1.png", "assets/img/hosp_bus2.png"],
                "solution": 3,
                "start_index": 2 
            },
            {
                "position": (64, 96),
                "images": ["assets/img/hosp_bus31.png", "assets/img/hosp_bus32.png", "assets/img/hosp_bus33.png", "assets/img/hosp_bus3.png"],
                "solution": 1,
                "start_index": 0 
            },
            {
                "position": (416, 96),
                "images": ["assets/img/hosp_bus31.png", "assets/img/hosp_bus32.png", "assets/img/hosp_bus33.png", "assets/img/hosp_bus3.png"],
                "solution": 2,
                "start_index": 1 
            },
            {
                "position": (416, 384),
                "images": ["assets/img/hosp_bus31.png", "assets/img/hosp_bus32.png", "assets/img/hosp_bus33.png", "assets/img/hosp_bus3.png"],
                "solution": 3,
                "start_index": 2 
            },
            {
                "position": (64, 384),
                "images": ["assets/img/hosp_bus31.png", "assets/img/hosp_bus32.png", "assets/img/hosp_bus33.png", "assets/img/hosp_bus3.png"],
                "solution": 0,
                "start_index": 1 
            },
            {
                "position": (64, 240),
                "images": ["assets/img/hosp_bus41.png", "assets/img/hosp_bus4.png", "assets/img/hosp_bus42.png", "assets/img/hosp_bus43.png"],
                "solution": 0,
                "start_index": 1 
            },
            {
                "position": (240, 96),
                "images": ["assets/img/hosp_bus41.png", "assets/img/hosp_bus4.png", "assets/img/hosp_bus42.png", "assets/img/hosp_bus43.png"],
                "solution": 2,
                "start_index": 3 
            },
            {
                "position": (240, 384),
                "images": ["assets/img/hosp_bus41.png", "assets/img/hosp_bus4.png", "assets/img/hosp_bus42.png", "assets/img/hosp_bus43.png"],
                "solution": 1,
                "start_index": 2 
            },
            {
                "position": (416, 240),
                "images": ["assets/img/hosp_bus41.png", "assets/img/hosp_bus4.png", "assets/img/hosp_bus42.png", "assets/img/hosp_bus43.png"],
                "solution": 3,
                "start_index": 0 
            }
        ]
        for config in puzzle_config:   
            terminal = Terminal(
                x=config["position"][0],
                y=config["position"][1],
                image_paths = config["images"],
                solution_index = config["solution"],
                start_index = config["start_index"]
            )
            self.buses.append(terminal)     
    def check_victory(self):
        return all(b.is_correct() for b in self.buses)
    def update(self):
        if self.click_timer > 0:
            self.click_timer -= self.janela.delta_time()
        if self.internal_state == "BRIEFING":
            if self.teclado.key_pressed("E") and self.key_press_timer <= 0:
                self.internal_state = "PLAYING"
                self.key_press_timer = self.key_press_cooldown # Reseta o cooldown da tecla
        
        elif self.internal_state == "PLAYING":
            if self.click_timer > 0:
                self.click_timer -= self.janela.delta_time()
            if self.mouse.is_button_pressed(1) and self.click_timer <= 0:
                for bus in self.buses:
                    if bus.is_mouse_over(self.mouse):
                        bus.cycle()
                        self.click_timer = self.click_cooldown
                        break
            if self.check_victory():
                self.internal_state = "SOLVED"
                self.key_press_timer = self.key_press_cooldown
        elif self.internal_state == "SOLVED":
            if self.teclado.key_pressed("E") and self.key_press_timer <= 0:
                return "COMPLETED"
        return "RUNNING"
    def draw(self):
        if self.internal_state == "BRIEFING":
            self.background_text.draw()
            self.janela.draw_text(
                "REDIRECIONE A ENERGIA", 
                x=(self.janela.width / 2) - 270, # Centraliza
                y=200, 
                size=30, 
                color=(170, 255, 255),
                font_name="assets/PressStart2P-Regular.ttf"
            )
            self.janela.draw_text(
                "Pressione [E] para iniciar", 
                x=(self.janela.width / 2) - 200, # Centraliza
                y=500, 
                size=20, 
                color=(255, 255, 150),
                font_name="assets/PressStart2P-Regular.ttf"
            )
        elif self.internal_state == "PLAYING":
            self.background_playing.draw()
            for bus in self.buses:
                bus.draw()
        elif self.internal_state == "SOLVED":
            self.background_text.draw()
            self.janela.draw_text(
                "ENERGIA REESTABELECIDA", 
                x = (self.janela.width) / 4, 
                y = (self.janela.heigth) / 3, 
                size=32, 
                color=(150, 255, 150),
                font_name=self.font_path
            )
            self.janela.draw_text(
                "Pressione [E] para sair", 
                x=(self.janela.width) / 2, 
                y= (self.janela.heigth) / 2, 
                size=20, 
                color=(180, 255, 180),
                font_name=self.font_path
            )