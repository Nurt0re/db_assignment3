-- Database Schema for Caregiving Platform
-- Created: November 15, 2025
-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS APPOINTMENT;

DROP TABLE IF EXISTS JOB_APPLICATION;

DROP TABLE IF EXISTS JOB;

DROP TABLE IF EXISTS ADDRESS;

DROP TABLE IF EXISTS MEMBER;

DROP TABLE IF EXISTS CAREGIVER;

DROP TABLE IF EXISTS USER;

-- Create USER table
CREATE TABLE
	"user" (
		user_id SERIAL PRIMARY KEY,
		email VARCHAR(255) NOT NULL UNIQUE,
		given_name VARCHAR(100) NOT NULL,
		surname VARCHAR(100) NOT NULL,
		city VARCHAR(100),
		phone_number VARCHAR(20),
		profile_description TEXT,
		password VARCHAR(255) NOT NULL,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);

-- Create CAREGIVER table
CREATE TABLE
	caregiver (
		caregiver_user_id INT PRIMARY KEY,
		photo VARCHAR(255),
		gender VARCHAR(50) CHECK (
			gender IN ('Male', 'Female', 'Other', 'Prefer not to say')
		),
		caregiving_type VARCHAR(100) NOT NULL,
		hourly_rate DECIMAL(10, 2) NOT NULL,
		FOREIGN KEY (caregiver_user_id) REFERENCES "user" (user_id) ON DELETE CASCADE
	);

-- Create MEMBER table
CREATE TABLE
	member (
		member_user_id INT PRIMARY KEY,
		house_rules TEXT,
		dependent_description TEXT,
		FOREIGN KEY (member_user_id) REFERENCES "user" (user_id) ON DELETE CASCADE
	);

-- Create ADDRESS table
CREATE TABLE
	address (
		address_id SERIAL PRIMARY KEY,
		member_user_id INT NOT NULL,
		house_number VARCHAR(20) NOT NULL,
		street VARCHAR(255) NOT NULL,
		town VARCHAR(100) NOT NULL,
		FOREIGN KEY (member_user_id) REFERENCES member (member_user_id) ON DELETE CASCADE
	);

-- Create JOB table
CREATE TABLE
	job (
		job_id SERIAL PRIMARY KEY,
		member_user_id INT NOT NULL,
		required_caregiving_type VARCHAR(100) NOT NULL,
		other_requirements TEXT,
		date_posted DATE NOT NULL,
		FOREIGN KEY (member_user_id) REFERENCES member (member_user_id) ON DELETE CASCADE
	);

-- Create JOB_APPLICATION table
CREATE TABLE
	job_application (
		application_id SERIAL PRIMARY KEY,
		caregiver_user_id INT NOT NULL,
		job_id INT NOT NULL,
		date_applied DATE NOT NULL,
		FOREIGN KEY (caregiver_user_id) REFERENCES caregiver (caregiver_user_id) ON DELETE CASCADE,
		FOREIGN KEY (job_id) REFERENCES job (job_id) ON DELETE CASCADE,
		CONSTRAINT unique_application UNIQUE (caregiver_user_id, job_id)
	);

-- Create APPOINTMENT table
CREATE TABLE
	appointment (
		appointment_id SERIAL PRIMARY KEY,
		caregiver_user_id INT NOT NULL,
		member_user_id INT NOT NULL,
		appointment_date DATE NOT NULL,
		appointment_time TIME NOT NULL,
		work_hours DECIMAL(5, 2) NOT NULL,
		status VARCHAR(20) CHECK (
			status IN (
				'Scheduled',
				'Confirmed',
				'Completed',
				'Cancelled'
			)
		) DEFAULT 'Scheduled',
		FOREIGN KEY (caregiver_user_id) REFERENCES caregiver (caregiver_user_id) ON DELETE CASCADE,
		FOREIGN KEY (member_user_id) REFERENCES member (member_user_id) ON DELETE CASCADE
	);

-- Create indexes for better query performance
CREATE INDEX idx_user_email ON "user" (email);

CREATE INDEX idx_user_city ON "user" (city);

CREATE INDEX idx_caregiver_type ON caregiver (caregiving_type);

CREATE INDEX idx_job_posted_date ON job (date_posted);

CREATE INDEX idx_job_caregiving_type ON job (required_caregiving_type);

CREATE INDEX idx_appointment_date ON appointment (appointment_date);

CREATE INDEX idx_appointment_status ON appointment (status);

CREATE INDEX idx_address_member ON address (member_user_id);
