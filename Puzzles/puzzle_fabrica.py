from pplay.window import Window
from pplay.sprite import Sprite
from pplay.mouse import Mouse
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
ASSETS_PATH = "assets/img/"

class PuzzleButton(Sprite):
    def __init__(self, x, y, button_id, off_image_path, on_image_path):
        # Define a imagem inicial e a posição
        super().__init__(off_image_path)
        self.set_position(x, y)
        
        self.id = button_id
        # Carrega a imagem do estado "pressionado"
        self.sprite_on = Sprite(on_image_path)
        self.sprite_on.set_position(x, y)
        
        # Controla o feedback visual do próprio botão
        self.is_lit = False
        self.lit_timer = 0
        self.lit_duration = 0.3

    def press(self):
        # Ativa o estado "pressionado" por um curto período
        self.is_lit = True
        self.lit_timer = self.lit_duration

    def update(self, delta_time):
        # Atualiza o timer para apagar a luz do botão
        if self.is_lit:
            self.lit_timer -= delta_time
            if self.lit_timer <= 0:
                self.is_lit = False

    def draw(self):
        # Desenha o sprite correto (aceso ou apagado)
        if self.is_lit:
            self.sprite_on.draw()
        else:
            self.draw()

    def is_mouse_over(self, mouse):
        return mouse.is_over(self)

# --- Classe Principal que Gerencia o Puzzle ---
class SequencePuzzle:
    def __init__(self, window, mouse):        
        self.window = window
        self.mouse = mouse
        self.is_solved = False        
        # Carrega o fundo principal do puzzle
        self.background = Sprite(ASSETS_PATH + "puzzle_fabricabg.png")
        
        # Carrega os sprites de flash e os redimensiona para a tela inteira
        self.flash_red = Sprite(ASSETS_PATH + "bat0_off.png")
        self.flash_green = Sprite(ASSETS_PATH + "bat_on.png")
        self.flash_red.set_size(226, 105)
        self.flash_green.set_size(226, 105)
        
        # Variáveis para controlar qual flash mostrar e por quanto tempo
        self.active_flash = None
        self.feedback_timer = 0
        self.feedback_duration = 0.4 # Duração do flash em segundos

        # Definição da Sequência e dos Botões
        self.SOLUTION_SEQUENCE = ["bateria_D", "bateria_A", "bateria_B", "bateria_C"]
        self.player_sequence = []
        self.buttons = []
        self._setup_buttons()

    def _setup_buttons(self):
        # Configuração de cada um dos 4 botões
        button_config = [
            {"id": "bateria_A", "pos": (368, 240), "off_img": "batt1_off.png", "on_img": "batt1_on.png"},
            {"id": "bateria_B", "pos": (512, 240), "off_img": "batt2_off.png", "on_img": "batt2_on.png"},
            {"id": "bateria_C", "pos": (368, 352), "off_img": "batt3_off.png", "on_img": "batt3_on.png"},
            {"id": "bateria_D", "pos": (512, 352), "off_img": "batt4_off.png", "on_img": "batt4_on.png"},
        ]
        
        for config in button_config:
            button = PuzzleButton(
                config["pos"][0], config["pos"][1], config["id"],
                ASSETS_PATH + config["off_img"], ASSETS_PATH + config["on_img"]
            )
            self.buttons.append(button)

    def process_click(self, button_id):
        # Lógica central que verifica a sequência
        self.player_sequence.append(button_id)
        current_solution_part = self.SOLUTION_SEQUENCE[:len(self.player_sequence)]

        if self.player_sequence != current_solution_part:
            # Errou: ativa o flash vermelho e reinicia
            print("ERRO!")
            self.active_flash = self.flash_red
            self.feedback_timer = self.feedback_duration
            self.player_sequence = []
            return
        
        if self.player_sequence == self.SOLUTION_SEQUENCE:
            # Acertou: ativa o flash verde e resolve
            print("RESOLVIDO!")
            self.active_flash = self.flash_green
            self.feedback_timer = self.feedback_duration
            self.is_solved = True

    def update(self):
        # Se o puzzle foi resolvido, não há mais lógica a ser feita
        if self.is_solved: return

        # Atualiza timers (luzes dos botões e flash da tela)
        for button in self.buttons:
            button.update(self.window.delta_time())
        if self.feedback_timer > 0:
            self.feedback_timer -= self.window.delta_time()

        # Processa cliques apenas se não houver um flash na tela
        if self.mouse.is_button_pressed(1) and self.feedback_timer <= 0:
            for button in self.buttons:
                if button.is_mouse_over(self.mouse):
                    button.press()
                    self.process_click(button.id)
                    self.window.delay(200) # Cooldown simples para o clique
                    break

    def draw(self):
        # Desenha a cena base
        self.background.draw()
        for button in self.buttons:
            button.draw()
        
        # Se um flash estiver ativo, desenha-o por cima de tudo
        if self.feedback_timer > 0 and self.active_flash:
            self.active_flash.draw()
            
        # Se resolvido, pode desenhar uma mensagem de texto final
        if self.is_solved:
            return False