import flet as ft
from flet import TextField, Text, Colors
from manager.http_manager import HttpManager
from manager.tokenManager import TokenManager
from manager.route_manager import RouteManager

class MyApp():
    def __init__(self):
        super().__init__()
        self.hm = HttpManager()
        self.token_manager = TokenManager()
        self.user_token = self.token_manager.load_token()
        self.error_message = Text(value="", color=Colors.RED)
        self.is_started = False
        self.user_info = None
        self.course_id_field = ft.TextField(label="Course ID")

    def start(self, token):
        if not self.is_started:
            self.token_manager.save_token(token)
            self.is_started = True
            print(token)
            result = self.hm.get_user_info(token)
            if isinstance(result, tuple) and len(result) == 2:
                self.user_info = result[1]
                print(self.user_info)
                self.catch_name()
            self.page.go("/main")


    def catch_name(self):
        result = self.hm.get_user_info(self.user_token)
        data = result[1]
        if isinstance(result, tuple) and len(result) > 0:
            return data[1]
        elif isinstance(result, str):
            return result
        else:
            return "Unknown User"

    def catch_email(self):
        result = self.hm.get_user_info(self.user_token)
        data = result[1]
        if isinstance(result, tuple) and len(result) > 0:
            return data[0]
        elif isinstance(result, str):
            return result
        else:
            return "Unknown Email"

    def logout(self, e):
        print("Logging out")
        self.user_token = None
        self.token_manager.save_token("")
        self.page.go("/")
        self.page.update()

    def main(self, page: ft.Page):
        self.page = page
        page.title = "Moodle"

        user_token_field = TextField(
            label="Enter your token",
            width=350,
            bgcolor="F2F2F2",
            border_radius=11,
        )
        page.window.max_width = 1100
        page.window.max_height = 900
        page.window.resizable = False

        self.route_manager = RouteManager(self, page, user_token_field, self.error_message, self.course_id_field)

        if self.user_token:
            page.on_route_change = self.route_manager.route_change
            page.go("/main")
            self.start(self.user_token)
        else:
            page.on_route_change = self.route_manager.route_change
            page.add(user_token_field, self.error_message)
            page.go("/")
        page.update()

if __name__ == "__main__":
    app = MyApp()
    ft.app(target=app.main)