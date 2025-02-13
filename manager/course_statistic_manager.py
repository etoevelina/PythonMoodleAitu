class GradeItem:
    def __init__(self, itemname, percentageformatted):
        self.itemname = itemname
        self.percentageformatted = percentageformatted


class CourseStatisticManager:
    def __init__(self):
        self.scholarship = 0.0
        self.avoid = 0.0
        self.finalResult = 0.0

    def find_mid_end(self, grades):
        mid = 0
        end = 0

        for item in grades:
            percentage_string = item.percentageformatted.replace(" %", "").strip()

            if percentage_string != "-":
                try:
                    percentage = float(percentage_string)
                    int_percentage = int(percentage)
                    if item.itemname == "Register Midterm":
                        print(f"mid1: {percentage_string}")
                        mid = int_percentage
                        print(f"mid: {mid}")
                    elif item.itemname == "Register Endterm":
                        end = int_percentage
                except ValueError:
                    print(f"Failed to convert {percentage_string} to a number")
            else:
                print(f"Received a '-' for {item.itemname}, setting it to 0")
                if item.itemname == "Register Midterm":
                    mid = 0
                elif item.itemname == "Register Endterm":
                    end = 0

        return mid, end

    def calculate_scholarship(self, grades):
        mid, end = self.find_mid_end(grades)

        end_component = end * 0.3
        mid_component = mid * 0.3
        total = 70 - end_component - mid_component
        final_result = (total * 100) / 40

        self.scholarship = final_result

    def calculate_retake(self, grades):
        mid, end = self.find_mid_end(grades)

        end_component = end * 0.3
        mid_component = mid * 0.3
        total = 50 - end_component - mid_component
        retake_result = (total * 100) / 40

        self.avoid = retake_result

    def calculate_higher_scholarship(self, grades):
        mid, end = self.find_mid_end(grades)

        end_component = end
        mid_component = mid
        total = 90 - end_component - mid_component
        higher_scholarship_result = (total * 100) / 40

        self.scholarship = higher_scholarship_result

    # def getting_att(self, grades):
    #     att = 0.0
    #     for item in grades:
    #         if item.itemname == "Attendance":
    #             percentage_string = item.percentageformatted.replace(" %", "").strip()
    #             try:
    #                 attendance_percentage = float(percentage_string)
    #                 att = attendance_percentage
    #                 print(f"att: {att}")
    #             except ValueError:
    #                 print(f"Failed to convert {percentage_string} to a number")
    #     return att
