from passwork_client import PassworkClient

# Конфигурация
ACCESS_TOKEN = "FxWvuVqP9cPvAdWq3BMsSwVaEtFltaka49sv+2HjJME="
REFRESH_TOKEN = "2z7wR6gkNYSVBZEV3D/zddX+GW7LYuNN4WYOaZxHgMQ=" # Опционально (требуется для ротации токенов)
MASTER_KEY = "EgOHwWQZcsgp/hFUAXS0PD60IUjxinfUEo8kUomhloumAXsRPtZ/7wTubtT7WXSpbfvKDDlm+yeOt5l5mN++IQ==" # Мастер-ключ (если включено клиентское шифрование)
HOST = "https://passwork.example.org" # Адрес хоста Пассворка

# Авторизация в Пассворке
try:
    passwork = PassworkClient(HOST)
    passwork.set_tokens(ACCESS_TOKEN, REFRESH_TOKEN)
    if bool(MASTER_KEY):
        passwork.set_master_key(MASTER_KEY)
except Exception as e:
    print(f"Ошибка: {e}") 
    exit(1)

# Пример: Создание элемента
try:
    VAULT_ID = "68d3c3b3473b357ee60a66b8"
    
    # Пример пользовательских полей
    custom_fields = [
        {
            "name": "Текстовое поле",
            "value": "Field value",
            "type": "text"
        },
        {
            "name": "Пароль",
            "value": "Secret123!",
            "type": "password"
        },
        {
            "name": "TOTP-код",
            "value": "ABCDEFGHIJKLMNOP",
            "type": "totp"
        }
    ]
    
    # Подготовка данных элемента
    item_data = {
        "vaultId": VAULT_ID,
        "name": "Grafana Access",
        "login": "ldap_view_grafana@passwork.local",
        "password": "P@ssw0rd",
        "url": "https://grafana.passwork.com",
        "description": "Item description",
        "tags": ["grafana", "monitoring"],
        "customs": custom_fields
    }
    
    # Создание элемента
    item_id = passwork.create_item(item_data)
    print(f"Элемент создан с ID: {item_id}")
    
    # Получение созданного элемента
    item = passwork.get_item(item_id)
    print(f"Созданный элемент: {item}")

except Exception as e:
    print(f"Ошибка: {e}") 