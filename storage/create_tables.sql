CREATE TABLE IF NOT EXISTS role (
    id SERIAL PRIMARY KEY NOT NULL,
    role_name VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS user_acc (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    role_id INT REFERENCES role (id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE IF NOT EXISTS user_activity (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    user_id BIGINT REFERENCES user_acc (id) ON DELETE CASCADE NOT NULL,
    activity_type VARCHAR(255) NOT NULL,
    date_of_activity DATE NOT NULL DEFAULT CURRENT_DATE,
    time_of_activity TIME NOT NULL DEFAULT CURRENT_TIME
);

CREATE TABLE IF NOT EXISTS patient (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    user_id BIGINT REFERENCES user_acc (id) ON DELETE CASCADE UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20) NOT NULL,
    phone_number CHAR(13) NOT NULL,
    email VARCHAR(50),
    CONSTRAINT proper_email CHECK (email ~* '.*@.+\..*'),
    CONSTRAINT proper_phone CHECK (phone_number ~* '\+375[0-9]{9}')
);

CREATE TABLE IF NOT EXISTS doctor_category (
    id SERIAL PRIMARY KEY NOT NULL,
    category_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS doctor_specialization (
    id SERIAL PRIMARY KEY NOT NULL,
    specialization_name VARCHAR(100) UNIQUE NOT NULL,
    category_id INT REFERENCES doctor_category (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS department (
    id SERIAL PRIMARY KEY NOT NULL,
    department_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS doctor (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id BIGINT REFERENCES user_acc (id) ON DELETE CASCADE UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    specialization_id INT REFERENCES doctor_specialization (id) ON DELETE SET NULL,
    department_id INT REFERENCES department (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS schedule_slot (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    date_of_slot DATE NOT NULL,
    time_of_slot TIME NOT NULL,
    doctor_id INT REFERENCES doctor (id) ON DELETE CASCADE NOT NULL,
    is_taken BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS service (
    id SERIAL PRIMARY KEY NOT NULL,
    service_name VARCHAR(50) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    doctor_id INT REFERENCES doctor (id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE IF NOT EXISTS appointment (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    slot_id BIGINT REFERENCES schedule_slot (id) ON DELETE CASCADE NOT NULL,
    patient_id BIGINT REFERENCES patient (id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE IF NOT EXISTS appointment_service (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    appointment_id BIGINT REFERENCES appointment (id) ON DELETE CASCADE NOT NULL,
    service_id INT REFERENCES service (id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE IF NOT EXISTS diagnosis (
    id SERIAL PRIMARY KEY NOT NULL,
    diagnosis_name VARCHAR(100) NOT NULL,
    diagnosis_code VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS prescription (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    note TEXT NOT NULL,
    appointment_id BIGINT REFERENCES appointment (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS patient_diagnosis (
    id BIGSERIAL PRIMARY KEY NOT NULL,
    patient_id BIGINT REFERENCES patient (id) ON DELETE CASCADE NOT NULL,
    diagnosis_id INT REFERENCES diagnosis (id) ON DELETE CASCADE NOT NULL,
    date_of_diagnosis DATE NOT NULL DEFAULT CURRENT_DATE,
    note TEXT
);
