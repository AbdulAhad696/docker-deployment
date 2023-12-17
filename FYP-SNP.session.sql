-- CREATE TABLE "lookup" (
--   "id" serial PRIMARY KEY,
--   "Type" text,
--   "Value" text
-- );

-- CREATE TABLE "Users" (
--   "id" serial PRIMARY KEY ,
--   "username" varchar(30) NOT NULL,
--   "email" varchar(50) NOT NULL,
--   "password" varchar(30) NOT NULL,
--   "usertype" smallint NOT NULL REFERENCES "lookup" ("id"),
--   "contact" varchar(11)
-- );

-- CREATE TABLE "Ward" (
--   "id" serial PRIMARY KEY,
--   "Name" varchar
-- );
-- CREATE TABLE "Patient" (
--   "id" serial PRIMARY KEY,
--   "UserId" integer REFERENCES "Users" ("id"),
--   "Fname" varchar(15),
--   "Lname" varchar(15),
--   "Age" smallint,
--   "Gender" smallint REFERENCES "lookup" ("id"),
--   "BloodGroup" char(2),
--   "Weight" smallint,
--   "Height" varchar(5),
--   "DoB" date,
--   "BMI" real,
--   "AdmitSysBP" smallint,
--   "AdmitDiBP" smallint,
--   "AdmitBPM" smallint,
--   "AdmitTemp" smallint,
--   "AdmitO2" smallint,
--   "Ward" smallint REFERENCES "Ward" ("id"),
--   "NursingDiagnosis" text,
--   "MedicalDiagnosis" text
-- );
-- CREATE TABLE "Doctor" (
--   "id" serial PRIMARY KEY,
--   "UserId" integer REFERENCES "Users" ("id"),
--   "Domain" varchar(20),
--   "Experience" smallint,
--   "Bio" varchar(50),
--   "Gender" smallint REFERENCES "lookup" ("id")
-- );
-- CREATE TABLE "Medication" (
--   "id" serial PRIMARY KEY,
--   "MedName" varchar,
--   "Dosage" varchar,
--   "PrescribedTo" integer REFERENCES "Patient" ("id"),
--   "PrescribedBy" integer REFERENCES "Doctor" ("id"),
--   "Current" boolean
-- );

-- CREATE TABLE "Nurse" (
--   "id" serial PRIMARY KEY,
--   "UserId" integer REFERENCES "Users" ("id"),
--   "Ward" smallint REFERENCES "Ward" ("id"),
--   "Type" smallint,
--   "Experience" smallint,
--   "Bio" varchar(50),
--   "Gender" smallint REFERENCES "lookup" ("id")
-- );

-- CREATE TABLE "MedicationSchedule" (
--   "MedId" smallint REFERENCES "Medication" ("id"), 
--   "AdministeredBy" integer REFERENCES "Nurse" ("id"),
--   "DateAdministered" date,
--   "TimeAdministered" time
-- );

-- CREATE TABLE "Documents" (
--   "id" serial PRIMARY KEY,
--   "PatientId" integer REFERENCES "Patient" ("id"),
--   "Name" varchar,
--   "Date" date,
--   "Link" varchar
-- );

-- CREATE TABLE "CareVitals" (
--   "PatientId" integer REFERENCES "Patient" ("id"),
--   "Time" time,
--   "Date" date,
--   "SystolicBP" smallint,
--   "DistolicBP" smallint,
--   "HeartRate" smallint,
--   "Temperature" real,
--   "SpO2" smallint,
--   "RespirationRate" smallint
-- );

-- ALTER TABLE "CareVitals" ADD FOREIGN KEY ("PatientId") ;

-- ALTER TABLE "Documents" ADD FOREIGN KEY ("PatientId") ;

-- ALTER TABLE "Users" ADD FOREIGN KEY ("usertype") ;

-- ALTER TABLE "Patient" ADD FOREIGN KEY ("Gender") ;

-- ALTER TABLE "Nurse" ADD FOREIGN KEY ("Gender") ;

-- ALTER TABLE "Doctor" ADD FOREIGN KEY ("Gender") ;

-- ALTER TABLE "MedicationSchedule" ADD FOREIGN KEY ("MedId") ;

-- ALTER TABLE "Nurse" ADD FOREIGN KEY ("Ward") ;

-- ALTER TABLE "Patient" ADD FOREIGN KEY ("Ward") ;

-- ALTER TABLE "MedicationSchedule" ADD FOREIGN KEY ("AdministeredBy") ;

-- ALTER TABLE "Medication" ADD FOREIGN KEY ("PrescribedBy") ;

-- ALTER TABLE "Medication" ADD FOREIGN KEY ("PrescribedTo") 

-- ALTER TABLE "Users" ADD FOREIGN KEY ("id") ;

-- ALTER TABLE "Users" ADD FOREIGN KEY ("id") ;

-- ALTER TABLE "Users" ADD FOREIGN KEY ("id") ;                                             

SELECT * FROM "API_Handler_ward"