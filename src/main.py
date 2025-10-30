import arcade
from .settings import WIDTH, HEIGHT, TITLE
from .scenes.menu import MenuView
def main() -> None:
    window = arcade.Window(WIDTH, HEIGHT, TITLE, update_rate=1/120)
    window.show_view(MenuView())
    arcade.run()
if __name__ == "__main__":
    main()   