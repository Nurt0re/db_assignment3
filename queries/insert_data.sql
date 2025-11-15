INSERT INTO
	"user" (
		email,
		given_name,
		surname,
		city,
		phone_number,
		profile_description,
		password
	)
VALUES
	(
		'john.doe@email.com',
		'John',
		'Doe',
		'Almaty',
		'+77771234567',
		'Experienced caregiver with 5 years experience',
		'hashed_password_1'
	),
	(
		'jane.smith@email.com',
		'Jane',
		'Smith',
		'Astana',
		'+77779876543',
		'Professional nurse looking for caregiving opportunities',
		'hashed_password_2'
	),
	(
		'arman.armanov@email.com',
		'Arman',
		'Armanov',
		'Almaty',
		'+77773414141',
		'Caring individual seeking elderly care positions',
		'hashed_password_3'
	),
	(
		'sarah.johnson@email.com',
		'Sarah',
		'Johnson',
		'Shymkent',
		'+77771111111',
		'Specialized in child care',
		'hashed_password_4'
	),
	(
		'mike.wilson@email.com',
		'Mike',
		'Wilson',
		'Almaty',
		'+77772222222',
		'Family needing care assistance',
		'hashed_password_5'
	),
	(
		'amina.aminova@email.com',
		'Amina',
		'Aminova',
		'Astana',
		'+77773333333',
		'Looking for reliable caregiver',
		'hashed_password_6'
	),
	(
		'peter.brown@email.com',
		'Peter',
		'Brown',
		'Almaty',
		'+77774444444',
		'Elderly care specialist',
		'hashed_password_7'
	),
	(
		'lisa.davis@email.com',
		'Lisa',
		'Davis',
		'Shymkent',
		'+77775555555',
		'Parent seeking childcare',
		'hashed_password_8'
	),
	(
		'david.lee@email.com',
		'David',
		'Lee',
		'Almaty',
		'+77776666666',
		'Experienced with special needs care',
		'hashed_password_9'
	),
	(
		'emma.white@email.com',
		'Emma',
		'White',
		'Astana',
		'+77777777777',
		'Family on Kabanbay Batyr street',
		'hashed_password_10'
	);

INSERT INTO
	caregiver (
		caregiver_user_id,
		photo,
		gender,
		caregiving_type,
		hourly_rate
	)
VALUES
	(
		1,
		'photos/john_doe.jpg',
		'Male',
		'Elderly Care',
		2500.00
	),
	(
		2,
		'photos/jane_smith.jpg',
		'Female',
		'Medical Care',
		3000.00
	),
	(
		3,
		'photos/arman_armanov.jpg',
		'Male',
		'Elderly Care',
		2200.00
	),
	(
		4,
		'photos/sarah_johnson.jpg',
		'Female',
		'Child Care',
		2800.00
	),
	(
		7,
		'photos/peter_brown.jpg',
		'Male',
		'Elderly Care',
		2600.00
	),
	(
		9,
		'photos/david_lee.jpg',
		'Male',
		'Special Needs Care',
		3500.00
	);

INSERT INTO
	member (
		member_user_id,
		house_rules,
		dependent_description
	)
VALUES
	(
		5,
		'No smoking, no pets',
		'Elderly father, needs daily assistance'
	),
	(
		6,
		'Quiet hours after 9 PM',
		'Two young children, ages 3 and 5'
	),
	(
		8,
		'No smoking',
		'Elderly mother with mobility issues'
	),
	(
		10,
		'No pets, clean environment',
		'Elderly grandmother, needs medication management'
	);

INSERT INTO
	address (member_user_id, house_number, street, town)
VALUES
	(5, '15', 'Abay Avenue', 'Almaty'),
	(6, '42', 'Dostyk Street', 'Astana'),
	(8, '88', 'Al-Farabi Avenue', 'Shymkent'),
	(10, '123', 'Kabanbay Batyr', 'Astana');

INSERT INTO
	job (
		member_user_id,
		required_caregiving_type,
		other_requirements,
		date_posted
	)
VALUES
	(
		5,
		'Elderly Care',
		'Must have experience with medication management',
		'2025-11-01'
	),
	(
		6,
		'Child Care',
		'CPR certified preferred, flexible hours, soft-spoken personality required',
		'2025-11-05'
	),
	(
		8,
		'Elderly Care',
		'Experience with mobility assistance required',
		'2025-11-08'
	),
	(
		10,
		'Elderly Care',
		'Nursing background required, soft-spoken and patient',
		'2025-11-10'
	),
	(
		5,
		'Elderly Care',
		'Weekend availability needed',
		'2025-11-12'
	);

INSERT INTO
	job_application (caregiver_user_id, job_id, date_applied)
VALUES
	(1, 1, '2025-11-02'),
	(2, 1, '2025-11-02'),
	(3, 1, '2025-11-03'),
	(1, 3, '2025-11-09'),
	(4, 2, '2025-11-06'),
	(2, 4, '2025-11-11'),
	(7, 5, '2025-11-13'),
	(9, 3, '2025-11-09');

INSERT INTO
	appointment (
		caregiver_user_id,
		member_user_id,
		appointment_date,
		appointment_time,
		work_hours,
		status
	)
VALUES
	(1, 5, '2025-11-15', '09:00:00', 8.00, 'Confirmed'),
	(
		2,
		10,
		'2025-11-16',
		'10:00:00',
		6.00,
		'Scheduled'
	),
	(4, 6, '2025-11-17', '14:00:00', 4.00, 'Confirmed'),
	(3, 8, '2025-11-18', '08:00:00', 8.00, 'Scheduled'),
	(7, 5, '2025-11-20', '09:00:00', 8.00, 'Scheduled'),
	(1, 8, '2025-11-22', '10:00:00', 6.00, 'Confirmed'),
	(2, 6, '2025-11-23', '13:00:00', 5.00, 'Completed'),
	(
		9,
		10,
		'2025-11-25',
		'09:00:00',
		8.00,
		'Scheduled'
	);
