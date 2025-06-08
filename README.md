# Hosts DNS Manager v9.0

<p align="center">
  <img src="https://storage.googleapis.com/gemini-prod/images/425a1768-45a9-4581-9b88-51f6630f9c2d.png" alt="Логотип" width="200"/>
</p>

<p align="center">
  <strong>🇷🇺 Русский</strong> | <a href="#eng-version">🇬🇧 English</a>
</p>

**Hosts DNS Manager** — это мощная кроссплатформенная консольная утилита для управления системным файлом `hosts` на Windows и Linux. Она позволяет легко применять и откатывать сложные наборы правил, блокировать домены и управлять DNS-записями с помощью профилей и категорий.

Приложение создано для удобства и безопасности, имеет интуитивно понятный интерфейс с анимациями, поддерживает несколько языков и автоматически создает резервные копии перед любыми изменениями.

---

### 🔥 Основные возможности

* **Управление через Профили:** Организуйте ваши правила блокировки в текстовые файлы (`profiles/*.txt`) и применяйте их одной командой.
* **Гибкий выбор категорий:** Применяйте как целые профили, так и отдельные категории из разных файлов одновременно.
* **Многоязычный интерфейс:** Поддержка русского и английского языков с возможностью выбора при запуске.
* **Разрешение конфликтов:** Автоматически обнаруживает конфликтующие правила (разные IP для одного домена) и предлагает варианты решения.
* **Автоматическое резервное копирование:** Перед каждым изменением файла `hosts` создается `auto-backup`, чтобы вы всегда могли откатиться.
* **Валидатор синтаксиса:** Встроенный инструмент для проверки файла `hosts` на наличие синтаксических ошибок.
* **Логирование действий:** Все операции записываются в файл `logs/hosts-manager.log` для истории и отладки.
* **Кроссплатформенность:** Работает на Windows и Linux.
* **Современный консольный UI:** Красочный интерфейс с анимациями, прогресс-барами и постраничным выводом (пагинацией).

### 🚀 Установка и запуск

#### Для обычных пользователей (рекомендуется)

1. Перейдите на [страницу Релизов](https://github.com/ВАШ_ЛОГИН/Hosts_DNS/releases) (замените на вашу ссылку).
2. Скачайте последнюю версию `HostsManager.exe` из раздела "Assets".
3. Поместите `.exe` файл в удобную папку.
4. Создайте рядом папку `profiles` и положите в нее ваши файлы с правилами.
5. Запускайте `HostsManager.exe` от имени Администратора.

#### Для разработчиков (из исходного кода)

1. Убедитесь, что у вас установлен Python 3.
2. Установите необходимые библиотеки:
   ```bash
   pip install colorama pyinstaller
   ```

3.  Запустите главный файл с правами администратора:
      * **Windows:** Откройте PowerShell/CMD от имени Администратора и выполните `python main.py`.
      * **Linux:** Выполните `sudo python3 main.py`.

### ⚙️ Как создавать профили

1.  В папке `profiles` создайте любой текстовый файл (например, `block-social.txt`).
2.  Внутри файла сгруппируйте ваши правила по категориям, используя следующий синтаксис:

<!-- end list -->

```
# START CATEGORY: Название Категории 1
127.0.0.1 site1.com
127.0.0.1 site2.com
# END CATEGORY: Название Категории 1

# START CATEGORY: Другая Категория
0.0.0.0 ads.service.com
# END CATEGORY: Другая Категория
```

Программа автоматически найдет все такие файлы и категории в них.

### 🛠️ Сборка в `.exe`

Для сборки собственного исполняемого файла из исходного кода используйте команду:

```bash
pyinstaller --onefile --icon="icon.ico" main.py
```

  * `--onefile`: Упаковать все в один файл.
  * `--icon="icon.ico"`: Установить иконку для приложения.
  * **Важно:** Не используйте флаг `--windowed` или `--noconsole`. Это приложение является консольным и требует терминала для работы.

Готовый файл `main.exe` будет находиться в папке `dist`, которая появится в корне вашего проекта.

### 📄 Лицензия

Этот проект распространяется под лицензией [Apache 2.0 License](https://www.google.com/search?q=LICENSE).

-----


<a name="eng-version"\>\</a\>🇬🇧 English Version

**Hosts DNS Manager** is a powerful, cross-platform console utility for managing the system's `hosts` file on Windows and Linux. It allows you to easily apply and roll back complex rule sets, block domains, and manage DNS records using profiles and categories.

The application is designed for convenience and safety, featuring an intuitive animated interface, multi-language support, and automatic backups before any changes are made.

### 🔥 Key Features

  * **Profile-Based Management:** Organize your blocking rules into text files (`profiles/*.txt`) and apply them with a single command.
  * **Flexible Category Selection:** Apply entire profiles or individual categories from different files simultaneously.
  * **Multi-Language Interface:** Supports Russian and English, with a language selection on startup.
  * **Conflict Resolution:** Automatically detects conflicting rules (different IPs for the same domain) and offers resolution options.
  * **Automatic Backups:** Before every modification of the `hosts` file, an `auto-backup` is created so you can always revert.
  * **Syntax Validator:** A built-in tool to check your `hosts` file for syntax errors.
  * **Action Logging:** All operations are logged to `logs/hosts-manager.log` for history and debugging.
  * **Cross-Platform:** Works on Windows and Linux.
  * **Modern Console UI:** A colorful interface with animations, progress bars, and pagination for easy viewing.

### 🚀 Installation and Usage

#### For End-Users (Recommended)

1.  Go to the [Releases page](https://www.google.com/search?q=https://github.com/YOUR_LOGIN/Hosts_DNS/releases) (replace with your link).
2.  Download the latest `HostsManager.exe` from the "Assets" section.
3.  Place the `.exe` file in a convenient folder.
4.  Create a `profiles` folder next to it and add your rule files.
5.  Run `HostsManager.exe` as an Administrator.

#### For Developers (from source)

1.  Ensure you have Python 3 installed.
2.  Install the required libraries:
    ```bash
    pip install colorama pyinstaller
    ```
3.  Run the main script with administrator privileges:
      * **Windows:** Open PowerShell/CMD as Administrator and run `python main.py`.
      * **Linux:** Run `sudo python3 main.py`.

### ⚙️ How to Create Profiles

1.  In the `profiles` folder, create any text file (e.g., `block-social.txt`).
2.  Inside the file, group your rules by category using the following syntax:

<!-- end list -->

```
# START CATEGORY: Category Name 1
127.0.0.1 site1.com
127.0.0.1 site2.com
# END CATEGORY: Category Name 1

# START CATEGORY: Another Category
0.0.0.0 ads.service.com
# END CATEGORY: Another Category
```

The program will automatically find all such files and their categories.

### 🛠️ Building the `.exe`

To build your own executable from the source code, use this command:

```bash
pyinstaller --onefile --icon="icon.ico" main.py
```

  * `--onefile`: Bundles everything into a single executable.
  * `--icon="icon.ico"`: Sets the application icon.
  * **Important:** Do not use the `--windowed` or `--noconsole` flag. This is a console application and requires a terminal to function.

The final `main.exe` will be located in the `dist` folder, which will appear in your project's root directory.

### 📄 License

This project is licensed under the [Apache 2.0 License](https://www.google.com/search?q=LICENSE).
