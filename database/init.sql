-- Inicializar usuario y privilegios para la aplicación
DO
$$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles WHERE rolname = 'app_user'
    ) THEN
        CREATE ROLE app_user LOGIN PASSWORD 'app_password123';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE invitaciones_db TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
ALTER ROLE app_user SET search_path TO public;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT USAGE, SELECT ON SEQUENCES TO app_user;

SELECT 'Base de datos inicializada correctamente' AS status;
