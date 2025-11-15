CREATE VIEW job_applications_view AS
SELECT 
    ja.application_id,
    ja.date_applied,
    cu.given_name || ' ' || cu.surname AS applicant_name,
    cu.email AS applicant_email,
    cu.city AS applicant_city,
    cu.phone_number AS applicant_phone,
    c.caregiving_type,
    c.hourly_rate,
    j.job_id,
    j.required_caregiving_type,
    j.other_requirements,
    j.date_posted,
    mu.given_name || ' ' || mu.surname AS job_poster_name,
    mu.email AS job_poster_email
FROM job_application ja
JOIN caregiver c ON ja.caregiver_user_id = c.caregiver_user_id
JOIN "user" cu ON c.caregiver_user_id = cu.user_id
JOIN job j ON ja.job_id = j.job_id
JOIN member m ON j.member_user_id = m.member_user_id
JOIN "user" mu ON m.member_user_id = mu.user_id
ORDER BY ja.date_applied DESC;
