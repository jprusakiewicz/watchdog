import os
from typing import List

from pydantic import BaseSettings

from app.logger import setup_custom_logger

logger = setup_custom_logger('app', 10)


def read_servers_paths(file_path: str) -> List[str]:
    servers_paths = []
    try:
        with open(file_path, 'rt') as f:
            servers_paths = f.read().split('\n')
        logger.debug(f"servers_paths read successful: {servers_paths}")
    except (FileNotFoundError, TypeError):
        logger.critical(f"File not found! {file_path}")
    return servers_paths


class Settings(BaseSettings):
    LOG_LEVEL = 10
    paths = read_servers_paths(os.getenv('SERVERS_PATH'))


settings = Settings()
