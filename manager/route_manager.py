import atexit
import webbrowser
import flet as ft
from flet import (View, Container, Column, Text, ElevatedButton, Colors, ButtonStyle, TextStyle, TextDecoration, ListView)
from flet.core import alignment
from flet.core.alignment import top_right
from flet.core.image import Image
from flet.core.row import Row
import os
from flet.core.stack import Stack
from manager.CourseManager import CourseManager
from DonutChart import DonutChart
from manager.course_statistic_manager import CourseStatisticManager, GradeItem
class RouteManager:
    TOKEN_FILE = "token.txt"
    IMAGE_PATH = "/Users/evelinapenkova/Downloads/PythonMoodleAitu/assets/donut_chart.png"

    def __init__(self, app, page, user_token_field, error_message, course_id_field):
        self.app = app
        self.page = page
        self.user_token_field = user_token_field
        self.error_message = error_message
        self.course_id_field = course_id_field
        self.list_view = ListView(auto_scroll=False, expand=True, height=None)
        self.course_stat_manager = CourseStatisticManager()
        self.course_manager = CourseManager(app, page, self.list_view, self.course_stat_manager, course_id_field)
        # labels = ["Present", "Absent"]


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
                                                on_click=lambda _: self.course_manager.login(self.user_token_field.value)
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
                            # bgcolor="#000000"
                        ),
                    ],
                )
            )
        elif self.page.route == "/main":
            total_attendance = int(self.app.hm.calculateTotalAttendance(self.app.user_token))

            values = [total_attendance, 100 - total_attendance]
            height = 150
            width = 150

            self.generate_chart()

            atexit.register(self.cleanup)
            image_path1 = "/Users/evelinapenkova/Downloads/PythonMoodleAitu/assets/donut_chart.png"
            if not os.path.exists(image_path1):
                print(f"Image not found: {image_path1}")
                image_path1 = None
            self.page.views.append(
                View(
                    "/main",
                    [
                        Column(
                            [
                                Row(
                                    [
                                        Column(
                                            [
                                                Text(
                                                    f"Hello! {self.app.catch_name()}",
                                                    font_family="inter",
                                                    size=28,
                                                    weight="bold",
                                                    color="white"
                                                ),

                                                Container(
                                                    content=Text(
                                                        self.app.catch_email(),
                                                        font_family="inter",
                                                        size=20,
                                                        weight="medium",
                                                        color="#9F9F9F"
                                                    ),
                                                ),

                                            ]
                                        ),
                                        Stack(
                                            [
                                                Container(
                                                    content=Image(
                                                        src=image_path1
                                                    ) if image_path1 else Text("Image not found", color="#FFFFFF"),
                                                    # alignment=top_right,
                                                    width=170,
                                                    height=170,
                                                ),
                                                Container(
                                                    content=Text(
                                                        "Total Attendance",
                                                        font_family="inter",
                                                        size=10,
                                                        weight="medium",
                                                        color="#9F9F9F"
                                                    ),
                                                    padding=ft.padding.only(top=140, left= 40)
                                                ),
                                            ],

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
                                            padding=ft.padding.only(left=170, right=10, bottom= 70)
                                        ),
                                    ]
                                ),

                                Container(
                                    content=Text(
                                        "⊹˚₊‧────────────────────────────────────────────────────────────────────────‧₊˚⊹",
                                        font_family="inter",
                                        size=10,
                                        weight="medium",
                                        color="#9F9F9F"
                                    ),
                                ),
                                Row(
                                    [
                                        ElevatedButton("Courses", on_click=lambda _: self.course_manager.show_courses()),
                                        ElevatedButton("Grades", on_click=lambda _: self.course_manager.show_grade_input()),
                                        ElevatedButton("Deadlines", on_click=lambda _: self.course_manager.show_deadlines())
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
            self.course_manager.show_courses()
        self.page.update()

    def generate_chart(self):
        values = [
            self.app.hm.calculateTotalAttendance(self.app.user_token),
            100 - self.app.hm.calculateTotalAttendance(self.app.user_token)
        ]
        fontSize = 50
        colors = [
            "mediumblue",
            "gray"
        ]
        chart = DonutChart("Total attendance", values, fontSize, colors)
        chart.save(self.IMAGE_PATH)

    def cleanup(self):
        if os.path.exists(self.IMAGE_PATH):
            os.remove(self.IMAGE_PATH)
            print(f"Image have deleted: {self.IMAGE_PATH}")