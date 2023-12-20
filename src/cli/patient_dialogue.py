from prettytable import PrettyTable
from src.controller.cli_controller import CLIController


class PatientCLI:
    def __init__(self, controller, pat_id):
        self.controller = controller
        self.patient_id = pat_id
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
            op_choice = int(self.input_with_check("Choose operation: 1 - see my appointments, 2 - get appointment, "
                                                  "3 - my diagnoses, 4 - my prescriptions",
                                                  ['1', '2', '3', '4']))
            if op_choice == 0:
                break
            elif op_choice == 1:
                app_ids = self.controller.get_patient_appointments(self.patient_id)
                print(app_ids)
                info = []
                for id in app_ids:
                    item = self.controller.get_doctor_app_info(id)
                    print(item)
                    info.append(item)
                name = ['appointment_id', 'service', 'patient', 'doctor', 'date', 'time', 'price']
                print(info)
                self.print_table(name, info)
            elif op_choice == 2:
                name = ['id', 'date', 'time', 'doctor']
                info = self.controller.get_app_slots()
                self.print_table(name, info)
                slots_ids = self.controller.get_app_slots_ids()
                slots_id = int(self.input_with_check("Select slot (by id): ", [str(x) for x in slots_ids]))
                if slots_id == 0:
                    return
                info = self.controller.get_doctor_services(self.controller.get_doctor_from_slot(slots_id))
                print(info)
                self.print_table('service', info)
                service_ids = self.controller.get_ids('service')
                service_id = int(self.input_with_check("Select service (by id): ", [str(x) for x in service_ids]))
                if service_id == 0:
                    return
                print(self.controller.create_appointment(slots_id, self.patient_id))
                app_id = self.controller.get_app_from_slot(slots_id)
                print(self.controller.create_appointment_service(app_id, service_id))
            elif op_choice == 3:
                name = ['Date of diagnosis', 'Diagnosis name', 'Diagnosis code']
                info = self.controller.get_patient_diagnoses(self.patient_id)
                self.print_table(name, info)
            elif op_choice == 4:
                name = ['Prescription', 'Date', 'Doctor']
                info = self.controller.get_patient_prescription(self.patient_id)
                self.print_table(name, info)
