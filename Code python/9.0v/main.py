# main.py
# Версия 9.0: Исправлена ошибка KeyError и порядок запуска (сначала права, потом язык).

import os
import sys
import time
import shutil
import math
import traceback

# Сначала выполняем проверку и запрос прав администратора
import elevation
elevation.request_admin_privileges()

# Теперь, когда права есть, импортируем все остальное
from hosts_manager import (
    get_hosts_content, create_backup, HOSTS_PATH, parse_profiles,
    apply_rules, get_applied_rules, get_all_rules, check_for_conflicts,
    validate_hosts_syntax
)
from localization import L
from logger import log, get_log_content

# --- Инициализация ---
try:
    import colorama
    colorama.init(autoreset=True)
    C = {k: getattr(colorama.Fore, k, getattr(colorama.Style, k, '')) for k in ["RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "GREY", "BOLD", "END"]}
    C["END"] = colorama.Style.RESET_ALL
except ImportError:
    print(L['en']['colorama_not_found'])
    C = {k: "" for k in ["RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "GREY", "BOLD", "END"]}

# --- Утилиты интерфейса ---
def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')
def print_color(text):
    for key, value in C.items(): text = text.replace(f"{{{key}}}", value)
    print(text, end="")
    print(C['END'], end="")

def show_spinner(duration, message=""):
    spinner = ['/', '-', '\\', '|']; end_time = time.time() + duration; i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{C['YELLOW']}{message} {spinner[i % len(spinner)]}{C['END']}"); sys.stdout.flush()
        time.sleep(0.1); i += 1
    sys.stdout.write('\r' + ' ' * (len(message) + 2) + '\r'); sys.stdout.flush()

def show_progress_bar(duration, message=""):
    steps = 40; print_color(f"{{CYAN}}{message}{{END}}\n")
    for i in range(steps + 1):
        progress = int((i / steps) * 100); bar = '█' * i + '-' * (steps - i)
        sys.stdout.write(f"\r[{C['GREEN']}{bar}{C['END']}] {progress}%"); sys.stdout.flush()
        time.sleep(duration / steps)
    print()

def show_message(message, duration=2, color="GREEN"):
    clear_screen(); print("\n" * 4); print_color(f"{{{color}}}{message.center(80)}{{END}}\n"); time.sleep(duration)

def animated_header(lang_strings):
    clear_screen(); header = " H O S T S   M A N A G E R   v9.0 "; border = "=" * (len(header) + 4)
    print_color(f"\n\n\n{{CYAN}}{border.center(80)}{{END}}\n"); sys.stdout.flush(); time.sleep(0.2)
    centered_header = ""
    for char in header:
        centered_header += char; print(f"{C['BOLD']}{C['CYAN']}  {centered_header.center(len(header))}  {C['END']}".center(96))
        time.sleep(0.02)
        if char != ' ': print("\033[A", end="")
    print_color(f"{{CYAN}}{border.center(80)}{{END}}\n"); time.sleep(0.3)

def display_paginated_list(T, title, content_list, page_size=20):
    if not content_list: return
    page = 0; total_pages = math.ceil(len(content_list) / page_size)
    while True:
        clear_screen(); print_color(f"{{BOLD}}{{CYAN}}{title}{{END}}\n\n")
        start_index = page * page_size
        end_index = start_index + page_size
        for item in content_list[start_index:end_index]:
            print_color(item)
        print("\n" + "-"*60)
        print_color(f"{{YELLOW}}{T['pagination_page'].format(page + 1, total_pages)}{{END}}  |  {T['pagination_controls']}")
        print("-" * 60)
        choice = input("> ").lower()
        if choice == 'n' and page < total_pages - 1: page += 1
        elif choice == 'p' and page > 0: page -= 1
        elif choice == 'q': break

# --- Логика меню ---
def select_language():
    while True:
        clear_screen(); print_color("{CYAN}===================================================={END}\n")
        print_color(f"  {L['ru']['select_language']}\n"); print_color("{CYAN}===================================================={END}\n")
        print_color("\n  [1] Русский\n"); print_color("  [2] English\n"); choice = input("\n> ").strip()
        if choice == '1': return L['ru'], 'ru'
        if choice == '2': return L['en'], 'en'

def print_main_menu(T):
    animated_header(T)
    print_color(f"\n{{GREY}}{T['hosts_file_path'].format(HOSTS_PATH)}{{END}}".center(102))
    print_color(f"\n\n{{BOLD}}{T['main_menu_title']}{{END}}\n")
    print_color(f"  {{GREEN}}[1]{{END}} {T['menu_1_apply']}\n")
    print_color(f"  {{CYAN}}[2]{{END}} {T['menu_2_validate']}\n")
    print_color(f"  {{BLUE}}[3]{{END}} {T['menu_3_view_hosts']}\n")
    print_color(f"  {{MAGENTA}}[4]{{END}} {T['menu_4_delete']}\n")
    print_color(f"  {{YELLOW}}[5]{{END}} {T['menu_5_clear']}\n")
    print_color(f"  {{CYAN}}[6]{{END}} {T['menu_6_backup']}\n")
    print_color(f"  {{GREY}}[7]{{END}} {T['menu_7_view_logs']}\n")
    print_color(f"\n  {{RED}}[0]{{END}} {T['menu_0_exit']}\n")
    print("-" * 60)

def view_hosts(T):
    content = get_hosts_content()
    if content is None: show_message(T['error_reading_hosts'], 3, "RED"); return
    if not content: show_message(T['hosts_file_empty'], 2, "YELLOW"); return
    formatted_content = [f"{{GREY}}{line.strip()}{{END}}\n" if line.strip().startswith('#') else f"{{END}}{line.strip()}{{END}}\n" for line in content]
    display_paginated_list(T, T['view_hosts_title'], formatted_content)

def select_and_apply_rules(T):
    log("User entered 'Apply Profiles' menu.")
    show_spinner(1, T["loading_profiles"])
    profiles_data = parse_profiles()
    if not profiles_data: show_message(T["profiles_not_found"], 3, "RED"); return
    selected_categories = {(p, c): False for p, cats in profiles_data.items() for c in cats}
    while True:
        clear_screen(); print_color(f"{{BOLD}}{{CYAN}}{T['selection_title']}{{END}}\n")
        p_idx, c_idx = 1, 1
        for p_name, cats in profiles_data.items():
            is_p_sel = all(selected_categories.get((p_name, c), False) for c in cats)
            p_check = "{GREEN}[x]{END}" if is_p_sel else "{GREY}[ ]{END}"
            print_color(f"\n{C['BOLD']}{p_check} {p_idx}. {T['profile']}: {p_name}{C['END']}\n")
            for c_name in cats:
                c_check = "{GREEN}[x]{END}" if selected_categories[(p_name, c_name)] else "{GREY}[ ]{END}"
                print_color(f"    {c_check} {c_idx}. {T['category']}: {c_name}\n")
                c_idx += 1
            p_idx += 1
        print_color(f"\n{{YELLOW}}{T['commands_title']}{{END}}\n"); print_color(f"  {T['command_p'].replace('p1', '{BOLD}p1{END}')}\n")
        print_color(f"  {T['command_c'].replace('c3', '{BOLD}c3{END}')}\n"); print_color(f"  {T['command_apply'].replace('apply', '{GREEN}apply{END}')}\n")
        print_color(f"  {T['command_back'].replace('back', '{RED}back{END}')}\n"); choice = input(f"\n{T['your_choice']}").strip().lower()
        if choice == 'back': log("User cancelled profile selection."); break
        if choice == 'apply':
            rules_to_apply = {c: profiles_data[p][c] for (p, c), sel in selected_categories.items() if sel}
            if not rules_to_apply: show_message(T["nothing_to_apply"], 2, "YELLOW"); continue
            show_message(T["auto_backup_creation"], 1.5, "BLUE"); show_spinner(1.5, T['conflict_scan'])
            existing_rules = get_all_rules(ignore_managed_block=True)
            conflicts = check_for_conflicts(rules_to_apply, existing_rules); domains_to_replace = []
            if conflicts:
                clear_screen(); print_color(f"{{BOLD}}{{RED}}{T['conflicts_found_title']}{{END}}\n")
                print(f"{T['conflict_domain']:<40}{T['conflict_old_ip']:<20}{T['conflict_new_ip']:<20}"); print("-" * 80)
                for c in conflicts: print_color(f"{{CYAN}}{c['domain']:<40}{{END}}{C['RED']}{c['old_ip']:<20}{C['END']}{C['GREEN']}{c['new_ip']:<20}{C['END']}\n")
                action = input(f"\n{T['resolve_prompt']}: ").lower().strip()
                if action == 'r': domains_to_replace = [c['domain'] for c in conflicts]
                elif action == 'k':
                    conflicting_domains = {c['domain'] for c in conflicts}
                    for cat, rules in list(rules_to_apply.items()):
                        rules_to_apply[cat] = [r for r in rules if r.split()[1] not in conflicting_domains]
                        if not rules_to_apply[cat]: del rules_to_apply[cat]
                else: show_message(T['action_cancelled'], 2, "YELLOW"); continue
            else: show_message(T['no_conflicts_found'], 2, "GREEN")
            show_progress_bar(2, T["applying_rules"])
            if apply_rules(rules_to_apply, domains_to_replace): show_message(T["rules_applied_success"], 2, "GREEN")
            else: show_message(T["rules_applied_error"], 3, "RED")
            break
        try:
            prefix, num = choice[0], int(choice[1:])
            if prefix == 'p' and 1 <= num <= len(profiles_data):
                p_name, cats = list(profiles_data.items())[num - 1]
                new_state = not all(selected_categories.get((p_name, c), False) for c in cats)
                for c_name in cats: selected_categories[(p_name, c_name)] = new_state
            elif prefix == 'c':
                curr_c_idx = 1
                for p, cats in profiles_data.items():
                    for c in cats:
                        if curr_c_idx == num: selected_categories[(p, c)] = not selected_categories[(p, c)]; raise StopIteration
                        curr_c_idx += 1
        except (ValueError, IndexError): show_message(T["invalid_command"], 1.5, "RED")
        except StopIteration: pass

def delete_applied_category(T):
    clear_screen(); print_color(f"{{BOLD}}{{MAGENTA}}{T['delete_cat_title']}{{END}}\n")
    applied_rules = get_applied_rules()
    if not applied_rules: show_message(T["no_applied_categories"], 3, "YELLOW"); return
    categories = list(applied_rules.keys())
    for i, cat in enumerate(categories): print_color(f"  {{YELLOW}}[{i+1}]{{END}} {cat}\n")
    try:
        choice_str = input(f"\n{T['choose_cat_to_delete']} ").strip()
        if not choice_str: show_message(T['invalid_input'], 2, "RED"); return
        choice = int(choice_str) - 1
        if 0 <= choice < len(categories):
            cat_to_delete = categories[choice]
            if input(T['delete_cat_confirm'].format(cat_to_delete)).lower() == 'y':
                log(f"User initiated deletion of category: {cat_to_delete}"); del applied_rules[cat_to_delete]
                show_message(T["auto_backup_creation"], 1.5, "BLUE"); show_progress_bar(1.5, T['applying_rules'])
                if apply_rules(applied_rules): show_message(T['category_deleted_success'], 2, "GREEN")
                else: show_message(T['rules_applied_error'], 3, "RED")
            else: log("Category deletion cancelled by user."); show_message(T['action_cancelled'], 2, "YELLOW")
        else: show_message(T['invalid_input'], 2, "RED")
    except ValueError: show_message(T['invalid_input'], 2, "RED")

def run_syntax_validator(T):
    clear_screen(); print_color(f"{{BOLD}}{{CYAN}}{T['validator_title']}{{END}}\n")
    show_spinner(2, T['validator_running']); errors = validate_hosts_syntax()
    if not errors: show_message(T['validator_no_errors'], 3, "GREEN"); return
    formatted_errors = []
    for error in errors:
        line_num, line_content = error['line_num'], error['line_content']
        error_type = T[f"validator_error_{error['error_type']}"]
        formatted_errors.append(f"{{YELLOW}}{T['validator_error_line'].format(line_num)}{{END}} {line_content}\n")
        formatted_errors.append(f"  -> {{RED}}{error_type}{{END}}\n\n")
    display_paginated_list(T, T['validator_errors_found'].format(len(errors)), formatted_errors, page_size=5)

def view_logs(T):
    logs = get_log_content()
    if logs is None: show_message(T['logs_not_found'], 2, "YELLOW"); return
    formatted_logs = [f"{{GREY}}{line.strip()}{{END}}\n" for line in logs]
    display_paginated_list(T, T['logs_title'], formatted_logs, page_size=30)

def main():
    try:
        T, lang_code = select_language()
        log(f"Application started. Language selected: {lang_code}")
        while True:
            print_main_menu(T)
            choice = input(f"\n{T['your_choice']}").strip()
            if choice == '1': select_and_apply_rules(T)
            elif choice == '2': run_syntax_validator(T)
            elif choice == '3': view_hosts(T)
            elif choice == '4': delete_applied_category(T)
            elif choice == '5':
                if input(f"{T['clear_confirm']}").lower() == 'y':
                    log("User initiated clearing all managed rules.")
                    show_message(T["auto_backup_creation"], 1.5, "BLUE"); show_progress_bar(1, T["clearing_records"])
                    if apply_rules({}): show_message(T["clear_success"], 2, "GREEN")
                    else: show_message(T["clear_error"], 3, "RED")
                else: log("Clearing all rules cancelled by user.")
            elif choice == '6':
                log("User initiated manual backup.")
                backup = create_backup()
                if backup: show_message(T["backup_created"].format(backup), 3, "BLUE")
                else: show_message(T["backup_error"], 2, "RED")
            elif choice == '7': view_logs(T)
            elif choice == '0':
                log("Application exit."); clear_screen()
                print_color(f"\n\n\n{{BOLD}}{{MAGENTA}}   {T['exiting']}   {{END}}\n\n\n"); break
            else: show_message(T["invalid_input"], 1.5, "RED")
    except Exception as e:
        log("="*20 + " FATAL CRASH " + "="*20)
        log(traceback.format_exc())
        print_color("\n\n{RED}Произошла критическая ошибка! Информация записана в лог-файл.{END}\n")
        print_color("{RED}An unexpected error occurred! Information has been written to the log file.{END}\n")

if __name__ == "__main__":
    main()
