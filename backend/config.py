import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./invitaciones.db")
    
    # JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_super_segura_aqui_cambiar_en_produccion")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # Email
    EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "smtp")  # smtp, aws_ses, sendgrid
    
    # SMTP Settings
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_USER = os.getenv("EMAIL_USER", "")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
    
    # AWS SES Settings
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    
    # SendGrid Settings
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
    
    # File Upload
    UPLOAD_DIR = "uploads"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # CORS
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "https://tu-dominio.com"
    ]
    
    # App Settings
    APP_NAME = "Sistema de Invitaciones"
    VERSION = "1.0.0"
    DESCRIPTION = "API para gestión de invitaciones y confirmaciones de eventos"

settings = Settings()