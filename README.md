# DATA MODELS AND DATABASE MANAGEMENT SYSTEMS
## Topic: medical center

## Functional requirements
* User authorization
* Work with entities (CRUD)
* The role system (roles: PATIENT, DOCTOR, ADMIN)
* Logging user actions

## Use cases
* Non-authorized user
  * Authorize
  * Registration
* Authorized user
  * Patient
    * Make an appointment
    * See their appointments
    * See their diagnoses
  * Doctor
    * See their appointments
    * Create patient diagnosis
    * Create prescriptions
  * Admin
    * CRUD with all entities

## Entities
1. `user`
   * id BIGSERIAL PRIMARY KEY NOT NULL,
   * username VARCHAR(50) UNIQUE NOT NULL,
   * password VARCHAR(50) NOT NULL,
   * FOREIGN KEY role_id REFERENCES role(id) NOT NULL
2. `user_activity`
   * id BIGSERIAL PRIMARY KEY NOT NULL,
   * FOREIGN KEY user_id REFERENCES user(id) NOT NULL,
   * activity_type VARCHAR(255) NOT NULL,
   * date_of_activity DATE NOT NULL,
   * time_of_activity TIME NOT NULL
3. `role`
   * id SERIAL PRIMARY KEY NOT NULL,
   * role_name VARCHAR(25) UNIQUE NOT NULL
4. `patient`
   * id BIGSERIAL PRIMARY KEY NOT NULL,
   * FOREIGN KEY user_id REFERENCES user(id) UNIQUE NOT NULL,
   * first_name VARCHAR(50) NOT NULL,
   * last_name VARCHAR(50) NOT NULL,
   * date_of_birth DATE NOT NULL,
   * gender VARCHAR(20) NOT NULL,
   * phone_number CHAR(13) ~ `'\+375[0-9]{9}'` NOT NULL,
   * email VARCHAR(50) ~ `'.*@.+\..*'`
5. `doctor`
   * id SERIAL PRIMARY KEY NOT NULL,
   * FOREIGN KEY user_id REFERENCES user(id) UNIQUE NOT NULL,
   * first_name VARCHAR(50) NOT NULL,
   * last_name VARCHAR(50) NOT NULL,
   * gender VARCHAR(20) NOT NULL,
   * FOREIGN KEY specialization_id REFERENCES doctor_specialization(id) NOT NULL,
   * FOREIGN KEY department_id REFERENCES department(id) NOT NULL
6. `doctor_category`
   * id SERIAL PRIMARY KEY NOT NULL,
   * category_name VARCHAR(25) UNIQUE NOT NULL
7. `doctor_specialization`
   * id SERIAL PRIMARY KEY NOT NULL,
   * specialization_name VARCHAR(25) UNIQUE NOT NULL,
   * FOREIGN KEY category_id REFERENCES doctor_category(id) NOT NULL
8. `department`
   * id SERIAL PRIMARY KEY NOT NULL,
   * department_name VARCHAR(50) UNIQUE NOT NULL,
9. `schedule_slot`
   * id BIGSERIAL PRIMARY KEY NOT NULL,
   * date_of_slot DATE NOT NULL,
   * time_of_slot TIME NOT NULL,
   * FOREIGN KEY doctor_id REFERENCES doctor(id) NOT NULL,
   * is_taken BOOLEAN NOT NULL DEFAULT FALSE
10. `service`
    * id SERIAL PRIMARY KEY NOT NULL,
    * service_name VARCHAR(50) NOT NULL,
    * price DECIMAL(12,2) NOT NULL,
    * FOREIGN KEY doctor_id REFERENCES doctor(id) NOT NULL
11. `appointment`
    * id BIGSERIAL PRIMARY KEY NOT NULL,
    * FOREIGN KEY slot_id REFERENCES schedule_slot(id) NOT NULL,
    * FOREIGN KEY patient_id REFERENCES patient(id) NOT NULL,
    * FOREIGN KEY prescription_id REFERENCES prescription(id)
12. `appointment_service` (MTM)
    * id BIGSERIAL PRIMARY KEY NOT NULL,
    * FOREIGN KEY appointment_id REFERENCES appointment(id) NOT NULL,
    * FOREIGN KEY service_id REFERENCES service(id) NOT NULL
13. `diagnosis`
    * id SERIAL PRIMARY KEY NOT NULL,
    * diagnosis_name VARCHAR(50) NOT NULL,
    * diagnosis_code VARCHAR(10) NOT NULL
14. `prescription`
    * id BIGSERIAL PRIMARY KEY NOT NULL,
    * note TEXT NOT NULL,
    * FOREIGN KEY appointment_id REFERENCES appointment(id) NOT NULL
15. `patient_diagnosis` (MTM)
    * id BIGSERIAL PRIMARY KEY NOT NULL,
    * FOREIGN KEY patient_id REFERENCES patient(id) NOT NULL,
    * FOREIGN KEY diagnosis_id REFERENCES diagnosis(id) NOT NULL,
    * date_of_diagnosis DATE NOT NULL,
    * note TEXT

![Entity diagram](https://github.com/dashadmdv/db-labs/assets/69718734/2390f553-ba61-426a-9a00-a8ba8288ace4)
