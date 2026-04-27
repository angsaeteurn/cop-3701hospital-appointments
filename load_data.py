import pandas as pd
import sqlite3

# Connect to the database
conn = sqlite3.connect('demo_medical.db')
cursor = conn.cursor()

# Load patients
patients_df = pd.read_csv('data/patients.csv')
patients_df = patients_df.drop_duplicates(subset='patient_id')
patients_df.to_sql('Patient', conn, if_exists='replace', index=False)

# Load doctors
doctors_df = pd.read_csv('data/doctors.csv')
doctors_df.to_sql('Doctor', conn, if_exists='replace', index=False)

# Load appointments
appointments_df = pd.read_csv('data/appointments.csv')
appointments_df.to_sql('Appointment', conn, if_exists='replace', index=False)

# Load medical history
medical_history_df = pd.read_csv('data/medical_history.csv')
medical_history_df.to_sql('MedicalHistory', conn, if_exists='replace', index=False)

# Load appointment features
appointment_features_df = pd.read_csv('data/appointment_features.csv')
appointment_features_df.to_sql('AppointmentFeatures', conn, if_exists='replace', index=False)

# Load doctor availability
doctor_availability_df = pd.read_csv('data/doctor_availability.csv')
doctor_availability_df.to_sql('DoctorAvailability', conn, if_exists='replace', index=False)

# Commit and close
conn.commit()
conn.close()

print("Data loaded successfully!")