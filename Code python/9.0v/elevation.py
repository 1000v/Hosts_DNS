# elevation.py
# Модуль для проверки и запроса прав администратора.

import os
import sys
import ctypes
import shutil

def is_admin():
    """Проверяет, запущен ли скрипт с правами администратора."""
    try:
        if os.name == 'nt':
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except AttributeError:
        return False

def request_admin_privileges():
    """Перезапускает скрипт с правами администратора, если их нет."""
    if is_admin():
        return
        
    if os.name == 'nt':
        # В Windows права запрашиваются через ShellExecuteW
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
    else:
        # В Linux/macOS перезапуск происходит из main.py, который уже проверил наличие sudo.
        # Эта функция вызывается после проверки.
        if shutil.which('sudo'):
            args = ['sudo', sys.executable] + sys.argv
            os.execvp('sudo', args)
        # Если sudo не найдено, main.py обработает это и выведет сообщение.
        sys.exit(0)
