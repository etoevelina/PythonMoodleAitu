import atexit
import webbrowser
import flet as ft
from flet import (View, Container, Column, Text, ElevatedButton, Colors, ButtonStyle, TextStyle, TextDecoration, ListView)
from flet.core import alignment
from flet.core.alignment import top_right
from flet.core.image import Image
from flet.core.row import Row
import os
import tempfile
from flet import ProgressBar
import asyncio

from flet.core.stack import Stack

from manager.tokenManager import TokenManager

from DonutChart import DonutChart
from flet.core.textfield import TextField
from manager.course_statistic_manager import CourseStatisticManager, GradeItem



class CourseManager:
    def __init__(self, app, page, list_view, course_stat_manager, course_id_field):
        self.app = app
        self.page = page
        self.list_view = list_view
        self.course_stat_manager = course_stat_manager
        self.course_id_field = course_id_field
        self.courses_cache = None

    def login(self, token):
        token_manager = TokenManager()
        token_manager.save_token(token)
        self.app.user_token = token
        self.page.go("/main")
        self.page.update()

    def show_courses(self):
        token = self.app.user_token
        if self.courses_cache is None:
            token = self.app.user_token
            courses = self.app.hm.get_courses(token)
            self.courses_cache = courses

        courses = self.courses_cache

        if isinstance(courses, str):
            self.list_view.controls = [ft.Text(courses, color="red")]
        else:
            course_items = []
            for course in reversed(courses):
                id = course["id"]
                course_name = course["name"]
                teacher = course["teacher"]
                end_date = course.get("enddate", "N/A")
                # attendance = course["attendance"]
                # values = [attendance, 100 - attendance]
                # fontSize = 40
                # colors = ["slateblue", "gainsboro"]
                # chart = DonutChart(f"Attendance for {course_name}", values, fontSize, colors)

                # with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                #     image_path = temp_file.name
                #     chart.save(image_path)

                # grades = self.app.hm.get_grades(token, id)
                # grade_items = [GradeItem(grade["name"], grade["percentage"]) for grade in grades]

                # self.course_stat_manager.calculate_scholarship(grade_items)
                # self.course_stat_manager.calculate_retake(grade_items)

                course_card = ft.Card(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(f"{course_name}", size=18, weight="bold", color="#FFFFFF"),
                                ft.Text(f"{teacher}", size=14, color="#D9D9D9"),
                                ft.Text(f"ID: {id}", size=12, color="#A4A4A4"),

                            ], spacing=5, width=350),
                            # ft.Column(
                            #     [
                            #         ft.Text(
                            #             f"To avoid retake:\nfinal > {self.course_stat_manager.avoid:.2f}" if self.course_stat_manager.avoid > 0 else "You will not have retake",
                            #             size=12,
                            #             color="gainsboro"
                            #         ),
                            #         ft.Text(
                            #             f"To save scholarship:\nfinal> {self.course_stat_manager.scholarship:.2f}" if self.course_stat_manager.avoid > 0 else "You will safe scholarship",
                            #             size=12, color="gainsboro"),
                            #     ], spacing=5, width=200
                            # ),
                            # ft.Container(
                            #     content=ft.Column(
                            #         [
                            #
                            #             ft.Image(src=image_path, width=120, height=120),
                            #             ft.Container(
                            #                 ft.Text(
                            #                     "Total Attendance",
                            #                     size=10,
                            #                     weight="medium",
                            #                     color="#9F9F9F"
                            #                 ), padding=ft.padding.only(left=20)
                            #             ),
                            #
                            #         ]
                            #     ),
                            #
                            # )

                        ], alignment=ft.alignment.center_right),
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