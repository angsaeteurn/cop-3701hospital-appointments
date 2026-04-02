-- ---------------- Patients ----------------
LOAD DATA INFILE 'data/patients.csv'
INTO TABLE Patient
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(patient_id, gender, age);

-- ---------------- Doctors ----------------
LOAD DATA INFILE 'data/doctors.csv'
INTO TABLE Doctor
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(doctor_id, doctor_firstname, doctor_lastname, specialty, license_number);

-- ---------------- Appointments ----------------
LOAD DATA INFILE 'data/appointments.csv'
INTO TABLE Appointment
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(appointment_id, patient_id, doctor_id, @scheduled_day, @appointment_day)
SET scheduled_day = STR_TO_DATE(@scheduled_day, '%Y-%m-%d %H:%i:%s'),
    appointment_day = STR_TO_DATE(@appointment_day, '%Y-%m-%d %H:%i:%s');

-- ---------------- Medical History ----------------
LOAD DATA INFILE 'data/medical_history.csv'
INTO TABLE MedicalHistory
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(patient_id, hypertension, diabetes, alcoholism, handicap, is_chronic);

-- ---------------- Appointment Features ----------------
LOAD DATA INFILE 'data/appointment_features.csv'
INTO TABLE AppointmentFeatures
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(appointment_id, scholarship, sms_received, no_show_count);

-- ---------------- Doctor Availability ----------------
LOAD DATA INFILE 'data/doctor_availability.csv'
INTO TABLE DoctorAvailability
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(availability_id, doctor_id, @available_date, @start_time, @end_time)
SET available_date = STR_TO_DATE(@available_date, '%Y-%m-%d'),
    start_time = STR_TO_DATE(@start_time, '%H:%i:%s'),
    end_time = STR_TO_DATE(@end_time, '%H:%i:%s');