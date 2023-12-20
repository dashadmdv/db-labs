from prettytable import PrettyTable
from src.controller.cli_controller import CLIController


class DoctorCLI:
    def __init__(self, controller, doc_id):
        self.controller = controller
        self.doctor_id = doc_id
        self.current_appointment = None
        self.current_patient = None
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
        if type(name) == list:
            table.field_names = name
        else:
            table.field_names = ["id"] + self.fields[self.tables.index(name)]
        table.add_rows(info)
        print(table)

    def run(self):
        while True:
            op_choice = int(self.input_with_check("Choose operation: 1 - see my appointments, 2 - select appointment",
                                                  ['1', '2']))
            if op_choice==0:
                break
            elif op_choice==1:
                app_ids = self.controller.get_doctor_appointments(self.doctor_id)
                info = []
                for id in app_ids:
                    info.append(self.controller.get_doctor_app_info(id))
                name = ['appointment_id', 'service', 'patient', 'doctor', 'date', 'time']
                self.print_table(name, info)
            elif op_choice == 2:
                app_ids = self.controller.get_doctor_appointments(self.doctor_id)
                app_id = int(self.input_with_check("Select appointment (by id): ", [str(x) for x in app_ids]))
                self.current_appointment = app_id
                self.current_patient = self.controller.get_patient_by_app(app_id)
                self.appointment_dialogue()

    def appointment_dialogue(self):
        while True:
            op_choice = int(self.input_with_check("Choose operation: 1 - see appointment details, 2 - add diagnosis"
                                                  ", 3 - add prescription, 4 - end appointment",
                                                  ['1', '2', '3', '4']))
            if op_choice == 0:
                break
            elif op_choice == 1:
                info = self.controller.get_doctor_app_info(self.current_appointment)
                name = ['appointment_id', 'service', 'patient', 'doctor', 'date', 'time', 'price']
                self.print_table(name, [info])
            elif op_choice == 2:
                patient_id = self.current_patient
                self.print_table('diagnosis', self.controller.get_table('diagnosis'))
                diagnosis_ids = self.controller.get_ids('diagnosis')
                diagnosis_id = int(self.input_with_check("Input diagnosis id: ", [str(x) for x in diagnosis_ids]))
                if diagnosis_id == 0:
                    return
                print(self.controller.create_patient_diagnosis(patient_id, diagnosis_id))
            elif op_choice == 3:
                note = input("Input note: ")
                return self.controller.create_prescription(note, self.current_appointment)
            elif op_choice == 4:
                self.current_appointment = None
                self.current_patient = None