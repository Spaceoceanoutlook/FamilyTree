import secrets

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Генерация секретного ключа для JWT
secret_key = secrets.token_urlsafe(32)
print()
print(f"JWT_SECRET_KEY={secret_key}")

# Генерация хэша пароля
admin_password = input("Придумайте пароль: ")
hashed_password = pwd_context.hash(admin_password)

print()
print("Добавьте эти значения в .env файл:")
print(f"\nJWT_SECRET_KEY={secret_key}")
print(f"HASHED_ADMIN_PASSWORD='{hashed_password}'")
print()
print("Важно: значение HASHED_ADMIN_PASSWORD заключено в кавычки ''")
print("Это предотвращает ошибки интерпретации символа $ в Docker")
