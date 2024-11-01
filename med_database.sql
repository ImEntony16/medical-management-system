CREATE DATABASE IF NOT EXISTS MEDICAL_MANAGEMENT;
USE MEDICAL_MANAGEMENT;

-- Dropping tables if they already exist to prevent conflicts
DROP TABLE IF EXISTS MEDICAL_RECORDS;
DROP TABLE IF EXISTS APPOINTMENTS;
DROP TABLE IF EXISTS PATIENTS;
DROP TABLE IF EXISTS DOCTORS;

-- Table for Doctors
CREATE TABLE DOCTORS (
    DOCTORID INT AUTO_INCREMENT PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL,
    SPECIALIZATION VARCHAR(100),
    CONTACTEMAIL VARCHAR(100),
    CONTACTPHONE VARCHAR(15),
    CREATEDAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Patients
CREATE TABLE PATIENTS (
    PATIENTID INT AUTO_INCREMENT PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL UNIQUE,
    ADDRESS VARCHAR(255),
    DOB DATE,
    GENDER VARCHAR(10),
    CONTACTPHONE VARCHAR(15),
    CREATEDAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Appointments
CREATE TABLE APPOINTMENTS (
    APPOINTMENTID INT AUTO_INCREMENT PRIMARY KEY,
    PATIENTID INT,
    DOCTORID INT,
    APPOINTMENTDATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    STATUS VARCHAR(50) NOT NULL,
    NOTES TEXT,
    FOREIGN KEY (PATIENTID) REFERENCES PATIENTS(PATIENTID) ON DELETE SET NULL,
    FOREIGN KEY (DOCTORID) REFERENCES DOCTORS(DOCTORID) ON DELETE SET NULL
);

-- Table for Medical Records
CREATE TABLE MEDICAL_RECORDS (
    RECORDID INT AUTO_INCREMENT PRIMARY KEY,
    PATIENTID INT,
    DOCTORID INT,
    RECORDDATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    DIAGNOSIS TEXT,
    TREATMENT TEXT,
    PRESCRIPTIONS TEXT,
    NOTES TEXT,
    FOREIGN KEY (PATIENTID) REFERENCES PATIENTS(PATIENTID) ON DELETE SET NULL,
    FOREIGN KEY (DOCTORID) REFERENCES DOCTORS(DOCTORID) ON DELETE SET NULL
);

-- Sample Data Insertion

-- Inserting doctors
INSERT INTO DOCTORS (NAME, SPECIALIZATION, CONTACTEMAIL, CONTACTPHONE) VALUES 
('Dr. Emily White', 'Cardiology', 'emily.white@hospital.com', '+1234567890'),
('Dr. James Green', 'Neurology', 'james.green@hospital.com', '+2345678901'),
('Dr. Sarah Black', 'Orthopedics', 'sarah.black@hospital.com', '+3456789012'),
('Dr. Michael Brown', 'Pediatrics', 'michael.brown@hospital.com', '+4567890123'),
('Dr. Jessica Gray', 'Dermatology', 'jessica.gray@hospital.com', '+5678901234');

-- Inserting patients
INSERT INTO PATIENTS (NAME, EMAIL, ADDRESS, DOB, GENDER, CONTACTPHONE) VALUES 
('John Doe', 'john.doe@example.com', '123 Elm St, Springfield', '1985-07-15', 'Male', '+1111111111'),
('Jane Smith', 'jane.smith@example.com', '456 Oak St, Springfield', '1990-08-20', 'Female', '+2222222222'),
('Alice Johnson', 'alice.johnson@example.com', '789 Pine St, Springfield', '1978-09-25', 'Female', '+3333333333'),
('Robert Brown', 'robert.brown@example.com', '321 Maple St, Springfield', '1982-10-30', 'Male', '+4444444444'),
('Laura Green', 'laura.green@example.com', '654 Birch St, Springfield', '1995-11-05', 'Female', '+5555555555');

-- Inserting appointments
INSERT INTO APPOINTMENTS (PATIENTID, DOCTORID, STATUS, NOTES) VALUES 
(1, 1, 'Scheduled', 'Routine check-up'),
(2, 2, 'Completed', 'Follow-up for headaches'),
(3, 3, 'Scheduled', 'Knee pain consultation'),
(4, 4, 'Cancelled', 'Scheduling conflict'),
(5, 5, 'Scheduled', 'Skin rash evaluation');

-- Inserting medical records
INSERT INTO MEDICAL_RECORDS (PATIENTID, DOCTORID, DIAGNOSIS, TREATMENT, PRESCRIPTIONS, NOTES) VALUES 
(1, 1, 'Hypertension', 'Lifestyle changes, medication', 'Lisinopril', 'Patient advised to monitor blood pressure daily'),
(2, 2, 'Migraine', 'Pain management, lifestyle adjustments', 'Ibuprofen', 'Follow-up in two weeks'),
(3, 3, 'Osteoarthritis', 'Physical therapy, medication', 'Naproxen', 'Patient referred to physical therapist'),
(4, 4, 'Flu', 'Rest, hydration', 'Acetaminophen', 'Patient advised to rest and avoid physical activity'),
(5, 5, 'Eczema', 'Topical steroids', 'Hydrocortisone', 'Patient advised on skin care routines');

-- Display all tables and sample data
SHOW TABLES;
SELECT * FROM DOCTORS;
SELECT * FROM PATIENTS;
SELECT * FROM APPOINTMENTS;
SELECT * FROM MEDICAL_RECORDS;
