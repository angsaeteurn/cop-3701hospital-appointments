import pandas as pd
import numpy as np
import os

# create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# read raw data
df = pd.read_csv("KaggleV2-May-2016.csv")

# ---------------- Patients ----------------
patients = df[['PatientId', 'Gender', 'Age']].drop_duplicates()
patients.columns = ['patient_id', 'gender', 'age']
# convert age to int if needed
patients['age'] = patients['age'].astype(int)
patients.to_csv('data/patients.csv', index=False)

# ---------------- Doctors (FAKE) ----------------
doctor_ids = list(range(1, 21))
doctor_firstnames = [f"First_{i}" for i in doctor_ids]
doctor_lastnames = [f"Last_{i}" for i in doctor_ids]
specialties = ["General"] * 20
license_numbers = [f"LIC{i:04}" for i in doctor_ids]

doctors = pd.DataFrame({
    'doctor_id': doctor_ids,
    'doctor_firstname': doctor_firstnames,
    'doctor_lastname': doctor_lastnames,
    'specialty': specialties,
    'license_number': license_numbers
})
doctors.to_csv('data/doctors.csv', index=False)

# ---------------- Assign doctors randomly ----------------
df['doctor_id'] = np.random.choice(doctor_ids, size=len(df))

# ---------------- Appointments ----------------
appointments = df[['AppointmentID', 'PatientId', 'doctor_id',
                   'ScheduledDay', 'AppointmentDay']]
appointments.columns = ['appointment_id', 'patient_id', 'doctor_id',
                        'scheduled_day', 'appointment_day']
# convert to datetime
appointments['scheduled_day'] = pd.to_datetime(appointments['scheduled_day'])
appointments['appointment_day'] = pd.to_datetime(appointments['appointment_day'])
appointments.to_csv('data/appointments.csv', index=False)

# ---------------- Medical History ----------------
history = df[['PatientId', 'Hipertension', 'Diabetes',
              'Alcoholism', 'Handcap']].drop_duplicates()
history.columns = ['patient_id', 'hypertension', 'diabetes',
                   'alcoholism', 'handicap']
# create a fake 'is_chronic' boolean
history['is_chronic'] = (history[['hypertension','diabetes']].sum(axis=1) > 0).astype(int)
history.to_csv('data/medical_history.csv', index=False)

# ---------------- Appointment Features ----------------
features = df[['AppointmentID', 'Scholarship', 'SMS_received', 'No-show']]
features.columns = ['appointment_id', 'scholarship', 'sms_received', 'no_show_count']
features.to_csv('data/appointment_features.csv', index=False)

# ---------------- Doctor Availability (FAKE) ----------------
availability = pd.DataFrame({
    'availability_id': range(1, 101),
    'doctor_id': np.random.choice(doctor_ids, 100),
    'available_date': pd.date_range(start='2023-01-01', periods=100),
    'start_time': np.random.choice(['09:00:00', '13:00:00', '17:00:00'], 100),
    'end_time': np.random.choice(['12:00:00', '16:00:00', '20:00:00'], 100)
})
availability.to_csv('data/doctor_availability.csv', index=False)