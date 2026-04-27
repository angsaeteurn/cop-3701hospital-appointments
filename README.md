---

# COP-3710 Hospital Appointments Database

## Domain & Scope

This project is a database management system designed to manage hospital appointments.
The goal of the system is to organize patient demographic information, schedule appointments, and track appointment outcomes (show or no-show).

The database is designed to support:

* Appointment conflict detection
* Tracking doctor availability
* Storing medical history records
* Supporting no-show prediction features
* Running time-based queries for daily and weekly schedules

The system focuses on improving scheduling efficiency and reducing missed appointments.

This database was designed based on an ER diagram consisting of six entities:
**Patient, Doctor, Appointment, MedicalHistory, AppointmentFeatures, and DoctorAvailability.**

The dataset used was the **Kaggle medical appointment dataset** containing over 100,000 records.

The database was normalized to **Third Normal Form (3NF):**

* Each table has a primary key
* No partial dependencies exist
* No transitive dependencies exist

Synthetic data was generated for **Doctor** and **DoctorAvailability** since the dataset did not include this information.
Foreign key relationships were preserved to ensure meaningful joins across tables.

## Users

The primary users of this system include:

* Hospital scheduling staff
* Hospital administrators
* Doctors
* Patients (limited access to their own appointments)
* Data analysts reviewing no-show patterns

## How to use
Run preprocess
run load data
run createdb
run dataload_1
run app

## Data Source

The primary dataset used for this project comes from:
[Kaggle No-Show Medical Appointments Dataset](https://www.kaggle.com/datasets/joniarroba/noshowappointments/data)

---
