-- Truncate all tables in the correct order (respecting foreign key constraints)
-- This removes all data but keeps the table structure

TRUNCATE TABLE appointment CASCADE;
TRUNCATE TABLE job_application CASCADE;
TRUNCATE TABLE job CASCADE;
TRUNCATE TABLE address CASCADE;
TRUNCATE TABLE member CASCADE;
TRUNCATE TABLE caregiver CASCADE;
TRUNCATE TABLE "user" CASCADE;

-- Reset sequences to start from 1
ALTER SEQUENCE IF EXISTS user_user_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS job_job_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS appointment_appointment_id_seq RESTART WITH 1;

SELECT 'All tables truncated successfully!' AS status;
