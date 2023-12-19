from prettytable import PrettyTable
from src.controller.cli_controller import CLIController


class CLI:
    def __init__(self):
        self.controller = None
        self.current_user_id = None
        self.current_username = None
        self.current_user_role = None
        self.exit_prompt = ", 0 - exit"
        self.back_prompt = ", 0 - go back"
        self.hint_prompt = " (enter a number): "
        self.tables = ['role', 'user_acc', 'user_activity', 'patient', 'doctor_category', 'doctor_specialization',
                       'department', 'doctor', 'schedule_slot', 'service', 'appointment', 'appointment_service',
                       'diagnosis', 'prescription', 'patient_diagnosis']
        self.fields = [["Role name"], ["Username", "Password", "Role id"], ["User id", "Activity", "Date", "Time"],
                       ["User id", "First name", "Last name", "Date of birth", "Gender", "Phone", "Email"],
                       ["Category name"], ["Specialization name", "Category id"], ["Department name"],
                       ["Date", "Time", "Doctor id"], ["Service name", "Price", "Doctor id"], ["Slot id", "Patient_id"],
                       ["Appointment id", "Service id"], ["Diagnosis name", "Diagnosis code"],
                       ["Note", "Appointment id"], ["Patient id", "Diagnosis id"]]

    def input_with_check(self, prompt: str, values_list: list, back_mode=True):
        prompt += (self.back_prompt if back_mode else self.exit_prompt) + self.hint_prompt
        values_list.extend(['0'])
        while True:
            value = input(prompt)
            if value not in values_list:
                print("No such option! Try again!")
                continue
            return value

    def print_table(self, name, info):
        table = PrettyTable()
        table.field_names = ["id"] + self.fields[self.tables.index(name)]
        table.add_rows(info)
        print(table)

    def registration(self):
        users = self.controller.get_usernames()
        while True:
            username = input("Input username: ")
            if username in users:
                print("This username exists!")
                continue
            break
        password = input("Input password: ")
        role_id = int(self.input_with_check("Are you 2 - patient or 3 - doctor? ", ['2', '3'], True))
        self.controller.create_user(username, password, role_id)
        user_id = self.controller.get_user_by_username(username)[0]
        if role_id == 2:
            self.create_patient(user_id)
        elif role_id == 3:
            self.create_doctor(user_id)

    def create_patient(self, user_id):
        first_name = input("First name: ")
        last_name = input("Last name: ")
        while True:
            date_of_birth = input("Date of birth (yyyy-mm-dd): ")
            if date_of_birth[4] != '-' and date_of_birth[7] != '-':
                print("Incorrect format!")
                continue
            break
        while True:
            gender = int(input("Male - 1 or female - 2, other - 3: "))
            if gender == 1:
                gender = 'Male'
            elif gender == 2:
                gender = 'Female'
            elif gender == 3:
                gender = input("Input gender: ")
            else:
                print("No such option!")
                continue
            break
        phone_number = input("Phone number (+375xxxxxxxxxx): ")
        email = input("Email: ")
        user_info = self.controller.get_item_by_id(user_id, 'user_acc')[0]
        self.controller.create_patient(user_id, first_name, last_name, date_of_birth, gender, phone_number, email)
        self.update_current_user(user_info[0], user_info[1], user_info[2])

    def create_doctor(self, user_id):
        first_name = input("First name: ")
        last_name = input("Last name: ")
        while True:
            gender = int(input("Male - 1 or female - 2, other - 3: "))
            if gender == 1:
                gender = 'Male'
            elif gender == 2:
                gender = 'Female'
            elif gender == 3:
                gender = input("Input gender: ")
            else:
                print("No such option!")
                continue
            break
        user_info = self.controller.get_item_by_id(user_id, 'user_acc')[0]
        self.controller.create_doctor_min(user_id, first_name, last_name, gender)
        self.update_current_user(user_info[0], user_info[1], user_info[2])

    def login(self):
        users = self.controller.get_usernames()
        username = input("Input username: ")
        if username not in users:
            print("This user doesn't exists!")
            return
        user_info = self.controller.get_item_by_id(self.controller.get_user_by_username(username)[0], 'user_acc')[0]
        password = input("Input password: ")
        if password != user_info[2]:
            print("Incorrect password!")
            return
        self.update_current_user(user_info[0], user_info[1], user_info[2])

    def logout(self):
        print("Bye!")
        self.update_current_user()

    def update_current_user(self, user_id=None, username=None, role=None):
        self.current_user_id = user_id
        self.current_username = username
        self.current_user_role = role
        if user_id:
            print(f"Hello, {username}!")

    def run(self):
        print('Hello! Setting up the database...')
        # here the database is created
        self.controller = CLIController()

        while True:
            choice = int(self.input_with_check(f"Registration - 1, {'login' if not self.current_user_id else 'logout'} - 2",
                                           ['1', '2'], False))
            if choice == 0:
                print('Goodbye!')
                break
            elif choice == 1:
                self.registration()
            elif choice == 2:
                if not self.current_user_id:
                    self.login()
                else:
                    self.logout()
