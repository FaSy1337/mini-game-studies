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
import random
import arcade
from ..settings import WIDTH, HEIGHT, BG_COLOR
from ..entities.player import Player

class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.player: Player | None = None
        self.keys_held: set[int] = set()

        self.coins: arcade.SpriteList | None = None
        self.score: int = 0

        self.ui_text_fps: arcade.Text | None = None
        self.ui_text_score: arcade.Text | None = None
        self.snd_pick: arcade.Sound | None = None

    def on_show_view(self) -> None:
        arcade.set_background_color(BG_COLOR)
        self.player = Player()

        # --- монетки ---
        self.coins = arcade.SpriteList(use_spatial_hash=True)
        margin = 40
        for _ in range(20):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.6)
            coin.center_x = random.randint(margin, WIDTH - margin)
            coin.center_y = random.randint(margin, HEIGHT - margin)
            self.coins.append(coin)

        # --- HUD ---
        self.ui_text_fps   = arcade.Text("FPS: 0", 8, HEIGHT - 22, (200, 200, 200), 12)
        self.ui_text_score = arcade.Text("SCORE: 0", 8, HEIGHT - 44, (230, 230, 255), 14)
        self.snd_pick      = arcade.load_sound(":resources:sounds/coin1.wav")

    def on_draw(self) -> None:
        self.clear()
        if self.coins:  self.coins.draw()
        if self.player: self.player.draw()
        if self.ui_text_fps:   self.ui_text_fps.draw()
        if self.ui_text_score: self.ui_text_score.draw()

    def on_update(self, dt: float) -> None:
        if self.player:
            self.player.handle_keys(self.keys_held)
            self.player.update(dt)

        # столкновения игрока с монетами
        if self.player and self.coins:
            hit_list = arcade.check_for_collision_with_list(self.player, self.coins)
            for coin in hit_list:
                coin.remove_from_sprite_lists()
                self.score += 1
                if self.snd_pick: arcade.play_sound(self.snd_pick)

        # обновление HUD
        if self.ui_text_fps:
            self.ui_text_fps.text = f"FPS: {int(arcade.get_fps())}"
        if self.ui_text_score:
            self.ui_text_score.text = f"SCORE: {self.score}"

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            from .pause import PauseView
            self.window.show_view(PauseView(self))
            return
        self.keys_held.add(symbol)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self.keys_held.discard(symbol)                             