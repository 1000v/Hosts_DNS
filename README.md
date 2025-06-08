#Hosts DNS Manager v9.0
Hosts DNS Manager — это мощная кроссплатформенная консольная утилита для управления системным файлом hosts на Windows и Linux. Она позволяет легко применять и откатывать сложные наборы правил, блокировать домены и управлять DNS-записями с помощью профилей и категорий.

Приложение создано для удобства и безопасности, имеет интуитивно понятный интерфейс с анимациями, поддерживает несколько языков и автоматически создает резервные копии перед любыми изменениями.

🔥 Основные возможности
Управление через Профили: Организуйте ваши правила блокировки в текстовые файлы (profiles/*.txt) и применяйте их одной командой.

Гибкий выбор категорий: Применяйте как целые профили, так и отдельные категории из разных файлов одновременно.

Многоязычный интерфейс: Поддержка русского и английского языков с возможностью выбора при запуске.

Разрешение конфликтов: Автоматически обнаруживает конфликтующие правила (разные IP для одного домена) и предлагает варианты решения.

Автоматическое резервное копирование: Перед каждым изменением файла hosts создается auto-backup, чтобы вы всегда могли откатиться.

Валидатор синтаксиса: Встроенный инструмент для проверки файла hosts на наличие синтаксических ошибок.

Логирование действий: Все операции записываются в файл logs/hosts-manager.log для истории и отладки.

Кроссплатформенность: Работает на Windows и Linux.

Современный консольный UI: Красочный интерфейс с анимациями, прогресс-барами и постраничным выводом (пагинацией).

🚀 Установка и запуск
Для обычных пользователей (рекомендуется)
Перейдите на страницу Релизов (замените на вашу ссылку).

Скачайте последнюю версию HostsManager.exe из раздела "Assets".

Поместите .exe файл в удобную папку.

Создайте рядом папку profiles и положите в нее ваши файлы с правилами.

Запускайте HostsManager.exe от имени Администратора.

Для разработчиков (из исходного кода)
Убедитесь, что у вас установлен Python 3.

Установите необходимые библиотеки:

pip install colorama pyinstaller

Запустите главный файл с правами администратора:

Windows: Откройте PowerShell/CMD от имени Администратора и выполните python main.py.

Linux: Выполните sudo python3 main.py.

⚙️ Как создавать профили
В папке profiles создайте любой текстовый файл (например, block-social.txt).

Внутри файла сгруппируйте ваши правила по категориям, используя следующий синтаксис:

# START CATEGORY: Название Категории 1
127.0.0.1 site1.com
127.0.0.1 site2.com
# END CATEGORY: Название Категории 1

# START CATEGORY: Другая Категория
0.0.0.0 ads.service.com
# END CATEGORY: Другая Категория

Программа автоматически найдет все такие файлы и категории в них.

🛠️ Сборка в .exe
Для сборки собственного исполняемого файла из исходного кода используйте команду:

pyinstaller --onefile --icon="icon.ico" main.py

--onefile: Упаковать все в один файл.

--icon="icon.ico": Установить иконку для приложения.

Важно: Не используйте флаг --windowed или --noconsole. Это приложение является консольным и требует терминала для работы.

Готовый файл main.exe будет находиться в папке dist, которая появится в корне вашего проекта.

📄 Лицензия
Этот проект распространяется под лицензией Apache 2.0 License.

🇬🇧 English Version
Hosts DNS Manager is a powerful, cross-platform console utility for managing the system's hosts file on Windows and Linux. It allows you to easily apply and roll back complex rule sets, block domains, and manage DNS records using profiles and categories.

The application is designed for convenience and safety, featuring an intuitive animated interface, multi-language support, and automatic backups before any changes are made.

🔥 Key Features
Profile-Based Management: Organize your blocking rules into text files (profiles/*.txt) and apply them with a single command.

Flexible Category Selection: Apply entire profiles or individual categories from different files simultaneously.

Multi-Language Interface: Supports Russian and English, with a language selection on startup.

Conflict Resolution: Automatically detects conflicting rules (different IPs for the same domain) and offers resolution options.

Automatic Backups: Before every modification of the hosts file, an auto-backup is created so you can always revert.

Syntax Validator: A built-in tool to check your hosts file for syntax errors.

Action Logging: All operations are logged to logs/hosts-manager.log for history and debugging.

Cross-Platform: Works on Windows and Linux.

Modern Console UI: A colorful interface with animations, progress bars, and pagination for easy viewing.

🚀 Installation and Usage
For End-Users (Recommended)
Go to the Releases page (replace with your link).

Download the latest HostsManager.exe from the "Assets" section.

Place the .exe file in a convenient folder.

Create a profiles folder next to it and add your rule files.

Run HostsManager.exe as an Administrator.

For Developers (from source)
Ensure you have Python 3 installed.

Install the required libraries:

pip install colorama pyinstaller

Run the main script with administrator privileges:

Windows: Open PowerShell/CMD as Administrator and run python main.py.

Linux: Run sudo python3 main.py.

⚙️ How to Create Profiles
In the profiles folder, create any text file (e.g., block-social.txt).

Inside the file, group your rules by category using the following syntax:

# START CATEGORY: Category Name 1
127.0.0.1 site1.com
127.0.0.1 site2.com
# END CATEGORY: Category Name 1

# START CATEGORY: Another Category
0.0.0.0 ads.service.com
# END CATEGORY: Another Category

The program will automatically find all such files and their categories.

🛠️ Building the .exe
To build your own executable from the source code, use this command:

pyinstaller --onefile --icon="icon.ico" main.py

--onefile: Bundles everything into a single executable.

--icon="icon.ico": Sets the application icon.

Important: Do not use the --windowed or --noconsole flag. This is a console application and requires a terminal to function.

The final main.exe will be located in the dist folder, which will appear in your project's root directory.

📄 License
This project is licensed under the Apache 2.0 License.
