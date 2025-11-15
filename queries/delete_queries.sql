DELETE FROM job
WHERE
    member_user_id IN (
        SELECT
            member_user_id
        FROM
            member
        WHERE
            member_user_id IN (
                SELECT
                    user_id
                FROM
                    "user"
                WHERE
                    given_name = 'Amina'
                    AND surname = 'Aminova'
            )
    );

DELETE FROM member
WHERE
    member_user_id IN (
        SELECT
            member_user_id
        FROM
            address
        WHERE
            street = 'Kabanbay Batyr'
    );
