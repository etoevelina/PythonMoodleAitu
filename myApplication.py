import os
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, BOLD, RIGHT
from travertino.constants import BLACK, WHITE


class MyApplication(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.size = (800, 600)
        self.main_window.min_width = self.main_window.max_width = 800
        self.main_window.min_height = self.main_window.max_height = 600

        try:
            image_path = os.path.join(os.path.dirname(__file__), "authView.png")
            image = toga.Image(image_path)
        except Exception as e:
            return

        image_view = toga.ImageView(image, style=Pack(padding=(0, 0, 0, 100),width=700, height=400))

        top_box = toga.Box(style=Pack(direction=ROW, alignment=RIGHT, flex=1))
        top_box.add(image_view)

        name_label = toga.Label(
            "Enter your token",
            style=Pack(padding=(0, 5), font_weight=BOLD, font_size=20, color=WHITE, width=400)
        )
        self.token_input = toga.TextInput(style=Pack(padding=5, width=370, background_color="#D3D3D3"))

        name_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        name_box.add(name_label)
        name_box.add(self.token_input)

        button = toga.Button(
            "Continue",
            on_press=self.say_hello,
            style=Pack(padding=10, font_size=15, width=146)
        )

        background_box = toga.Box(style=Pack(direction=COLUMN, background_color=BLACK, flex=1))
        background_box.add(top_box)
        background_box.add(name_box)
        background_box.add(button)

        self.main_window.content = background_box
        self.main_window.show()

    def say_hello(self, widget):
        print(self.token_input.value)

def main():
    return MyApplication('My Application', 'org.beeware.myapp')

if __name__ == '__main__':
    main().main_loop()
