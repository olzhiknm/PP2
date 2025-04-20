CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) UNIQUE,
    phone VARCHAR(20)
);

CREATE OR REPLACE FUNCTION search_pattern(patt TEXT)
RETURNS TABLE(id INT, first_name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    WHERE first_name ILIKE '%' || patt || '%'
       OR phone ILIKE '%' || patt || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook (first_name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

CREATE TEMP TABLE IF NOT EXISTS temp_users (
    name TEXT,
    phone TEXT
);

CREATE OR REPLACE PROCEDURE insert_many_users()
LANGUAGE plpgsql
AS $$
DECLARE
    u RECORD;
    invalid_data TEXT := '';
BEGIN
    FOR u IN SELECT * FROM temp_users LOOP
        IF u.phone ~ '^\d{10,15}$' THEN
            CALL insert_or_update_user(u.name, u.phone);
        ELSE
            invalid_data := invalid_data || u.name || ' (' || u.phone || '), ';
        END IF;
    END LOOP;
    RAISE NOTICE 'Некорректные данные: %', invalid_data;
END;
$$;

CREATE OR REPLACE FUNCTION paginate_users(lim INT, off INT)
RETURNS TABLE(id INT, first_name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook ORDER BY id LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook WHERE first_name = p_value OR phone = p_value;
END;
$$;
