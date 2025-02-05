import requests
import json

class HttpManager:
    def __init__(self):
        pass

    def get_user_info(self, token):
        base_url = "https://aitu-web-app-2240c1581e3e.herokuapp.com/users/get_user/"
        url = base_url + token

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                username = data["username"]
                fullname = data["fullname"]
                userid = data["userid"]

                print("User:\n")
                print(f"Username: {username}")
                print(f"Fullname: {fullname}")
                print(f"User ID: {userid}")
                return True, [username,fullname]
                # return response.text
            else:
                return False, f"Invalid token: {response.status_code}"
                # return f"Invalid token: {response.status_code}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

    def get_courses(self, token):
        base_url = "https://aitu-web-app-2240c1581e3e.herokuapp.com/courses/get_courses/"
        url = base_url + token

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print("Courses:\n")
                for course in data:
                    id = course["id"]
                    fullname = course["fullname"]
                    parts = fullname.split("|")
                    course_name = parts[0].strip()
                    teacher = parts[1].strip()
                    print(f"ID: {id}")
                    print(f"Course Name: {course_name}")
                    print(f"Teacher: {teacher}")
                    print("➽─────────────────────────────────────────❥")

                return response.text
            else:
                return f"GET request failed. Response Code: {response.status_code}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

    def get_deadlines(self, token):
        base_url = "https://aitu-web-app-2240c1581e3e.herokuapp.com/deadlines/get_deadlines/"
        url = base_url + token

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print("Deadlines:\n")
                for deadline in data:
                    name = deadline["name"]
                    formattedtime = deadline["formattedtime"]
                    coursename = deadline["coursename"]
                    print(f"Name: {name}")
                    print(f"Deadline Time: {formattedtime}")
                    print(f"Course Name: {coursename}")
                    print("➽─────────────────────────────────────────❥")

                return response.text
            else:
                return f"GET request failed. Response Code: {response.status_code}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

    def get_grades(self, token, course_id):
        base_url = "https://aitu-web-app-2240c1581e3e.herokuapp.com/grades/get_grades/"
        url = base_url + token

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for course in data:
                    if course["courseid"] == course_id:
                        fullname = course["coursename"]
                        print(f"Course: {fullname}")
                        print(".・。.・゜✭・.・✫・゜・。..・。.・゜✭・.・✫・゜・。.")
                        grade_items = course["gradeitems"]
                        for grade_item in grade_items:
                            if grade_item["percentageformatted"] not in ["-", "0.00 %"]:
                                print(f"Item Name: {grade_item['itemname']}")
                                print(f"Percentage: {grade_item['percentageformatted']}")

                        return json.dumps(course)
                return "Course not found."
            else:
                return f"GET request failed. Response Code: {response.status_code}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"