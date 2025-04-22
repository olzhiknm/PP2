CREATE TABLE phonebook (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(15)
);

CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, last_name VARCHAR, phone_number VARCHAR) AS
$$
BEGIN
    RETURN QUERY
    SELECT id, first_name, last_name, phone_number
    FROM phonebook
    WHERE first_name ILIKE '%' || pattern || '%'
       OR last_name ILIKE '%' || pattern || '%'
       OR phone_number ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_or_update_user(first_name VARCHAR, last_name VARCHAR, phone_number VARCHAR)
AS
$$
BEGIN
    IF EXISTS (
        SELECT 1 FROM phonebook
        WHERE phonebook.first_name = first_name AND phonebook.last_name = last_name
    ) THEN
        UPDATE phonebook
        SET phone_number = phone_number
        WHERE phonebook.first_name = first_name AND phonebook.last_name = last_name;
    ELSE
        INSERT INTO phonebook (first_name, last_name, phone_number)
        VALUES (first_name, last_name, phone_number);
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_multiple_users(user_list TEXT[])
AS
$$
DECLARE
    user_record TEXT;
    first_name VARCHAR;
    last_name VARCHAR;
    phone_number VARCHAR;
BEGIN
    FOREACH user_record IN ARRAY user_list LOOP
        first_name := split_part(user_record, ',', 1);
        last_name := split_part(user_record, ',', 2);
        phone_number := split_part(user_record, ',', 3);

        IF phone_number ~ '^\d{10}$' THEN
            CALL insert_or_update_user(first_name, last_name, phone_number);
        ELSE
            RAISE NOTICE 'Invalid phone number: %', phone_number;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Переименовали параметр 'limit' на 'p_limit', и 'offset' на 'p_offset'
CREATE OR REPLACE FUNCTION get_phonebook_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, first_name VARCHAR, last_name VARCHAR, phone_number VARCHAR) AS
$$
BEGIN
    RETURN QUERY
    SELECT id, first_name, last_name, phone_number
    FROM phonebook
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_user_by_username_or_phone(username_or_phone VARCHAR)
AS
$$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = username_or_phone OR phone_number = username_or_phone;
END;
$$ LANGUAGE plpgsql;
