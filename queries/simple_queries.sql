SELECT 
    cu.given_name || ' ' || cu.surname AS caregiver_name,
    mu.given_name || ' ' || mu.surname AS member_name,
    a.appointment_date,
    a.status
FROM appointment a
JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
JOIN "user" cu ON c.caregiver_user_id = cu.user_id
JOIN member m ON a.member_user_id = m.member_user_id
JOIN "user" mu ON m.member_user_id = mu.user_id
WHERE a.status IN ('Confirmed', 'Completed');

SELECT 
    job_id,
    required_caregiving_type,
    other_requirements,
    date_posted
FROM job
WHERE other_requirements ILIKE '%soft-spoken%';

SELECT 
    a.appointment_id,
    cu.given_name || ' ' || cu.surname AS caregiver_name,
    a.work_hours,
    a.appointment_date
FROM appointment a
JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
JOIN "user" cu ON c.caregiver_user_id = cu.user_id
WHERE c.caregiving_type = 'Child Care';

SELECT 
    u.given_name || ' ' || u.surname AS member_name,
    u.city,
    m.house_rules,
    m.dependent_description
FROM member m
JOIN "user" u ON m.member_user_id = u.user_id
WHERE u.city = 'Astana' 
    AND m.house_rules ILIKE '%No pets%'
    AND EXISTS (
        SELECT 1 
        FROM job j 
        WHERE j.member_user_id = m.member_user_id 
            AND j.required_caregiving_type = 'Elderly Care'
    );
