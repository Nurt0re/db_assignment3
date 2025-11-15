UPDATE "user"
SET
    phone_number = '+77773414141'
WHERE
    given_name = 'Arman'
    AND surname = 'Armanov';

UPDATE caregiver
SET
    hourly_rate = CASE
        WHEN hourly_rate < 10 THEN hourly_rate + 0.3
        ELSE hourly_rate * 1.10
    END;
