import requests
import json
import os
from dotenv import load_dotenv

class HttpManager:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

    def get_user_info(self, token):
        base_url = os.getenv("USER_URL")
        url = f"{base_url}{token}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                username = data["username"]
                fullname = data["fullname"]
                userid = data["userid"]
                return True, [username, fullname]
            else:
                return False, f"Invalid token: {response.status_code}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

    def get_courses(self, token):
        base_url = os.getenv("COURSE_URL")
        url = f"{base_url}{token}"
        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            if not isinstance(data, list):
                return f"Unexpected response format: {data}"

            courses = []
            for course in data:
                try:
                    id = course["id"]
                    fullname = course["fullname"]
                    parts = fullname.split("|")
                    course_name = parts[0].strip()
                    teacher = parts[1].strip() if len(parts) > 1 else "Unknown"

                    courses.append({
                        "id": id,
                        "name": course_name,
                        "teacher": teacher,
                        "enddate": course.get("enddate", "Unknown")
                    })
                except KeyError as e:
                    print(f"Skipping course due to missing key: {e}")

            return courses

        except requests.exceptions.RequestException as e:
            return f"HTTP request failed: {str(e)}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

    def get_deadlines(self, token):
        base_url = os.getenv("DEADLINES_URL")
        url = f"{base_url}{token}"
        try:
            deadlines = []
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for deadline in data:
                    name = deadline["name"]
                    formattedtime = deadline["formattedtime"]
                    coursename = deadline["coursename"]

                    deadlines.append({
                        "name": name,
                        "formattedtime": formattedtime,
                        "coursename": coursename
                    })

                return deadlines
            else:
                return f"GET request failed. Response Code: {response.status_code}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

    def get_grades(self, token, course_id):
        base_url = os.getenv("GRADES_URL")
        url = f"{base_url}{token}"

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            if not isinstance(data, list):
                return f"Unexpected response format: {data}"

            grades = []
            for course in data:
                if course["courseid"] == course_id:
                    fullname = course["coursename"]
                    grade_items = course.get("gradeitems", [])
                    for grade_item in grade_items:
                        if grade_item["percentageformatted"] not in ["-", "0.00 %"]:
                            name = grade_item["itemname"]
                            percentage = grade_item["percentageformatted"]

                            grades.append({
                                "name": name,
                                "percentage": percentage,
                                "coursename": fullname
                            })

                    return grades

            return "Course not found."

        except requests.exceptions.RequestException as e:
            return f"HTTP request failed: {str(e)}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"