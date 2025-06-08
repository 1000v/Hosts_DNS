# logger.py
# Модуль для ведения лог-файла.

import os
from datetime import datetime

LOG_FILE = "hosts-manager.log"
LOGS_DIR = "logs"

def log(message):
    """
    Записывает сообщение в лог-файл с временной меткой.
    """
    try:
        # Убедимся, что папка для логов существует
        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)

        log_path = os.path.join(LOGS_DIR, LOG_FILE)

        # Записываем сообщение
        with open(log_path, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] - {message}\n")
    except Exception as e:
        # Выводим ошибку в консоль, если не удалось записать лог
        print(f"\n[Logger Error] Could not write to log file: {e}\n")


def get_log_content():
    """
    Возвращает содержимое лог-файла.
    """
    try:
        log_path = os.path.join(LOGS_DIR, LOG_FILE)
        if not os.path.exists(log_path):
            return None # Файл еще не создан
        with open(log_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception as e:
        print(f"\n[Logger Error] Could not read log file: {e}\n")
        return [] # Возвращаем пустой список в случае ошибки
