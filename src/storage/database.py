import datetime
import psycopg2
import src.storage.create_database as db
from src.config import (
    DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
)

db_config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME,
    'port': DB_PORT
}


class Database:
    def __init__(self):
        db.create_database()
        db.create_tables()
        self._conn = psycopg2.connect(**db_config)
        self._cursor = self._conn.cursor()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        self.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    # READ

    def show_table(self, name):
        return self.query(f"SELECT * FROM {name} ORDER BY id;")

    def select_by_id(self, item_id, table):
        sql = f"SELECT * FROM {table} WHERE id = {item_id};"
        self.execute(sql)
        return self.fetchone()

    def get_usernames(self):
        return self.query(f"SELECT username FROM user_acc;")

    def get_user_by_username(self, username):
        sql = f"SELECT id FROM user_acc WHERE username = '{username}';"
        self.execute(sql)
        return self.fetchone()

    # CREATE

    def create_role(self, name):
        try:
            sql = f"""
                        INSERT INTO role (role_name)
                        VALUES ('{name}');
                    """
            self.execute(sql)
            return "Role added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_user(self, username, password, role_id):
        try:
            sql = f"""
                        INSERT INTO user_acc (username, password, role_id)
                        VALUES ('{username}', '{password}', {role_id});
                    """
            self.execute(sql)
            return "Role added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_user_activity(self, user_id, activity_type, date_of_activity='', time_of_activity=''):
        try:
            sql = f"""
                        INSERT INTO user_activity (user_id, activity_type, date_of_activity, time_of_activity)
                        VALUES ({user_id}, '{activity_type}', '{date_of_activity}', '{time_of_activity}');
                    """
            self.execute(sql)
            return "User activity added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_patient(self, user_id, first_name, last_name, date_of_birth, gender, phone_number, email=''):
        try:
            sql = f"""
                        INSERT INTO patient (user_id, first_name, last_name, date_of_birth, gender, phone_number, email)
                        VALUES ({user_id}, '{first_name}', '{last_name}', '{date_of_birth}', '{gender}', '{phone_number}', '{email}');
                    """
            self.execute(sql)
            return "Patient added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_doc_category(self, name):
        try:
            sql = f"""
                        INSERT INTO doctor_category (category_name)
                        VALUES ('{name}');
                    """
            self.execute(sql)
            return "Doctor category added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_doc_spec(self, name, category_id):
        try:
            sql = f"""
                        INSERT INTO doctor_specialization (specialization_name, category_id)
                        VALUES ('{name}', {category_id});
                    """
            self.execute(sql)
            return "Doctor specialization added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_department(self, name):
        try:
            sql = f"""
                        INSERT INTO department (department_name)
                        VALUES ('{name}');
                    """
            self.execute(sql)
            return "Department added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_doctor(self, user_id, first_name, last_name, gender, specialization_id, department_id):
        try:
            sql = f"""
                        INSERT INTO doctor (user_id, first_name, last_name, gender, specialization_id, department_id)
                        VALUES ({user_id}, '{first_name}', '{last_name}', '{gender}', {specialization_id}, {department_id});
                    """
            self.execute(sql)
            return "Doctor added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_doctor_min(self, user_id, first_name, last_name, gender):
        try:
            sql = f"""
                        INSERT INTO doctor (user_id, first_name, last_name, gender)
                        VALUES ({user_id}, '{first_name}', '{last_name}', '{gender}');
                    """
            self.execute(sql)
            return "Doctor added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_slot(self, date_of_slot, time_of_slot, doctor_id):
        try:
            sql = f"""
                        INSERT INTO schedule_slot (date_of_slot, time_of_slot, doctor_id)
                        VALUES ('{date_of_slot}', '{time_of_slot}', {doctor_id});
                    """
            self.execute(sql)
            return "Schedule slot added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_service(self, service_name, price, doctor_id):
        try:
            sql = f"""
                        INSERT INTO service (service_name, price, doctor_id)
                        VALUES ('{service_name}', {price}, {doctor_id});
                    """
            self.execute(sql)
            return "Service added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_appointment(self, slot_id, patient_id):
        try:
            sql = f"""
                        INSERT INTO appointment (slot_id, patient_id)
                        VALUES ({slot_id}, {patient_id});
                    """
            self.execute(sql)
            return "Appointment added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_appointment_service(self, appointment_id, service_id):
        try:
            sql = f"""
                        INSERT INTO appointment_service (appointment_id, service_id)
                        VALUES ({appointment_id}, {service_id});
                    """
            self.execute(sql)
            return "Service added to appointment!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_diagnosis(self, diagnosis_name, diagnosis_code):
        try:
            sql = f"""
                        INSERT INTO appointment_service (appointment_id, service_id)
                        VALUES ('{diagnosis_name}', '{diagnosis_code}');
                    """
            self.execute(sql)
            return "Diagnosis added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_prescription(self, note, appointment_id):
        try:
            sql = f"""
                        INSERT INTO prescription (note, appointment_id)
                        VALUES ('{note}', {appointment_id});
                    """
            self.execute(sql)
            return "Prescription added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def create_patient_diagnosis(self, patient_id, diagnosis_id):
        try:
            sql = f"""
                        INSERT INTO patient_diagnosis (patient_id, diagnosis_id)
                        VALUES ({patient_id}, {diagnosis_id});
                    """
            self.execute(sql)
            return "Diagnosis added to patient!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    # UPDATE

    def update_role(self, id, name):
        try:
            sql = f"""
                        UPDATE role
                        SET role_name='{name}'
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Role updated!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_user(self, id, username, password, role_id):
        try:
            sql = f"""
                        UPDATE user_acc 
                        SET username='{username}', password='{password}', role_id={role_id}
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Role added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_user_activity(self, id, user_id, activity_type, date_of_activity='', time_of_activity=''):
        try:
            sql = f"""
                        UPDATE user_activity 
                        SET user_id={user_id}, activity_type='{activity_type}', date_of_activity='{date_of_activity}', 
                        time_of_activity='{time_of_activity}'
                        WHERE id={id};
                    """
            self.execute(sql)
            return "User activity added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_patient(self, id, user_id, first_name, last_name, date_of_birth, gender, phone_number, email=''):
        try:
            sql = f"""
                        UPDATE patient 
                        SET user_id={user_id}, first_name='{first_name}', last_name='{last_name}', 
                        date_of_birth='{date_of_birth}', gender='{gender}', phone_number='{phone_number}', email='{email}')
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Patient added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_doc_category(self, id, name):
        try:
            sql = f"""
                        UPDATE doctor_category 
                        SET category_name='{name}'
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Doctor category added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_doc_spec(self, id, name, category_id):
        try:
            sql = f"""
                        UPDATE doctor_specialization 
                        SET specialization_name='{name}', category_id={category_id}
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Doctor specialization added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_department(self, id, name):
        try:
            sql = f"""
                        UPDATE department 
                        SET department_name='{name}'
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Department added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_doctor(self, id, user_id, first_name, last_name, gender, specialization_id, department_id):
        try:
            sql = f"""
                        UPDATE doctor 
                        SET user_id={user_id}, first_name='{first_name}', last_name='{last_name}', gender='{gender}', 
                        specialization_id={specialization_id}, department_id={department_id}
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Doctor added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_slot(self, id, date_of_slot, time_of_slot, doctor_id):
        try:
            sql = f"""
                        UPDATE schedule_slot 
                        SET date_of_slot='{date_of_slot}', time_of_slot='{time_of_slot}', doctor_id={doctor_id}
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Schedule slot added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_service(self, id, service_name, price, doctor_id):
        try:
            sql = f"""
                        UPDATE service 
                        SET service_name='{service_name}', price={price}, doctor_id={doctor_id}
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Service added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_appointment(self, id, slot_id, patient_id):
        try:
            sql = f"""
                        UPDATE appointment 
                        SET slot_id={slot_id}, patient_id={patient_id}
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Appointment added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_appointment_service(self, id, appointment_id, service_id):
        try:
            sql = f"""
                        UPDATE appointment_service 
                        SET appointment_id={appointment_id}, service_id={service_id}
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Service added to appointment!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_diagnosis(self, id, diagnosis_name, diagnosis_code):
        try:
            sql = f"""
                        UPDATE appointment_service 
                        SET appointment_id='{diagnosis_name}', service_id='{diagnosis_code}'
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Diagnosis added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_prescription(self, id, note, appointment_id):
        try:
            sql = f"""
                        UPDATE prescription 
                        SET note='{note}', appointment_id={appointment_id}
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Prescription added!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    def update_patient_diagnosis(self, id, patient_id, diagnosis_id):
        try:
            sql = f"""
                        UPDATE patient_diagnosis 
                        SET patient_id={patient_id}, diagnosis_id={diagnosis_id})
                        WHERE id={id};
                    """
            self.execute(sql)
            return "Diagnosis added to patient!"
        except Exception as e:
            self.execute("ROLLBACK")
            return e

    # DELETE

    def delete_by_id(self, item_id, table):
        sql = f"DELETE FROM {table} WHERE id = {item_id};"
        self.execute(sql)
        return "Item deleted!"
