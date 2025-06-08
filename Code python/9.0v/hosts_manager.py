# hosts_manager.py
# Версия 9.0: Стабильная версия с логированием и валидацией.

import os
import platform
import shutil
import re
from datetime import datetime
from logger import log

# --- Константы ---
PROFILES_DIR = "profiles"
BACKUP_DIR = "backups"
MANAGED_BLOCK_MARKER = "HOSTS MANAGER MANAGED BLOCK"
CATEGORY_MARKER_REGEX = re.compile(r"# ----- Category: (.*?) -----")
DISABLED_RULE_MARKER = "# [DISABLED BY HOSTS MANAGER] "
IP_V4_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
IP_V6_REGEX = re.compile(r"^(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}$")

def get_hosts_path():
    if platform.system() == "Windows":
        return os.path.join(os.environ["SystemRoot"], "System32", "drivers", "etc", "hosts")
    else:
        return "/etc/hosts"

HOSTS_PATH = get_hosts_path()

def _ensure_dir_exists(path):
    if not os.path.exists(path): os.makedirs(path)

def get_hosts_content():
    _ensure_dir_exists(os.path.dirname(HOSTS_PATH))
    try:
        with open(HOSTS_PATH, 'r', encoding='utf-8') as f: return f.readlines()
    except FileNotFoundError:
        log("Info: hosts file does not exist, returning empty list.")
        return []
    except Exception as e:
        log(f"ERROR: Failed to read hosts file. Details: {e}")
        return None

def write_hosts_content(content):
    try:
        with open(HOSTS_PATH, 'w', encoding='utf-8') as f: f.writelines(content)
        return True
    except Exception as e:
        log(f"ERROR: Failed to write to hosts file. Details: {e}")
        print(f"Ошибка при записи в файл hosts: {e}"); return False

def create_backup(is_auto=False):
    _ensure_dir_exists(BACKUP_DIR)
    prefix = "auto_" if is_auto else ""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"{prefix}hosts_{timestamp}.bak"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    try:
        if os.path.exists(HOSTS_PATH):
            shutil.copy(HOSTS_PATH, backup_path)
            log(f"Backup created: {backup_filename}")
            return backup_filename
    except Exception as e:
        log(f"ERROR: Backup creation failed: {e}")
        print(f"Ошибка при создании резервной копии: {e}")
    return None

