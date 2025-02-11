# route_manager.py
import webbrowser
import flet as ft
from flet import (View, Container, Column, Text, ElevatedButton, Colors, ButtonStyle, TextStyle, TextDecoration, ListView)
from flet.core import alignment
from flet.core.alignment import top_right
from flet.core.image import Image
from flet.core.row import Row
from flet.core.stack import Stack
import os
from manager.tokenManager import TokenManager

from manager.http_manager import HttpManager

from flet.core.textfield import TextField


class RouteManager:
    TOKEN_FILE = "token.txt"

    def __init__(self, app, page, user_token_field, error_message, course_id_field):
        self.app = app
        self.page = page
        self.user_token_field = user_token_field
        self.error_message = error_message
        self.course_id_field = course_id_field
        self.list_view = ListView(auto_scroll=False, expand=True, height=None)

    def update_list_view(self, items):
        formatted_items = [str(item).replace("\n", " ") for item in items]
        self.list_view.controls = [ft.Text(item, color="#FFFFFF") for item in formatted_items]
        self.page.update()

    def route_change(self, e):
        self.page.views.clear()
        self.page.bgcolor = "#000000"

        if self.page.route == "/":
            image_path = "/Users/evelinapenkova/Downloads/PythonMoodleAitu/assets/zagagulina.png"
            if not os.path.exists(image_path):
                print(f"Image not found: {image_path}")
                image_path = None

            self.page.views.append(
                View(
                    "/",
                    [
                        Container(
                            content=Image(
                                src=image_path
                            ) if image_path else Text("Image not found", color="#FFFFFF"),
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
                                         weight="bold",
                                         color="#FFFFFF"),
                                    ft.Row(
                                        [
                                            self.user_token_field,
                                            ElevatedButton(
                                                "Login",
                                                width=146,
                                                height=40,
                                                bgcolor="#FFFFFF",
                                                color="#000000",
                                                on_click=lambda _: self.login(self.user_token_field.value)
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
                                    self.error_message,
                                ],
                                alignment=alignment.bottom_left,
                            ),
                            alignment=alignment.bottom_left,
                            bgcolor="#000000"
                        ),
                    ],
                )
            )
        elif self.page.route == "/main":
            self.page.views.append(
                View(
                    "/main",
                    [
                        Column(
                            [

                                Row(
                                    [
                                        Text(
                                            f"Hello! {self.app.catch_name()}",
                                            font_family="inter",
                                            size=28,
                                            weight="bold",
                                            color="white"
                                        ),

                                        Container(
                                            content=ft.TextButton(
                                                "Logout",
                                                on_click=self.app.logout,
                                                style=ButtonStyle(
                                                    color="white",
                                                    overlay_color="transparent",
                                                    text_style=TextStyle(
                                                        decoration=TextDecoration.UNDERLINE)
                                                )
                                            ),
                                            alignment=ft.alignment.top_right,
                                            padding=ft.padding.only(left=10, right=10)
                                        ),
                                    ],
                                    # expand=True,


                                ),
                                Container(
                                     Text(self.app.catch_email(),
                                          font_family="inter",
                                          size=20,
                                          weight="medium",
                                          color="#9F9F9F"
                                          ),

                                    # padding=ft.padding.only(left=10, right=10)
                                ),
                                Row(
                                    [
                                        ElevatedButton("Courses", on_click=lambda _: self.show_courses()),

                                        ElevatedButton("Grades", on_click=lambda _: self.show_grade_input()),
                                        ElevatedButton("Deadlines", on_click=lambda _: self.show_deadlines())
                                    ],
                                    alignment=alignment.center,
                                ),
                                Container(
                                    content=self.list_view,
                                    bgcolor="#000000",
                                    padding=ft.padding.all(10),
                                    expand=True
                                )
                            ],
                            expand=True
                        )
                    ],
                )
            )

            self.show_courses()

        self.page.update()

    def login(self, token):
        token_manager = TokenManager()
        token_manager.save_token(token)
        self.app.user_token = token
        self.page.go("/main")
        self.page.update()

    def show_courses(self):
        token = self.app.user_token
        courses = self.app.hm.get_courses(token)

        if isinstance(courses, str):
            self.list_view.controls = [ft.Text(courses, color="red")]
        else:
            course_items = []
            for course in reversed(courses):
                id = course["id"]
                course_name = course["name"]
                teacher = course["teacher"]
                end_date = course.get("enddate", "N/A")

                course_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"{course_name}", size=18, weight="bold", color="#FFFFFF"),
                            ft.Text(f"{teacher}", size=14, color="#D9D9D9"),
                            ft.Text(f"ID: {id}", size=12, color="#A4A4A4"),
                        ], spacing=5),
                        padding=15,
                        bgcolor="#222222",
                        border_radius=12,
                        shadow=ft.BoxShadow(blur_radius=8, color="#000000")
                    )
                )

                course_items.append(course_card)

            self.list_view.controls = course_items

        self.page.update()

    def show_deadlines(self):

        TextField
        deadlines = self.app.hm.get_deadlines(self.app.user_token)

        if isinstance(deadlines, str):
            self.list_view.controls = [ft.Text(deadlines, color="red")]
        else:
            deadlines_items = []
            for deadline in deadlines:
                deadline_name = deadline["name"]
                formattedtime = deadline["formattedtime"]
                coursename = deadline["coursename"]

                deadline_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"{deadline_name}", size=18, weight="bold", color="#FFFFFF"),
                            ft.Text(f"{formattedtime}", size=14, color="#D9D9D9"),
                            ft.Text(f"Course: {coursename}", size=12, color="#A4A4A4"),
                        ], spacing=5),
                        padding=15,
                        bgcolor="#222222",
                        border_radius=12,
                        shadow=ft.BoxShadow(blur_radius=8, color="#000000")
                    )
                )

                deadlines_items.append(deadline_card)

            self.list_view.controls = deadlines_items

        self.page.update()

    def showGrades(self, course_id):

        try:
            course_id = int(course_id)
        except ValueError:
            self.list_view.controls = [ft.Text("Invalid course ID", color="red")]
            self.page.update()
            return

        grades = self.app.hm.get_grades(self.app.user_token, course_id)

        if isinstance(grades, str):
            self.list_view.controls = [ft.Text(grades, color="red")]
        else:
            grades_items = []
            for grade in grades:
                grade_name = grade["name"]
                grade_percentage = grade["percentage"]
                grade_course_name = grade["coursename"]

                grade_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"{grade_name}", size=18, weight="bold", color="#FFFFFF"),
                            ft.Text(f"{grade_percentage}", size=14, color="#D9D9D9"),
                            ft.Text(f"Course: {grade_course_name}", size=12, color="#A4A4A4"),
                        ], spacing=5),
                        padding=15,
                        bgcolor="#222222",
                        border_radius=12,
                        shadow=ft.BoxShadow(blur_radius=8, color="#000000")
                    )
                )

                grades_items.append(grade_card)

            self.list_view.controls = grades_items

        self.page.update()

    def show_grade_input(self):
        self.list_view.controls = [
            ft.Row(
                [
                    self.course_id_field,
                    ElevatedButton(
                        "Show Grades",
                        width=146,
                        height=40,
                        bgcolor="#FFFFFF",
                        color="#000000",
                        on_click=lambda _: self.showGrades(self.course_id_field.value)
                    ),
                ],
                alignment=alignment.center
            )
        ]
        self.page.update()