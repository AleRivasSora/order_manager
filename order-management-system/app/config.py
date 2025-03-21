from datetime import timedelta

SECRET_KEY = "your_secret_key_here"  # Cambia esto por una clave secreta segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tiempo de expiración del token de acceso
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Tiempo de expiración del token de refresco