def parse_profiles():
    _ensure_dir_exists(PROFILES_DIR)
    profiles_data = {}
    profile_files = [f for f in os.listdir(PROFILES_DIR) if f.endswith(('.txt', '.conf', '.hosts'))]
    for filename in profile_files:
        filepath = os.path.join(PROFILES_DIR, filename)
        profiles_data[filename] = {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
            pattern = re.compile(r"# START CATEGORY: (.*?)\n(.*?)\n# END CATEGORY:", re.DOTALL)
            matches = pattern.findall(content)
            for category_name, category_content in matches:
                lines = [line.strip() for line in category_content.strip().split('\n')]
                valid_lines = [line for line in lines if line and not line.startswith('#')]
                if valid_lines:
                    profiles_data[filename][category_name.strip()] = valid_lines
        except Exception as e:
            log(f"ERROR: Failed to parse profile {filename}: {e}")
            print(f"Не удалось обработать профиль {filename}: {e}")
    return profiles_data

def get_all_rules(ignore_managed_block=False):
    content = get_hosts_content()
    if content is None: return None
    if not content: return {}
    rules = {}
    in_managed_block = False
    for line in content:
        line_strip = line.strip()
        if f"# START {MANAGED_BLOCK_MARKER}" in line_strip: in_managed_block = True
        if f"# END {MANAGED_BLOCK_MARKER}" in line_strip: in_managed_block = False; continue
        if ignore_managed_block and in_managed_block: continue
        if not line_strip or (line_strip.startswith('#') and not line_strip.startswith(DISABLED_RULE_MARKER)):
            continue
        if line_strip.startswith(DISABLED_RULE_MARKER):
            line_strip = line_strip[len(DISABLED_RULE_MARKER):]
        parts = line_strip.split()
        if len(parts) >= 2:
            ip, domain = parts[0], parts[1]
            rules[domain] = ip
    return rules

def check_for_conflicts(rules_to_apply, existing_rules):
    conflicts = []
    all_new_rules = {}
    for rules_list in rules_to_apply.values():
        for rule in rules_list:
            parts = rule.split()
            if len(parts) >= 2:
                all_new_rules[parts[1]] = parts[0]
    for domain, new_ip in all_new_rules.items():
        if domain in existing_rules and existing_rules[domain] != new_ip:
            conflicts.append({"domain": domain, "old_ip": existing_rules[domain], "new_ip": new_ip})
    return conflicts

def apply_rules(rules_to_apply, domains_to_replace=[]):
    if not create_backup(is_auto=True):
        log("CRITICAL: Automatic backup failed. Aborting modification.")
        return False
    
    log(f"Applying {len(rules_to_apply)} categories with {len(domains_to_replace)} domain replacements.")
    full_content = get_hosts_content()
    if full_content is None: return False
    
    if domains_to_replace:
        modified_content = []
        for line in full_content:
            line_strip = line.strip()
            parts = line_strip.split()
            if len(parts) >= 2 and parts[1] in domains_to_replace and not line_strip.startswith('#'):
                 modified_content.append(f"{DISABLED_RULE_MARKER}{line_strip}\n")
            else:
                 modified_content.append(line)
        full_content = modified_content

    new_content = []
    in_managed_block = False
    for line in full_content:
        if f"# START {MANAGED_BLOCK_MARKER}" in line: in_managed_block = True; continue
        if f"# END {MANAGED_BLOCK_MARKER}" in line: in_managed_block = False; continue
        if not in_managed_block: new_content.append(line)
    
    while new_content and new_content[-1].strip() == "":
        new_content.pop()

    if rules_to_apply:
        new_content.append(f"\n\n# START {MANAGED_BLOCK_MARKER} - Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        for category_name, rules in sorted(rules_to_apply.items()):
            new_content.append(f"\n# ----- Category: {category_name} -----\n")
            for rule in rules:
                new_content.append(f"{rule}\n")
        new_content.append(f"\n# END {MANAGED_BLOCK_MARKER}\n")

    return write_hosts_content(new_content)

def get_applied_rules():
    content = get_hosts_content()
    if content is None: return None
    if not content: return {}
    applied_rules = {}
    in_managed_block = False
    current_category = None
    for line in content:
        line_strip = line.strip()
        if f"# START {MANAGED_BLOCK_MARKER}" in line_strip: in_managed_block = True; continue
        if f"# END {MANAGED_BLOCK_MARKER}" in line_strip: break
        if in_managed_block:
            match = CATEGORY_MARKER_REGEX.match(line_strip)
            if match:
                current_category = match.group(1)
                applied_rules[current_category] = []
            elif current_category and line_strip and not line_strip.startswith('#'):
                applied_rules[current_category].append(line_strip)
    return applied_rules

def validate_hosts_syntax():
    log("Syntax validation started.")
    errors = []
    content = get_hosts_content()
    if content is None:
        return [{"line_num": 0, "line_content": "", "error_type": "File Read Error", "details": "Could not read hosts file."}]

    for i, line in enumerate(content):
        line_num = i + 1
        line_strip = line.strip()

        if not line_strip or line_strip.startswith('#'):
            continue

        parts = line_strip.split()
        if len(parts) < 2:
            errors.append({"line_num": line_num, "line_content": line_strip, "error_type": "format"})
            continue
        
        ip, domain = parts[0], parts[1]
        
        if not IP_V4_REGEX.match(ip) and not IP_V6_REGEX.match(ip):
             errors.append({"line_num": line_num, "line_content": line_strip, "error_type": "invalid_ip"})

    if not errors:
        log("Syntax validation finished. No errors found.")
    else:
        log(f"Syntax validation finished. Found {len(errors)} errors.")
    return errors
