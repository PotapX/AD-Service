from typing import Union
from ldap3 import Server, Connection, ALL, SUBTREE, BASE
from ldap3.core.exceptions import LDAPException, LDAPBindError
from configs.config import Settings
import base64

class ADManager:
    '''Класс для управления Active Directory через LDAP'''

    def __init__(self, server: str, user: str, password: str ,base_ou: str):
 
        '''
            Инициализация подключения к Active Directory
        Параметры:
            server (str): Адрес сервера AD (например, 'dc.example.com')
            username (str): Логин служебного пользователя (формат: 'user@domain.com' или 'DOMAIN\\user')
            password (str): Пароль пользователя
            base_ou (str, optional): Базовый OU для операций (например, 'OU=Users,DC=domain,DC=com')
        '''

        self.server_address = server
        self.username = user
        self.password = password
        self.base_ou = base_ou
        self.connection = None

    def connect(self) -> tuple [bool, str]:
    
        '''Установка соединения с сервером AD'''
        
        try:
            # Создаем сервер
            server = Server(self.server_address, get_info=ALL)
            
            # Устанавливаем соединение
            self.connection = Connection(
                server,
                user=self.username,
                password=self.password,
                auto_bind=True
            )
            return True, ''    
        except LDAPBindError as e:
            err = f"Ошибка аутентификации: {e}"
            return False, err
        except LDAPException as e:
            err = f"Ошибка подключения к LDAP: {e}"
            return False, err
        
    def disconnect(self):
        '''Закрытие соединения с AD'''

        if self.connection:
            self.connection.unbind()
            self.connection = None
        
    def read_groups(self) -> tuple[bool, Union[list, str]]:
        '''Чтение групп из указанного OU'''
        
        if not self.connection:
            return False, 'Нет подключения к AD'

        attributes = ['cn', 'description', 'distinguishedName', 'objectGUID', 'sAMAccountName']
            
        search_base = self.base_ou
        
        if not search_base:
           return False, 'Не указан OU для поиска'
        
        # Фильтр для поиска групп
        search_filter = '(objectClass=group)'
        
        try:
            self.connection.search(
                search_base=search_base,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=attributes
            )
            
            groups = []
            
            if not self.connection.entries and self.connection.last_error:
                return False, self.connection.last_error

            for entry in self.connection.entries:
                group_data = {}
                for attr in attributes:
                    if hasattr(entry, attr):
                        value = getattr(entry, attr)
                        # Преобразуем объект атрибута в удобный формат
                        if isinstance(value, list):
                            group_data[attr] = [str(v) for v in value]
                        else:
                            group_data[attr] = str(value)
                groups.append(group_data)
            
            return True, groups
            
        except LDAPException as e:
            err = f"Ошибка при чтении групп: {e}"
            return False, err 

    def read_group_users(self, group_dn: str) -> tuple[bool, Union[list, str]]:
        '''
        Чтение пользователей группы по DN группы  
        Параметры:
            group_dn (str): Distinguished Name группы
        '''

        if not self.connection:
            return False, 'Нет подключения к AD'
        
        attributes = ['sAMAccountName', 
                      'cn', 
                      'mail', 
                      'distinguishedName', 
                      'objectGUID', 
                      'employeeNumber',
                      'userPrincipalName',
                      'userAccountControl'
                      ]
        
        try:
            # Проверяем существование группы по DN
            self.connection.search(
                search_base=group_dn,
                search_filter='(objectClass=group)',
                search_scope=BASE,
                attributes=['objectClass']  # Минимальные атрибуты для проверки
            )
            
            if not self.connection.entries:
                err = f"Группа с DN '{group_dn}' не найдена"
                return False, err
            
            # Получаем всех членов группы 
            search_filter = f'(&(objectClass=user)(memberOf={group_dn}))'
                    
            # Выполняем поиск
            self.connection.search(
                        search_base=self.base_ou,
                        search_filter=search_filter,
                        search_scope='SUBTREE',
                        attributes=attributes
                    )
            # Собираем результаты
            users = []
            for entry in self.connection.entries:
                user_data = {}
                for attr in attributes:
                    if attr in entry:
                        user_data[attr] = entry[attr].value
                    else:
                        user_data[attr] = None
                users.append(user_data)
            
            return True, users
            
        except LDAPException as e:
            err = f"Ошибка при чтении пользователей группы: {e}"
            return False, err

    def create_group(self, group_name: str, description: str = "", 
                    group_scope: str = "GLOBAL", group_type: str = "SECURITY") -> tuple[bool, Union[list, str]]:
        '''
        Создание группы в Active Directory
        Параметры:
            group_name (str): Имя группы
            description (str): Описание группы
            group_scope (str): Область группы (GLOBAL, DOMAIN_LOCAL, UNIVERSAL)
            group_type (str): Тип группы (SECURITY, DISTRIBUTION)
        '''
        if not self.connection:
            return False, 'Нет подключения к AD'
        
        ou = self.base_ou
        
        # Формируем DN новой группы
        group_dn = f"CN={group_name},{ou}"
        
        # Преобразуем параметры в числовые флаги
        scope_flags = {
            "GLOBAL": 2,
            "DOMAIN_LOCAL": 4,
            "UNIVERSAL": 8
        }
        
        type_flags = {
            "SECURITY": -2147483648,  # 0x80000000
            "DISTRIBUTION": 0
        }
        
        group_type_value = scope_flags.get(group_scope, 2) | type_flags.get(group_type, -2147483648)
        
        # Атрибуты для создания группы
        attributes = {
            'objectClass': ['top', 'group'],
            'cn': group_name,
            'sAMAccountName': group_name,
            'groupType': group_type_value,
            'description': description
        }
        
        try:
            # Создаем группу
            result = self.connection.add(group_dn, attributes=attributes)
            
            if result:
                response = {
                    "group_dn":group_dn
                }
                return True, [response] 
            else:
                err = f"Ошибка при создании группы: {self.connection.result}"
                return False, err 
                
        except LDAPException as e:
            err = f"Ошибка при создании группы: {e}"
            return False, err

    def read_user_certificates(self, user_object_id: str) -> tuple[bool, Union[list, str]]:
        '''
        Чтение сертификатов пользователя по objectGUID        
        Параметры:
            user_object_id (str): objectGUID пользователя            
        '''
        if not self.connection:
            return False, 'Нет подключения к AD'
        
        attributes = ['userCertificate']

        try:
            if isinstance(user_object_id, bytes):
                user_filter = f'(objectGUID={user_object_id.hex()})'
            else:
                user_filter = f'(objectGUID={user_object_id})'
            
            self.connection.search(
                search_base=self.base_ou,
                search_filter=user_filter,
                search_scope=SUBTREE,
                attributes=attributes
            )
            
            if not self.connection.entries:
                return False, 'Сертификаты пользователя отсутсвуют'

            user_entry = self.connection.entries[0]
              

            certificates = []

            # Возвращаем сертификаты в base64

            for attr_name in attributes:
                if hasattr(user_entry, attr_name) and user_entry[attr_name]:
                    for i, cert_bin in enumerate(user_entry[attr_name].values):
                        certificates.append({
                            'certificate_data': base64.b64encode(cert_bin).decode('ascii'),
                            })
            
            return True, certificates
            
        except LDAPException as e:
            err = f"Ошибка при чтении сертификатов: {e}"
            return False, err                 

