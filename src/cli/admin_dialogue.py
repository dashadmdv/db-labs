from prettytable import PrettyTable
from src.controller.cli_controller import CLIController


class AdminCLI:
    def __init__(self, controller):
        self.controller = controller
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

    def run(self):
        while True:
            for i, table in enumerate(self.tables):
                print(f"{i+1}. {table}")
            table_choice = int(self.input_with_check("Choose table (by index) to work with", list(str(x) for x in range(len(self.tables)+1))))
            if table_choice == 0:
                break
            name = self.tables[table_choice-1]
            while True:
                op_choice = int(self.input_with_check("Choose operation: 1 - show table, 2 - add item, 3 - show item"
                                                      " (by id), 4 - update item (by id), 5 - delete item (by id)",
                                                      ['1', '2', '3', '4', '5']))
                if op_choice == 0:
                    break
                elif op_choice == 1:
                    self.print_table(name, self.controller.get_table(name))
                elif op_choice == 2:
                    print(self.create_dialogue(name))
                elif op_choice == 3:
                    ids = self.controller.get_ids(name)
                    item_id = int(self.input_with_check("Input item id: ", [str(x) for x in ids]))
                    if item_id == 0:
                        continue
                    self.print_table(name, self.controller.get_item_by_id(item_id, name))
                elif op_choice == 4:
                    print(self.update_dialogue(name))
                elif op_choice == 5:
                    ids = self.controller.get_ids(name)
                    item_id = int(self.input_with_check("Input item id: ", [str(x) for x in ids]))
                    if item_id == 0:
                        continue
                    print(self.controller.delete_by_id(item_id, name))

    def create_dialogue(self, name):
        if name == "role":
            return self.create_role()
        elif name == 'user_acc':
            return self.create_user()
        elif name == 'user_activity':
            return self.create_user_activity()
        elif name == 'patient':
            return self.create_patient()
        elif name == 'doctor_category':
            return self.create_doc_category()
        elif name == 'doctor_specialization':
            return self.create_doc_spec()
        elif name == 'department':
            return self.create_department()
        elif name == 'doctor':
            return self.create_doctor()
        elif name == 'schedule_slot':
            return self.create_slot()
        elif name == 'service':
            return self.create_service()
        elif name == 'appointment':
            return self.create_appointment()
        elif name == 'appointment_service':
            return self.create_appointment_service()
        elif name == 'diagnosis':
            return self.create_diagnosis()
        elif name == 'prescription':
            return self.create_prescription()
        elif name == 'patient_diagnosis':
            return self.create_patient_diagnosis()

    def update_dialogue(self, name):
        if name == "role":
            return self.create_role(update=True)
        elif name == 'user_acc':
            return self.create_user(update=True)
        elif name == 'user_activity':
            return self.create_user_activity(update=True)
        elif name == 'patient':
            return self.create_patient(update=True)
        elif name == 'doctor_category':
            return self.create_doc_category(update=True)
        elif name == 'doctor_specialization':
            return self.create_doc_spec(update=True)
        elif name == 'department':
            return self.create_department(update=True)
        elif name == 'doctor':
            return self.create_doctor(update=True)
        elif name == 'schedule_slot':
            return self.create_slot(update=True)
        elif name == 'service':
            return self.create_service(update=True)
        elif name == 'appointment':
            return self.create_appointment(update=True)
        elif name == 'appointment_service':
            return self.create_appointment_service(update=True)
        elif name == 'diagnosis':
            return self.create_diagnosis(update=True)
        elif name == 'prescription':
            return self.create_prescription(update=True)
        elif name == 'patient_diagnosis':
            return self.create_patient_diagnosis(update=True)

    def create_role(self, update=False):
        if update:
            it_ids = self.controller.get_ids('role')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        name = input("Input role name: ")
        if update:
            return self.controller.update_role(it_id, name)
        return self.controller.create_role(name)

    def create_user(self, update=False):
        if update:
            it_ids = self.controller.get_ids('user_acc')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        users = self.controller.get_usernames()
        while True:
            username = input("Input username: ")
            if username in users:
                print("This username exists!")
                continue
            break
        password = input("Input password: ")
        role_id = int(self.input_with_check("Role 1 - admin, 2 - patient or 3 - doctor? ", ['1', '2', '3'], True))
        if update:
            return self.controller.update_user(it_id, username, password, role_id)
        return self.controller.create_user(username, password, role_id)

    def create_patient(self, update=False):
        if update:
            it_ids = self.controller.get_ids('patient')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        ids = self.controller.get_ids('user_acc')
        user_id = int(self.input_with_check("Input user id: ", [str(x) for x in ids]))
        if user_id == 0:
            return
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
        if update:
            return self.controller.update_patient(it_id, user_id, first_name, last_name, date_of_birth, gender, phone_number,
                                                  email)
        return self.controller.create_patient(user_id, first_name, last_name, date_of_birth, gender, phone_number, email)

    def create_doctor(self, update=False):
        if update:
            it_ids = self.controller.get_ids('doctor')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        ids = self.controller.get_ids('user_acc')
        user_id = int(self.input_with_check("Input user id: ", [str(x) for x in ids]))
        if user_id == 0:
            return
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
        spec_ids = self.controller.get_ids('doctor_specialization')
        spec_id = int(self.input_with_check("Input specialization id: ", [str(x) for x in spec_ids]))
        dep_ids = self.controller.get_ids('department')
        dep_id = int(self.input_with_check("Input department id: ", [str(x) for x in dep_ids]))
        if update:
            return self.controller.update_doctor(it_id, user_id, first_name, last_name, gender, spec_id, dep_id)
        return self.controller.create_doctor(user_id, first_name, last_name, gender, spec_id, dep_id)

    def create_user_activity(self, update=False):
        if update:
            it_ids = self.controller.get_ids('user_activity')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        ids = self.controller.get_ids('user_acc')
        user_id = int(self.input_with_check("Input user id: ", [str(x) for x in ids]))
        if user_id == 0:
            return
        activity_type = input("Activity type: ")
        if update:
            return self.controller.update_user_activity(it_id, user_id, activity_type)
        return self.controller.create_user_activity(user_id, activity_type)

    def create_doc_category(self, update=False):
        if update:
            it_ids = self.controller.get_ids('doctor_category')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        name = input("Input doctor category name: ")
        if update:
            return self.controller.update_doc_category(it_id, name)
        return self.controller.create_doc_category(name)

    def create_doc_spec(self, update=False):
        if update:
            it_ids = self.controller.get_ids('doctor_specialization')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        name = input("Input doctor specialization name: ")
        ids = self.controller.get_ids('doctor_category')
        category_id = int(self.input_with_check("Input category id: ", [str(x) for x in ids]))
        if category_id == 0:
            return
        if update:
            return self.controller.update_doc_spec(it_id, name, category_id)
        return self.controller.create_doc_spec(name, category_id)

    def create_department(self, update=False):
        if update:
            it_ids = self.controller.get_ids('department')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        name = input("Input department name: ")
        if update:
            return self.controller.update_department(it_id, name)
        return self.controller.create_department(name)

    def create_slot(self, update=False):
        if update:
            it_ids = self.controller.get_ids('schedule_slot')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        while True:
            date_of_slot = input("Date of slot (yyyy-mm-dd): ")
            if date_of_slot[4] != '-' and date_of_slot[7] != '-':
                print("Incorrect format!")
                continue
            break
        while True:
            time_of_slot = input("Time of slot (hh:mm:ss): ")
            if time_of_slot[2] != ':' and time_of_slot[5] != ':':
                print("Incorrect format!")
                continue
            break
        ids = self.controller.get_ids('doctor')
        doctor_id = int(self.input_with_check("Input doctor id: ", [str(x) for x in ids]))
        if doctor_id == 0:
            return
        if update:
            return self.controller.update_slot(it_id, date_of_slot, time_of_slot, doctor_id)
        return self.controller.create_slot(date_of_slot, time_of_slot, doctor_id)

    def create_service(self, update=False):
        if update:
            it_ids = self.controller.get_ids('service')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        name = input("Input service name: ")
        price = int(input("Input price: "))
        ids = self.controller.get_ids('doctor')
        doctor_id = int(self.input_with_check("Input doctor id: ", [str(x) for x in ids]))
        if doctor_id == 0:
            return
        if update:
            return self.controller.update_service(it_id, name, price, doctor_id)
        return self.controller.create_service(name, price, doctor_id)

    def create_appointment(self, update=False):
        if update:
            it_ids = self.controller.get_ids('appointment')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        slot_ids = self.controller.get_ids('schedule_slot')
        slot_id = int(self.input_with_check("Input slot id: ", [str(x) for x in slot_ids]))
        if slot_id == 0:
            return
        patient_ids = self.controller.get_ids('patient')
        patient_id = int(self.input_with_check("Input patient id: ", [str(x) for x in patient_ids]))
        if slot_id == 0:
            return
        if update:
            return self.controller.update_appointment(it_id, slot_id, patient_id)
        return self.controller.create_appointment(slot_id, patient_id)

    def create_appointment_service(self, update=False):
        if update:
            it_ids = self.controller.get_ids('appointment_service')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        app_ids = self.controller.get_ids('appointment')
        app_id = int(self.input_with_check("Input appointment id: ", [str(x) for x in app_ids]))
        if app_id == 0:
            return
        service_ids = self.controller.get_ids('service')
        service_id = int(self.input_with_check("Input service id: ", [str(x) for x in service_ids]))
        if service_id == 0:
            return
        if update:
            return self.controller.update_appointment_service(it_id, app_id, service_id)
        return self.controller.create_appointment_service(app_id, service_id)

    def create_diagnosis(self, update=False):
        if update:
            it_ids = self.controller.get_ids('diagnosis')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        name = input("Input diagnosis name: ")
        code = input("Input diagnosis code: ")
        if update:
            return self.controller.update_diagnosis(it_id, name, code)
        return self.controller.create_diagnosis(name, code)

    def create_prescription(self, update=False):
        if update:
            it_ids = self.controller.get_ids('prescription')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        note = input("Input note: ")
        app_ids = self.controller.get_ids('appointment')
        app_id = int(self.input_with_check("Input appointment id: ", [str(x) for x in app_ids]))
        if app_id == 0:
            return
        if update:
            return self.controller.update_prescription(it_id, note, app_id)
        return self.controller.create_prescription(note, app_id)

    def create_patient_diagnosis(self, update=False):
        if update:
            it_ids = self.controller.get_ids('patient_diagnosis')
            it_id = int(self.input_with_check("Input item id: ", [str(x) for x in it_ids]))
            if it_id == 0:
                return
        patient_ids = self.controller.get_ids('patient')
        patient_id = int(self.input_with_check("Input patient id: ", [str(x) for x in patient_ids]))
        if patient_id == 0:
            return
        diagnosis_ids = self.controller.get_ids('diagnosis')
        diagnosis_id = int(self.input_with_check("Input diagnosis id: ", [str(x) for x in diagnosis_ids]))
        if diagnosis_id == 0:
            return
        if update:
            return self.controller.update_patient_diagnosis(it_id, patient_id, diagnosis_id)
        return self.controller.create_patient_diagnosis(patient_id, diagnosis_id)
