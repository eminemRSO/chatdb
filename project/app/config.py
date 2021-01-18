from os import getenv
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# openssl rand -hex 32
SECRET_KEY = getenv("SECRET_KEY", "90233f04cbaf3032176aedf04498e9f1c71fdf2be33650f74a639602487e2740")
ALGORITHM = getenv("ALGORTIHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
TOKEN_URL = getenv("TOKEN_URL", "token")

DB_PASSWORD = getenv("DB_PASSWORD", "admin-password")
DB_USER = getenv("DB_USER", "admin-user")
DB_AUTH_SOURCE = getenv("DB_AUTH_SOURCE", "admin")
AUTH_MECHANISM = getenv("AUTH_MECHANISM", "SCRAM-SHA-1")
DB_URL = getenv("DB_URL", "localhost")
