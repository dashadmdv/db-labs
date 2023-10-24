update user_acc
set password='password' where id=5;

select * from patient
where gender='Male';

select username from user_acc
where role_id=2;

select count(*) from patient
where gender='Male';

/* asceding order */
select * from user_acc
order by role_id;

/* descending order */
select * from user_acc
order by role_id desc;

/* show full role entity instead of role_id in user_acc table */
select * from user_acc
join role on user_acc.role_id=role.id;

/* show full patient info instead of patient_id in appointment table */
select * from appointment
join patient on appointment.patient_id=patient.id;

/* get female patients 18+ years old */
select * from patient
where gender='Female' AND (extract(year from current_date) - extract(year from date_of_birth)) > 17;

/* the same, but shorter query */
select * from patient
where gender='Female' AND extract(year from age(date_of_birth)) > 17;

/* get total appointments cost of user with id=1 */
select sum(price) from appointment_service
join service on appointment_service.service_id=service.id
join appointment on appointment_service.appointment_id=appointment.id
where patient_id=1;