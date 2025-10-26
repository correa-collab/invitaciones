-- Crear base de datos de invitaciones
CREATE DATABASE IF NOT EXISTS invitaciones_db;

-- Conectar a la base de datos
\c invitaciones_db;

-- Crear usuario para la aplicación
CREATE USER app_user WITH ENCRYPTED PASSWORD 'app_password123';
GRANT ALL PRIVILEGES ON DATABASE invitaciones_db TO app_user;

-- Mensaje de confirmación
SELECT 'Base de datos inicializada correctamente' as status;