# TODO Написать  методы для работы с AD для вызова из вне
        
def read_groups(server: str, base_ou:str) -> tuple[bool, Union[list, str]]:
        
    server_data = Settings.get_server_by_host(server)

    ADConnect = ADManager(server=server, 
                       user=server_data.login,
                       password=server_data.password,
                       base_ou=base_ou)
    
    ADConnect.connect()

    return ADConnect.read_groups()
    
def read_user_certificates(server: str, base_ou:str, user_object_id: str) -> tuple[bool, Union[list, str]]:
    
    server_data = Settings.get_server_by_host(server)

    ADConnect = ADManager(server=server, 
                       user=server_data.login,
                       password=server_data.password,
                       base_ou=base_ou)
    
    ADConnect.connect()

    return ADConnect.read_user_certificates(user_object_id)

def read_group_users(server: str, base_ou:str, group_dn: str) -> tuple[bool, Union[list, str]]:
    
    server_data = Settings.get_server_by_host(server)

    ADConnect = ADManager(server=server, 
                       user=server_data.login,
                       password=server_data.password,
                       base_ou=base_ou)
    
    ADConnect.connect()

    return ADConnect.read_group_users(group_dn)

def create_group(server: str,
                 base_ou:str, 
                 group_name: str, 
                 description: str = "", 
                 group_scope: str = "GLOBAL", 
                 group_type: str = "SECURITY"
                 ) -> tuple[bool, Union[list, str]]:
    
    server_data = Settings.get_server_by_host(server)

    ADConnect = ADManager(server=server, 
                       user=server_data.login,
                       password=server_data.password,
                       base_ou=base_ou)
    
    ADConnect.connect()

    return ADConnect.create_group(group_name,
                                  description,
                                  group_scope,
                                  group_type)