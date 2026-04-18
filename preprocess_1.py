import os
from pathlib import Path
import pandas as pd
import numpy as np

RNG = np.random.default_rng(42)

DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

RAW_FILE = Path('KaggleV2-May-2016.csv')
if not RAW_FILE.exists():
    raise FileNotFoundError(
        "KaggleV2-May-2016.csv was not found in the current folder. "
        "Place the Kaggle file next to this script and run again."
    )


raw = pd.read_csv(RAW_FILE, low_memory=False)


raw['ScheduledDay'] = pd.to_datetime(raw['ScheduledDay'], errors='coerce', utc=True).dt.tz_localize(None)
raw['AppointmentDay'] = pd.to_datetime(raw['AppointmentDay'], errors='coerce', utc=True).dt.tz_localize(None)

# ---------------- Patients ----------------
first_names = [
    'Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Avery', 'Riley', 'Cameron', 'Skyler', 'Quinn',
    'Parker', 'Reese', 'Rowan', 'Drew', 'Jamie', 'Logan', 'Dakota', 'Hayden', 'Kendall', 'Blake'
]
last_names = [
    'Smith', 'Johnson', 'Brown', 'Williams', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson',
    'Martinez', 'Anderson', 'Taylor', 'Thomas', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson'
]

patients = raw[['PatientId', 'Gender', 'Age']].drop_duplicates().copy()
patients.columns = ['patient_id', 'gender', 'age']
patients['age'] = pd.to_numeric(patients['age'], errors='coerce').fillna(0).clip(lower=0).astype(int)


patients['patient_firstname'] = patients['patient_id'].apply(
    lambda x: first_names[int(x) % len(first_names)]
)
patients['patient_lastname'] = patients['patient_id'].apply(
    lambda x: last_names[int(x // 7) % len(last_names)]
)

# Approximate DOB from age using a fixed reference date for consistency
reference_date = pd.Timestamp('2016-05-01')
patients['DOB'] = reference_date - pd.to_timedelta(patients['age'] * 365, unit='D')
patients['DOB'] = patients['DOB'].dt.date

patients = patients[['patient_id', 'patient_firstname', 'patient_lastname', 'gender', 'DOB']]
patients.to_csv(DATA_DIR / 'patients.csv', index=False)

# ---------------- Doctors ----------------
# Schema requires: doctor_id, doctor_firstname, doctor_lastname, specialty, license_number
specialties = ['General', 'Cardiology', 'Pediatrics', 'Dermatology', 'Neurology']
doctor_ids = list(range(1, 21))
doctors = pd.DataFrame({
    'doctor_id': doctor_ids,
    'doctor_firstname': [
        'Emily', 'Liam', 'Sophia', 'Noah', 'Olivia', 'Elijah', 'Ava', 'James', 'Isabella', 'Benjamin',
        'Mia', 'Lucas', 'Charlotte', 'Henry', 'Amelia', 'Alexander', 'Harper', 'Michael', 'Evelyn', 'Daniel'
    ],
    'doctor_lastname': [
        'Carter', 'Nguyen', 'Patel', 'Lopez', 'Hall', 'Young', 'Allen', 'King', 'Wright', 'Scott',
        'Green', 'Baker', 'Adams', 'Nelson', 'Hill', 'Ramirez', 'Campbell', 'Mitchell', 'Roberts', 'Turner'
    ],
    'specialty': [specialties[i % len(specialties)] for i in range(len(doctor_ids))],
    'license_number': [f'LIC{i:04d}' for i in doctor_ids],
})
doctors.to_csv(DATA_DIR / 'doctors.csv', index=False)

# Random doctor assignment for each appointment row
raw['doctor_id'] = RNG.integers(1, 21, size=len(raw))

# ---------------- Appointments ----------------
appointments = raw[['AppointmentID', 'PatientId', 'doctor_id', 'ScheduledDay', 'AppointmentDay']].copy()
appointments.columns = ['appointment_id', 'patient_id', 'doctor_id', 'scheduled_day', 'appointment_day']
appointments['scheduled_day'] = appointments['scheduled_day'].dt.strftime('%Y-%m-%d %H:%M:%S')
appointments['appointment_day'] = appointments['appointment_day'].dt.strftime('%Y-%m-%d %H:%M:%S')
appointments.to_csv(DATA_DIR / 'appointments.csv', index=False)

# ---------------- Medical History ----------------
# Schema requires only: patient_id, diagnosis_date, is_chronic
history = raw[['PatientId', 'Hipertension', 'Diabetes']].drop_duplicates().copy()
history.columns = ['patient_id', 'hypertension', 'diabetes']
history['is_chronic'] = ((history['hypertension'] == 1) | (history['diabetes'] == 1)).astype(int)

# Give each patient a deterministic diagnosis date
base_date = pd.Timestamp('2014-01-01')
history['diagnosis_date'] = history['patient_id'].apply(
    lambda x: (base_date + pd.Timedelta(days=int(x) % 700)).date()
)
history = history[['patient_id', 'diagnosis_date', 'is_chronic']]
history.to_csv(DATA_DIR / 'medical_history.csv', index=False)

# ---------------- Appointment Features ----------------
# Schema requires: appointment_id, days_since_last_visit, sms_received, no_show_count
features = raw[['AppointmentID', 'SMS_received', 'No-show']].copy()
features.columns = ['appointment_id', 'sms_received', 'no_show_text']
features['no_show_count'] = (features['no_show_text'].astype(str).str.strip().str.upper() == 'YES').astype(int)

# Use the gap between scheduling and appointment day as a stand-in for days since last visit
feature_dates = raw[['ScheduledDay', 'AppointmentDay']].copy()
features['days_since_last_visit'] = (
    (feature_dates['AppointmentDay'] - feature_dates['ScheduledDay']).dt.total_seconds() / 86400.0
).fillna(0).clip(lower=0).round().astype(int)
features = features[['appointment_id', 'days_since_last_visit', 'sms_received', 'no_show_count']]
features.to_csv(DATA_DIR / 'appointment_features.csv', index=False)

# ---------------- Doctor Availability ----------------
# Create 5 availability slots per doctor
availability_rows = []
availability_id = 1
availability_dates = pd.date_range(start='2023-01-01', periods=5, freq='7D')
slots = [('09:00:00', '12:00:00'), ('13:00:00', '17:00:00')]

for doctor_id in doctor_ids:
    for i, available_date in enumerate(availability_dates):
        start_time, end_time = slots[i % len(slots)]
        availability_rows.append({
            'availability_id': availability_id,
            'doctor_id': doctor_id,
            'available_date': available_date.date(),
            'start_time': start_time,
            'end_time': end_time,
        })
        availability_id += 1

availability = pd.DataFrame(availability_rows)
availability.to_csv(DATA_DIR / 'doctor_availability.csv', index=False)

print('Created:')
for name in [
    'patients.csv',
    'doctors.csv',
    'appointments.csv',
    'medical_history.csv',
    'appointment_features.csv',
    'doctor_availability.csv',
]:
    print(DATA_DIR / name)
