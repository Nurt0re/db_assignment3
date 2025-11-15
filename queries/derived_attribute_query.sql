SELECT 
    c.caregiver_user_id,
    u.given_name || ' ' || u.surname AS caregiver_name,
    c.caregiving_type,
    c.hourly_rate,
    COUNT(a.appointment_id) AS number_of_accepted_appointments,
    SUM(a.work_hours) AS total_hours_worked,
    SUM(a.work_hours * c.hourly_rate) AS total_cost_to_pay
FROM caregiver c
JOIN "user" u ON c.caregiver_user_id = u.user_id
JOIN appointment a ON c.caregiver_user_id = a.caregiver_user_id
WHERE a.status IN ('Confirmed', 'Completed')
GROUP BY c.caregiver_user_id, u.given_name, u.surname, c.caregiving_type, c.hourly_rate
ORDER BY total_cost_to_pay DESC;
