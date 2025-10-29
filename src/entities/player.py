import arcade
from ..settings import WIDTH, HEIGHT, PLAYER_SREED

class Player(arcade.SpriteSolidColor):
    def _init_(self):
        super()._init_(40, 40, arcade.color_from_hex_string("#DCDCFf"))
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2
        self.vx = 0.0
        self.vy = 0.0
        
    def update(self, dt: float):
        self.center_x += self.vx * dt
        self.center_y += self.vy * dt
        self.center_x = max(20, min(WIDTH - 20, self.center_x))
        self.center_y = max(20, min(HEIGHT - 20, self.center_y))

    def handle_keys(self, key_held: set):
        self.vx = ((arcade.key.D in keys_held) - (arcade.key.A in keys_held)) * PLAYER_SREED
        self.vy = ((arcade.key.W in keys_held) - (arcade.key.S in keys_held)) * PLAYER_SREED