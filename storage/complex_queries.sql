--total cost of services from catalog by doctor
SELECT
    first_name,
    last_name,
    (SELECT COALESCE(SUM(service.price), 0) FROM service WHERE service.doctor_id = doctor.id) AS total_service_cost
FROM doctor;

--total cash by doctor
SELECT
    d.first_name,
    d.last_name,
    COALESCE(SUM(ser.price), 0) AS total_revenue
FROM doctor d
LEFT JOIN schedule_slot s ON d.id = s.doctor_id
LEFT JOIN appointment a ON s.id = a.slot_id
LEFT JOIN appointment_service aps ON a.id = aps.appointment_id
LEFT JOIN service ser ON aps.service_id = ser.id
GROUP BY d.id;

--list of patients who got appointment at least once
SELECT
    p.first_name || ' ' || p.last_name AS patient_name,
    p.date_of_birth,
    a.date_of_activity
FROM patient p
JOIN user_activity a ON p.user_id = a.user_id
WHERE a.activity_type = 'User got an appointment'
ORDER BY p.last_name, p.first_name;

--total service cost for each patient
SELECT
    p.first_name || ' ' || p.last_name AS patient_name,
    SUM(s.price) AS total_cost
FROM patient p
JOIN appointment a ON p.id = a.patient_id
JOIN appointment_service aps ON a.id = aps.appointment_id
JOIN service s ON aps.service_id = s.id
GROUP BY p.id
ORDER BY total_cost DESC;

--3 most common diagnoses
SELECT
    d.diagnosis_name,
    COUNT(pd.id) AS diagnosis_count
FROM diagnosis d
JOIN patient_diagnosis pd ON d.id = pd.diagnosis_id
GROUP BY d.id
ORDER BY diagnosis_count DESC
LIMIT 3;

--doctors who made more than 1 service
SELECT
    doctor.id,
    doctor.first_name,
    doctor.last_name,
    COUNT(appointment_service.id) AS total_services
FROM
    doctor
JOIN
    service ON doctor.id = service.doctor_id
JOIN
    appointment_service ON service.id = appointment_service.service_id
GROUP BY
    doctor.id, doctor.first_name, doctor.last_name
HAVING
    COUNT(appointment_service.id) > 1;

--average doctors' service count by specialization
SELECT
    doctor.id,
    doctor.first_name,
    doctor.last_name,
    doctor_specialization.specialization_name,
    AVG(COUNT(appointment_service.id)) OVER (PARTITION BY doctor_specialization.id) AS avg_services_per_doctor
FROM doctor
JOIN doctor_specialization ON doctor.specialization_id = doctor_specialization.id
LEFT JOIN service ON doctor.id = service.doctor_id
LEFT JOIN appointment_service ON service.id = appointment_service.service_id
GROUP BY doctor.id, doctor.first_name, doctor.last_name, doctor_specialization.specialization_name, doctor_specialization.id;

--count patients by age groups
SELECT
    CASE
        WHEN extract(year from age(date_of_birth)) >= 0 AND extract(year from age(date_of_birth)) < 18 THEN '0-17'
        WHEN extract(year from age(date_of_birth)) >= 18 AND extract(year from age(date_of_birth)) < 30 THEN '18-29'
        WHEN extract(year from age(date_of_birth)) >= 30 AND extract(year from age(date_of_birth)) < 50 THEN '30-49'
        WHEN extract(year from age(date_of_birth)) >= 50 THEN '50+'
        ELSE 'Unknown'
    END AS age_group,
    COUNT(*) AS patient_count
FROM patient
GROUP BY age_group
ORDER BY age_group;

--put together info about doctors' specializations and their services
EXPLAIN ANALYZE
SELECT
    d.first_name || ' ' || d.last_name AS doctor_name,
    ds.specialization_name,
    'Doctor' AS role
FROM doctor d
JOIN doctor_specialization ds ON d.specialization_id = ds.id
UNION
SELECT
    d.first_name || ' ' || d.last_name,
    s.service_name,
    'Service'
FROM doctor d
JOIN service s ON d.id = s.doctor_id;


--view for user activity
CREATE OR REPLACE VIEW patient_activity_view AS
SELECT
    p.first_name || ' ' || p.last_name AS patient_name,
    a.activity_type,
    a.date_of_activity,
    a.time_of_activity
FROM patient p
JOIN user_activity a ON p.user_id = a.user_id;

--daily report by doctor
CREATE OR REPLACE VIEW daily_report_by_doctor AS
SELECT
    d.id AS doctor_id,
    d.first_name,
    d.last_name,
    s.date_of_slot,
    COUNT(a.id) AS appointments_count
FROM doctor d
JOIN schedule_slot s ON d.id = s.doctor_id
LEFT JOIN appointment a ON s.id = a.slot_id
GROUP BY d.id, d.first_name, d.last_name, s.date_of_slot;

--patient last appointments
CREATE OR REPLACE VIEW patient_last_appointment_view AS
SELECT
    p.id AS patient_id,
    p.first_name,
    p.last_name,
    MAX(s.date_of_slot) AS last_visit_date
FROM patient p
JOIN appointment a ON p.id = a.patient_id
JOIN schedule_slot s ON a.slot_id = s.id
GROUP BY p.id, p.first_name, p.last_name;
