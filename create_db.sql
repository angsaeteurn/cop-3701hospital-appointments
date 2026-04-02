CREATE TABLE Patient (
    patient_id BIGINT PRIMARY KEY,
    patient_firstname VARCHAR(50),
    patient_lastname VARCHAR(50),
    gender CHAR(1),
    DOB DATE
);

CREATE TABLE Doctor (
    doctor_id INT PRIMARY KEY,
    doctor_firstname VARCHAR(50),
    doctor_lastname VARCHAR(50),
    specialty VARCHAR(50),
    license_number VARCHAR(50)
);

CREATE TABLE Appointment (
    appointment_id INT PRIMARY KEY,
    patient_id BIGINT,
    doctor_id INT,
    scheduled_day DATETIME,
    appointment_day DATETIME,
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id)
);

CREATE TABLE MedicalHistory (
    patient_id BIGINT PRIMARY KEY,
    diagnosis_date DATE,
    is_chronic BOOLEAN,
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);

CREATE TABLE AppointmentFeatures (
    appointment_id INT PRIMARY KEY,
    days_since_last_visit INT,
    sms_received BOOLEAN,
    no_show_count INT,
    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id)
);

CREATE TABLE DoctorAvailability (
    availability_id INT PRIMARY KEY,
    doctor_id INT,
    available_date DATE,
    start_time TIME,
    end_time TIME,
    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id)
);