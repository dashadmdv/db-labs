--user creation
CREATE OR REPLACE FUNCTION log_create_user_function()
RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO user_activity (user_id, activity_type)
    VALUES (NEW.id, 'User registered');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS log_create_user_trigger ON user_acc;

CREATE TRIGGER log_create_user_trigger
AFTER INSERT
ON user_acc
FOR EACH ROW
EXECUTE FUNCTION log_create_user_function();

--user update
CREATE OR REPLACE FUNCTION log_update_user_function()
RETURNS TRIGGER AS
$$
BEGIN
    INSERT INTO user_activity (user_id, activity_type)
    VALUES (OLD.id, 'User updated');
    RETURN OLD;
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS log_update_user_trigger ON user_acc;

CREATE TRIGGER log_update_user_trigger
AFTER UPDATE
ON user_acc
FOR EACH ROW
EXECUTE FUNCTION log_update_user_function();

--take appointment
CREATE OR REPLACE FUNCTION update_slot_status_function()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE schedule_slot
    SET is_taken=TRUE WHERE id=NEW.slot_id;

    INSERT INTO user_activity (user_id, activity_type)
    VALUES (NEW.patient_id, 'User got an appointment');

    RETURN NEW;
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_slot_status_trigger ON appointment;

CREATE TRIGGER update_slot_status_trigger
AFTER INSERT
ON appointment
FOR EACH ROW
EXECUTE FUNCTION update_slot_status_function();

--cancel appointment
CREATE OR REPLACE FUNCTION cancel_slot_status_function()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE schedule_slot
    SET is_taken=FALSE WHERE id=OLD.slot_id;

    INSERT INTO user_activity (user_id, activity_type)
    VALUES (OLD.patient_id, 'User cancelled an appointment');

    RETURN OLD;
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS cancel_slot_status_trigger ON appointment;

CREATE TRIGGER cancel_slot_status_trigger
AFTER DELETE
ON appointment
FOR EACH ROW
EXECUTE FUNCTION cancel_slot_status_function();


-- procedure
CREATE OR REPLACE PROCEDURE get_patient_appointments(patient_id_param BIGINT)
AS $$
DECLARE
    appointment_info RECORD;
BEGIN
    FOR appointment_info IN
        SELECT
            a.id AS appointment_id,
            s.date_of_slot,
            s.time_of_slot,
            d.first_name AS doctor_first_name,
            d.last_name AS doctor_last_name,
            ser.service_name,
            ser.price
        FROM appointment a
        JOIN schedule_slot s ON a.slot_id = s.id
        JOIN doctor d ON s.doctor_id = d.id
        LEFT JOIN appointment_service aps ON a.id = aps.appointment_id
        LEFT JOIN service ser ON aps.service_id = ser.id
        WHERE a.patient_id = patient_id_param
    LOOP
        RAISE INFO 'Appointment ID: %, Date: %, Time: %, Doctor: % %, Service: %, Price: %',
                     appointment_info.appointment_id,
                     appointment_info.date_of_slot,
                     appointment_info.time_of_slot,
                     appointment_info.doctor_first_name,
                     appointment_info.doctor_last_name,
                     appointment_info.service_name,
                     appointment_info.price;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

