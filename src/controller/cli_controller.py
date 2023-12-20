import sys

from src.storage.database import Database


class CLIController:
    def __init__(self):
        try:
            db = Database()
        except Exception as e:
            print(f'Unable to connect!\n{e}')
            sys.exit()
        else:
            self.db = db

    def close_database(self):
        self.db.close()

    def get_table(self, name):
        return self.db.show_table(name)

    def get_item_by_id(self, item_id, name):
        return [self.db.select_by_id(item_id, name)]

    def get_usernames(self):
        users = self.db.get_usernames()
        result = []
        for user in users:
            result.extend(user)
        return result

    def get_user_by_username(self, username):
        return self.db.get_user_by_username(username)

    def get_ids(self, name):
        ids = self.db.get_ids(name)
        result = []
        for id_ in ids:
            result.extend(id_)
        return result

    def get_doctor_by_user_id(self, user_id):
        return self.db.get_doctor_by_user_id(user_id)[0]

    def get_patient_by_user_id(self, user_id):
        return self.db.get_patient_by_user_id(user_id)[0]

    def get_patient_by_app(self, app_id):
        return self.db.get_patient_by_app(app_id)[0]

    def get_doctor_appointments(self, doc_id):
        ids = self.db.get_doctor_appointments(doc_id)
        result = []
        for id_ in ids:
            result.extend(id_)
        return result

    def get_patient_appointments(self, pat_id):
        ids = self.db.get_patient_appointments(pat_id)
        result = []
        for id_ in ids:
            result.extend(id_)
        return result

    def get_patient_diagnoses(self, pat_id):
        return self.db.get_patient_diagnoses(pat_id)

    def get_patient_prescription(self, pat_id):
        return self.db.get_patient_prescription(pat_id)

    def get_doctor_app_info(self, app_id):
        return self.db.get_doctor_app_info(app_id)

    def get_app_slots(self):
        return self.db.get_app_slots()

    def get_app_slots_ids(self):
        ids = self.db.get_app_slots_ids()
        result = []
        for id_ in ids:
            result.extend(id_)
        return result

    def get_doctor_services(self, doc_id):
        return self.db.get_doctor_services(doc_id)

    def get_app_from_slot(self, slot_id):
        return self.db.get_app_from_slot(slot_id)[0]

    def get_doctor_from_slot(self, slot_id):
        return self.db.get_doctor_from_slot(slot_id)[0]

    def create_role(self, name):
        return self.db.create_role(name)

    def create_user(self, username, password, role_id):
        return self.db.create_user(username, password, role_id)

    def create_user_activity(self, user_id, activity_type):
        return self.db.create_user_activity(user_id, activity_type)

    def create_patient(self, user_id, first_name, last_name, date_of_birth, gender, phone_number, email=''):
        return self.db.create_patient(user_id, first_name, last_name, date_of_birth, gender, phone_number, email)

    def create_doc_category(self, name):
        return self.db.create_doc_category(name)

    def create_doc_spec(self, name, category_id):
        return self.db.create_doc_spec(name, category_id)

    def create_department(self, name):
        return self.db.create_department(name)

    def create_doctor(self, user_id, first_name, last_name, gender, specialization_id, department_id):
        return self.db.create_doctor(user_id, first_name, last_name, gender, specialization_id, department_id)

    def create_doctor_min(self, user_id, first_name, last_name, gender):
        return self.db.create_doctor_min(user_id, first_name, last_name, gender)

    def create_slot(self, date_of_slot, time_of_slot, doctor_id):
        return self.db.create_slot(date_of_slot, time_of_slot, doctor_id)

    def create_service(self, service_name, price, doctor_id):
        return self.db.create_service(service_name, price, doctor_id)

    def create_appointment(self, slot_id, patient_id):
        return self.db.create_appointment(slot_id, patient_id)

    def create_appointment_service(self, appointment_id, service_id):
        return self.db.create_appointment_service(appointment_id, service_id)

    def create_diagnosis(self, diagnosis_name, diagnosis_code):
        return self.db.create_diagnosis(diagnosis_name, diagnosis_code)

    def create_prescription(self, note, appointment_id):
        return self.db.create_prescription(note, appointment_id)

    def create_patient_diagnosis(self, patient_id, diagnosis_id):
        return self.db.create_patient_diagnosis(patient_id, diagnosis_id)

    # UPDATE

    def update_role(self, id, name):
        entity = self.get_item_by_id(id, 'role')[0]
        if entity[1] != name:
            return self.db.update_role(id, name)
        return "Nothing to update!"

    def update_user(self, id, username, password, role_id):
        entity = self.get_item_by_id(id, 'user_acc')[0]
        username = username or entity[1]
        password = password or entity[2]
        role_id = role_id or entity[3]
        return self.db.update_user(id, username, password, role_id)

    def update_user_activity(self, id, user_id, activity_type, date_of_activity='', time_of_activity=''):
        entity = self.get_item_by_id(id, 'user_activity')[0]
        user_id = user_id or entity[1]
        activity_type = activity_type or entity[2]
        date_of_activity = date_of_activity or entity[3]
        time_of_activity = time_of_activity or entity[4]
        return self.db.update_user_activity(id, user_id, activity_type, date_of_activity, time_of_activity)

    def update_patient(self, id, user_id, first_name, last_name, date_of_birth, gender, phone_number, email=''):
        entity = self.get_item_by_id(id, 'patient')[0]
        user_id = user_id or entity[1]
        first_name = first_name or entity[2]
        last_name = last_name or entity[3]
        date_of_birth = date_of_birth or entity[4]
        gender = gender or entity[5]
        phone_number = phone_number or entity[6]
        email = email or entity[7]
        return self.db.update_patient(id, user_id, first_name, last_name, date_of_birth, gender, phone_number, email)

    def update_doc_category(self, id, name):
        entity = self.get_item_by_id(id, 'doctor_category')[0]
        if entity[1] != name:
            return self.db.update_doc_category(id, name)
        return "Nothing to update!"

    def update_doc_spec(self, id, name, category_id):
        entity = self.get_item_by_id(id, 'doctor_specialization')[0]
        name = name or entity[1]
        category_id = category_id or entity[2]
        return self.db.update_doc_spec(id, name, category_id)

    def update_department(self, id, name):
        entity = self.get_item_by_id(id, 'department')[0]
        if entity[1] != name:
            return self.db.update_department(id, name)
        return "Nothing to update!"

    def update_doctor(self, id, user_id, first_name, last_name, gender, specialization_id, department_id):
        entity = self.get_item_by_id(id, 'doctor')[0]
        user_id = user_id or entity[1]
        first_name = first_name or entity[2]
        last_name = last_name or entity[3]
        gender = gender or entity[4]
        specialization_id = specialization_id or entity[5]
        department_id = department_id or entity[6]
        return self.db.update_doctor(id, user_id, first_name, last_name, gender, specialization_id, department_id)

    def update_slot(self, id, date_of_slot, time_of_slot, doctor_id):
        entity = self.get_item_by_id(id, 'schedule_slot')[0]
        date_of_slot = date_of_slot or entity[1]
        time_of_slot = time_of_slot or entity[2]
        doctor_id = doctor_id or entity[3]
        return self.db.update_slot(id, date_of_slot, time_of_slot, doctor_id)

    def update_service(self, id, service_name, price, doctor_id):
        entity = self.get_item_by_id(id, 'service')[0]
        service_name = service_name or entity[1]
        price = price or entity[2]
        doctor_id = doctor_id or entity[3]
        return self.db.update_service(id, service_name, price, doctor_id)

    def update_appointment(self, id, slot_id, patient_id):
        entity = self.get_item_by_id(id, 'appointment')[0]
        slot_id = slot_id or entity[1]
        patient_id = patient_id or entity[2]
        return self.db.update_appointment(id, slot_id, patient_id)

    def update_appointment_service(self, id, appointment_id, service_id):
        entity = self.get_item_by_id(id, 'appointment_service')[0]
        appointment_id = appointment_id or entity[1]
        service_id = service_id or entity[2]
        return self.db.update_appointment_service(id, appointment_id, service_id)

    def update_diagnosis(self, id, diagnosis_name, diagnosis_code):
        entity = self.get_item_by_id(id, 'diagnosis')[0]
        diagnosis_name = diagnosis_name or entity[1]
        diagnosis_code = diagnosis_code or entity[2]
        return self.db.update_diagnosis(id, diagnosis_name, diagnosis_code)

    def update_prescription(self, id, note, appointment_id):
        entity = self.get_item_by_id(id, 'prescription')[0]
        note = note or entity[1]
        appointment_id = appointment_id or entity[2]
        return self.db.update_prescription(id, note, appointment_id)

    def update_patient_diagnosis(self, id, patient_id, diagnosis_id):
        entity = self.get_item_by_id(id, 'patient_diagnosis')[0]
        patient_id = patient_id or entity[1]
        diagnosis_id = diagnosis_id or entity[2]
        return self.db.update_patient_diagnosis(id, patient_id, diagnosis_id)

    # DELETE

    def delete_by_id(self, item_id, table):
        return self.db.delete_by_id(item_id, table)
