# myApp.py

import http_manager

class MyApp:
    def __init__(self):
        self.http_manager = http_manager.HttpManager()

    def main_menu(self, token):
        while True:
            print("Welcome to the user menu!")
            print("1. View user info")
            print("2. View all courses")
            print("3. View all deadlines")
            print("4. View marks by course id")
            print("5. Logout")
            option = int(input("Enter option (1-5): "))
            if option == 1:
                self.http_manager.get_user_info(token)
            elif option == 2:
                self.http_manager.get_courses(token)
            elif option == 3:
                self.http_manager.get_deadlines(token)
            elif option == 4:
                course_id = int(input("Please copy and paste course id: "))
                self.http_manager.get_grades(token, course_id)
            elif option == 5:
                break
            else:
                print("Invalid option. Please try again.")

    def start(self):
        token = input("Please enter token: ")
        self.main_menu(token)

if __name__ == "__main__":
    MyApp()