go
select * from users;INSERT INTO users (
    id,
    email,
    password_hash,
    first_name,
    last_name,
    is_active,
    is_staff,
    created_at,
    updated_at,
    last_login
  )
VALUES (
    id:integer,
    'email:character varying',
    'password_hash:bytea',
    'first_name:character varying',
    'last_name:character varying',
    is_active:boolean,
    is_staff:boolean,
    'created_at:timestamp without time zone',
    'updated_at:timestamp without time zone',
    'last_login:timestamp without time zone'
  );