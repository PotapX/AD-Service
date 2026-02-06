from configs.logging_config import setup_logging
import yaml
from dataclasses import dataclass
from typing import List, Optional
from configs.crypt import decrypt_file
import logging
from configs.env import get_env_variable
from api.errors import APIError

setup_logging()

logger = logging.getLogger(__name__)

LOG_DIR = 'logs'


@dataclass
class ServerConfig:
    """Конфигурация сервера"""
    name: str
    host: str
    port: int
    item_id: str
    enable_passwork: bool
    login: str
    password: str

@dataclass
class GeneralConfig:
    """Общие настройки сервиса"""
    api_key: str
  
@dataclass
class PassworkClientConfig:
    """Конфигурация Passwork клиента"""
    access_token: str
    refresh_token: str
    master_key: str
    host: str  

class Config:
    """Класс для чтения и работы с конфигурацией из YAML файла"""
    
    def __init__(self, config_path: str = "conf.yml"):
        """Инициализация конфигурации"""
        self.config_path = config_path
        self.passwork_client: Optional[PassworkClientConfig] = None
        self.general: Optional[GeneralConfig] = None
        self.servers: List[ServerConfig] = []
        self._load_config()
    
    def _load_config(self) -> None:
        """Загрузка конфигурации из YAML файла"""
        logger.info("Начало загрузки конфигурационного файла")
        try:
            
            key = get_env_variable()

            config_text = decrypt_file(file_path=self.config_path, password=key)

            config_data = yaml.safe_load(config_text)
 
            # Загрузка конфигурации PassworkClient
            passwork_data = config_data.get('PassworkClient', {})
            self.passwork_client = PassworkClientConfig(
                                        access_token=passwork_data.get('ACCESS_TOKEN', ''),
                                        refresh_token=passwork_data.get('REFRESH_TOKEN', ''),
                                        master_key=passwork_data.get('MASTER_KEY', ''),
                                        host=passwork_data.get('HOST', '')
                                        )
            
            general_data = config_data.get('General', {})
            self.general = GeneralConfig(
                                api_key=general_data.get('ADIS_ACCESS_KEY')
                                ) 

            # Загрузка списка серверов
            servers_data = config_data.get('servers', [])
            for server in servers_data:
                
                server_data = ServerConfig(
                    name=server.get('name', ''),
                    host=server.get('host', ''),
                    port=server.get('port', 389),
                    item_id=server.get('item_id', ''),
                    enable_passwork=server.get('enable_passwork', ''),
                    login=server.get('login', ''),
                    password=server.get('password', '')
                )
                if server_data.enable_passwork == True:
                    # TODO добавить обработку получения уч. данных с passwork
                    pass
                self.servers.append(server_data)
                logger.info(f"Параметры домена {server_data.name}")
            logger.info("Конфигурационный файл загружен")
        except FileNotFoundError:
            logger.error(f"Конфигурационный файл не найден: {self.config_path}")
            raise FileNotFoundError(f"Конфигурационный файл не найден: {self.config_path}")
        except yaml.YAMLError as e:
            logger.error(f"Ошибка парсинга YAML: {e}", exc_info=True)
            raise ValueError(f"Ошибка парсинга YAML: {e}")
        except Exception as e:
            logger.error(f"Ошибка загрузки конфигурации: {e}", exc_info=True)
            raise ValueError(f"Ошибка загрузки конфигурации: {e}")
    
    def get_api_key_header(self) -> str:
        return self.general.api_key         
    
    def get_server_by_name(self, name: str) -> Optional[ServerConfig]:
        """Получить конфигурацию сервера по имени"""
        for server in self.servers:
            if server.name == name:
                return server
        return None
    
    def get_server_by_host(self, host: str) -> Optional[ServerConfig]:
        """Получить конфигурацию сервера по хосту"""
        for server in self.servers:
            if server.host == host:
                return server
        raise APIError(message=f'Не найдены учетные данные домена по адресу {host}',status_code=500)
    
Settings = Config(config_path="conf.yml.enc")
