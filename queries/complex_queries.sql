SELECT 
    j.job_id,
    u.given_name || ' ' || u.surname AS member_name,
    j.required_caregiving_type,
    j.date_posted,
    COUNT(ja.application_id) AS number_of_applicants
FROM job j
JOIN member m ON j.member_user_id = m.member_user_id
JOIN "user" u ON m.member_user_id = u.user_id
LEFT JOIN job_application ja ON j.job_id = ja.job_id
GROUP BY j.job_id, u.given_name, u.surname, j.required_caregiving_type, j.date_posted
ORDER BY number_of_applicants DESC;

SELECT 
    c.caregiver_user_id,
    u.given_name || ' ' || u.surname AS caregiver_name,
    c.caregiving_type,
    SUM(a.work_hours) AS total_hours_worked
FROM caregiver c
JOIN "user" u ON c.caregiver_user_id = u.user_id
JOIN appointment a ON c.caregiver_user_id = a.caregiver_user_id
WHERE a.status IN ('Confirmed', 'Completed')
GROUP BY c.caregiver_user_id, u.given_name, u.surname, c.caregiving_type
ORDER BY total_hours_worked DESC;

SELECT 
    c.caregiver_user_id,
    u.given_name || ' ' || u.surname AS caregiver_name,
    c.hourly_rate,
    COUNT(a.appointment_id) AS accepted_appointments,
    AVG(a.work_hours * c.hourly_rate) AS average_pay_per_appointment,
    SUM(a.work_hours * c.hourly_rate) AS total_earnings
FROM caregiver c
JOIN "user" u ON c.caregiver_user_id = u.user_id
JOIN appointment a ON c.caregiver_user_id = a.caregiver_user_id
WHERE a.status IN ('Confirmed', 'Completed')
GROUP BY c.caregiver_user_id, u.given_name, u.surname, c.hourly_rate
ORDER BY total_earnings DESC;

SELECT 
    c.caregiver_user_id,
    u.given_name || ' ' || u.surname AS caregiver_name,
    c.caregiving_type,
    c.hourly_rate,
    SUM(a.work_hours * c.hourly_rate) AS total_earnings
FROM caregiver c
JOIN "user" u ON c.caregiver_user_id = u.user_id
JOIN appointment a ON c.caregiver_user_id = a.caregiver_user_id
WHERE a.status IN ('Confirmed', 'Completed')
GROUP BY c.caregiver_user_id, u.given_name, u.surname, c.caregiving_type, c.hourly_rate
HAVING SUM(a.work_hours * c.hourly_rate) > (
    SELECT AVG(earnings)
    FROM (
        SELECT SUM(a2.work_hours * c2.hourly_rate) AS earnings
        FROM caregiver c2
        JOIN appointment a2 ON c2.caregiver_user_id = a2.caregiver_user_id
        WHERE a2.status IN ('Confirmed', 'Completed')
        GROUP BY c2.caregiver_user_id
    ) AS avg_earnings
)
ORDER BY total_earnings DESC;
