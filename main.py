import webbrowser
import os

import flet as ft
from flet import (AppBar, ElevatedButton, Page, Text, TextField, View, Colors, SnackBar, Image, Column, Row, Container, Stack, ButtonStyle, TextStyle, TextDecoration)
from flet.core import alignment
from flet.core.alignment import top_right
import http_manager


class MoodleApp:
    def __init__(self):
        self.hm = http_manager.HttpManager()
        self.user_token = self.load_token()

    def save_token(self, token):
        with open("token.txt", "w") as file:
            file.write(token)

    def load_token(self):
        if os.path.exists("token.txt"):
            with open("token.txt", "r") as file:
                return file.read().strip()
        return None

    def main(self, page: ft.Page):
        page.title = "Moodle"
        user_token_field = TextField(
            label="Enter your token",
            width=350,
            bgcolor="F2F2F2",
            border_radius=11,
        )
        error_message = Text(value="", color=Colors.RED)
        page.window.max_width = 800
        page.window.max_height = 700
        page.window.resizable = False
        page.window.bgcolor = "#000000"

        def validate_token(token):
            print(f"Validating token: {token}")
            logic, user_info = self.hm.get_user_info(token)
            print(f"Token validation result: {logic}")
            return logic

        def catch_name(token):
            logic, user_info = self.hm.get_user_info(token)
            return user_info[1] if logic else "Unknown"

        def catch_email(token):
            logic, user_info = self.hm.get_user_info(token)
            return user_info[0] if logic else "Unknown"

        def start(token):
            print("start function called")
            if not validate_token(token):
                print("Token is not valid")
                error_message.value = "Invalid token. Please try again."
                page.update()
            else:
                self.user_token = token
                self.save_token(token)
                print("Token is  valid")
                print("Token is valid, navigating to /main")
                page.go("/main")

        def route_change(e):
            page.views.clear()
            if page.route == "/":
                page.views.append(
                    View(
                        "/",
                        [
                            Container(
                                content=Image(
                                    src="/Users/evelinapenkova/Downloads/PythonMoodleAitu/assets/zagagulina.png"
                                ),
                                alignment=top_right,
                                width=810,
                                height=380,
                            ),
                            Container(
                                content=Column(
                                    [
                                        Text("Welcome to the Moodle app!",
                                             font_family="inter",
                                             size=28,
                                             weight="bold"),
                                        ft.Row(
                                            [
                                                user_token_field,
                                                ElevatedButton(
                                                    "Login",
                                                    width=146,
                                                    height=40,
                                                    bgcolor="#FFFFFF",
                                                    color="#000000",
                                                    on_click=lambda _: start(user_token_field.value)
                                                ),
                                            ],
                                            alignment=alignment.center,
                                        ),
                                        ElevatedButton(
                                            "How to find it?",
                                            bgcolor=Colors.TRANSPARENT,
                                            color="#FFFFFF",
                                            style=ButtonStyle(
                                                text_style=TextStyle(
                                                    font_family="inter",
                                                    color="#FFFFFF",
                                                    size=15,
                                                    weight="medium",
                                                    decoration=TextDecoration.UNDERLINE
                                                )
                                            ),
                                            on_click=lambda _: webbrowser.open(
                                                "https://www.notion.so/How-to-find-your-token-189e80e5e5c280e792a2e4a6cbd4b4e1?pvs=4"
                                            ),
                                        ),
                                        error_message,
                                    ],
                                    alignment=alignment.bottom_left,
                                ),
                                alignment=alignment.bottom_left,
                            ),
                        ],
                    )
                )
            elif page.route == "/main":
                page.views.append(
                    View(
                        "/main",
                        [
                            Stack(
                                [
                                    Container(
                                        content=Image(
                                            src="/Users/evelinapenkova/Downloads/PythonMoodleAitu/assets/ell.png",
                                            fit=ft.ImageFit.COVER,
                                        ),
                                        expand=True,
                                        alignment=top_right,
                                    ),
                                    Container(
                                        content=Column(
                                            [
                                                Row(
                                                    [
                                                        Text(
                                                            f"Hello! {catch_name(self.user_token)}",
                                                            font_family="inter",
                                                            size=28,
                                                            weight="bold",
                                                            expand=True,
                                                            color="white"
                                                        ),
                                                        Container(
                                                            content=ft.TextButton(
                                                                "Logout",
                                                                on_click=lambda _: page.go("/"),
                                                                style=ButtonStyle(
                                                                    color="white",
                                                                    overlay_color="transparent",
                                                                    text_style=TextStyle(
                                                                        decoration=TextDecoration.UNDERLINE)
                                                                )
                                                            ),
                                                            padding=ft.padding.only(left=10, right=10)
                                                        ),
                                                    ],
                                                    expand=True
                                                ),
                                                Text(
                                                    catch_email(self.user_token),
                                                    font_family="inter",
                                                    size=20,
                                                    weight="medium",
                                                    color="#9F9F9F"
                                                ),
                                            ],
                                            alignment=alignment.center,
                                        ),
                                        alignment=alignment.center,
                                    ),
                                    Container(
                                        content=Row(
                                            [
                                                ElevatedButton("Courses", on_click=lambda _: page.go("/courses")),
                                                ElevatedButton("Grades", on_click=lambda _: page.go("/grades")),
                                                ElevatedButton("Show graded by course id",
                                                               on_click=lambda _: page.go("/show_graded")),
                                            ],
                                            alignment=alignment.space_between,
                                        ),
                                    ),
                                ],
                            )
                        ],
                    )
                )
            elif page.route == "/courses":
                page.views.append(
                    View(
                        "/courses",
                        [
                            Text("Courses View", size=20)
                        ]
                    )
                )
            elif page.route == "/deadlines":
                page.views.append(
                    View(
                        "/deadlines",
                        [
                            Text("Deadlines View", size=20)
                        ]
                    )
                )
            elif page.route == "/show_graded":
                page.views.append(
                    View(
                        "/show_graded",
                        [
                            Text("Show Graded View", size=20)
                        ]
                    )
                )

            page.update()

        if self.user_token:
            start(self.user_token)

        page.on_route_change = route_change
        page.go("/")


if __name__ == "__main__":
    app = MoodleApp()
    ft.app(target=app.main)