import arcade 
from ..settings import WIDTH, HEIGHT, TITLE
from ..entities.player import Player

class GameScene(arcade.Window):
    def _init_(self):
        super()._inite_(WIDTH, HEIGHT, TITLE, update_rate=1/120)
        arcade.set.background_color(arcade.color_from_hex_string("#121216"))
        self.player = Player()
        self.keys_held: set[int] = set()
        self.fps_label = arcade.Text ("FPS: 0", 8, HEIGHT - 24, (200,200,200), 12)

    def on_draw(self):
        self.clear()
        self.player.draw()
        self.fps_label.draw()

    def on_update(self, dt: float):
        self.player.handle_keys(self.keys_held)
        self.player.update(dt)
        self.fps_label.text = f"FPS: {int(arcade.get_fps())}"

    def on_key_press(self, symbol: int, modifiers: int):
        self.keys_held.add(symbol)

    def on_key_release(self, symbol: int, modifiers: int):
        self.keys_held.discard(symbol)                            