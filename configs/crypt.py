import sys
from cryptography.fernet import Fernet
import base64
import hashlib

def _generate_key_from_password(password: str) -> bytes:
    '''Восстанавливаем ключ из пароля'''
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def decrypt_file(file_path: str, password: str) -> str:
    ''' Расшифровка конфигурационного файла'''
    key = _generate_key_from_password(password)
    fernet = Fernet(key)

    with open(file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        print("Ошибка при расшифровке. Проверьте правильность пароля или файла.")
        sys.exit(1)

    return decrypted_data.decode('utf-8')

