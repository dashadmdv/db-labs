# DATA MODELS AND DATABASE MANAGEMENT SYSTEMS
## Topic: medical center

## Functional requirements
* User authorization
* User management (CRUD)
* The role system (roles: PATIENT, DOCTOR, ADMIN)
* Logging user actions
* Departments CRUD (ADMIN)
* Doctor categories&specializations CRUD (ADMIN)
* Schedule CRUD (ADMIN)
* Services CRUD (ADMIN)
* Appointments CRUD (PATIENT, DOCTOR)
* Diagnoses CRUD (DOCTOR)
* Prescriptions CRUD (DOCTOR)

## Use cases
* Non-authorized user
  * See doctors list
  * See doctor's services list
  * See appointments schedule
  * Authorize
* Authorized user
  * Patient
    * See doctors list
    * See doctor's services list
    * See appointments schedule
    * Make an appointment
  * Doctor
    * See their appointments
    * User diagnosis CRUD
    * Prescriptions CRUD
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
   * FOREIGN KEY user_id REFERENCES user(id) NOT NULL,
   * first_name VARCHAR(50) NOT NULL,
   * last_name VARCHAR(50) NOT NULL,
   * date_of_birth DATE NOT NULL,
   * gender VARCHAR(20) NOT NULL,
   * phone_number VARCHAR(20) ~ '\+[0-9]{6,19}' NOT NULL,
   * email VARCHAR(50) ~ '.*@.+\..*'
5. `doctor`
   * id SERIAL PRIMARY KEY NOT NULL,
   * FOREIGN KEY user_id REFERENCES user(id),
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
   * specialization_name VARCHAR(25) UNIQUE NOT NULL
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
    * price DECIMAL(12,2) NOT NULL
11. `appointment`
    * id BIGSERIAL PRIMARY KEY NOT NULL,
    * FOREIGN KEY slot_id REFERENCES schedule_slot(id) NOT NULL,
    * FOREIGN KEY patient_id REFERENCES patient(id) NOT NULL,
    * FOREIGN KEY service_id REFERENCES service(id) NOT NULL,
    * FOREIGN KEY prescription_id REFERENCES prescription(id)
12. `diagnosis`
    * id SERIAL PRIMARY KEY NOT NULL,
    * diagnosis_name VARCHAR(50) NOT NULL,
    * diagnosis_code VARCHAR(10) NOT NULL,
13. `prescription`
    * id BIGSERIAL PRIMARY KEY NOT NULL,
    * note TEXT NOT NULL
14. `user_diagnosis`
    * id BIGSERIAL PRIMARY KEY NOT NULL,
    * FOREIGN KEY user_id REFERENCES user(id) NOT NULL,
    * FOREIGN KEY diagnosis_id REFERENCES diagnosis(id) NOT NULL
    * note TEXT

![Entity diagram](https://github.com/dashadmdv/db-labs/assets/69718734/ecc907f3-56a4-4fcd-a74c-521a44802fbf)
