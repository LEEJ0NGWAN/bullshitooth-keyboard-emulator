import keyboard, json, os
from datetime import datetime

HID_USAGE_TABLE_FILE = "hid_usage_table.json"
KEY_HID_MAP_FILE = "keyboard_hid_usage_map.json"

LOG_DIR = 'log'
LOG_FILE = None

MAPPING_SAVE_KEY = 'enter'
MAPPING_SAVE_KEY_HID_USAGE_NAME = 'Enter'

target_hid_usage_id = None
target_hid_usage_name = None

key_hid_mapping_info = {}

def main():

    global target_hid_usage_id, target_hid_usage_name

    keyboard.hook(key_mapper)

    with open(HID_USAGE_TABLE_FILE) as file:

        hid_key_table = json.load(file)

        for hid_usage_id in hid_key_table:
            target_hid_usage_id = hid_usage_id
            target_hid_usage_name = hid_key_table[hid_usage_id]

            clear_screen()
            print(f'This is bluetooth key mapping util from keyboard input.\n')
            print(f'[Target key] {target_hid_usage_name}\n')
            print(f'Press any key you want to map\n (skip: [{MAPPING_SAVE_KEY_HID_USAGE_NAME}], exit: [Ctrl+Z])')

            keyboard.wait(hotkey=MAPPING_SAVE_KEY)

    with open(KEY_HID_MAP_FILE, 'w') as file:
        json.dump(key_hid_mapping_info, file, indent=4, ensure_ascii=False)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def write_log(line: str):

    global LOG_FILE

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    if LOG_FILE is None:
        LOG_FILE = f'{LOG_DIR}/key_hid_mapping_{datetime.now()}.log'

    with open(LOG_FILE, 'a') as file:
        file.write(line)

def key_mapper(event:keyboard.KeyboardEvent):

    current_input_key = event.name
    current_input_key_code = event.scan_code

    if current_input_key == MAPPING_SAVE_KEY \
    and target_hid_usage_name != MAPPING_SAVE_KEY_HID_USAGE_NAME:
        return

    clear_screen()

    print(f'[Target key] {target_hid_usage_name}\n')
    print(f' {current_input_key} (pressed) => {target_hid_usage_name} (bluetooth)\n')
    print(f'Press [{MAPPING_SAVE_KEY_HID_USAGE_NAME}] to save current mapping.')

    key_hid_mapping_info[current_input_key_code] = target_hid_usage_id

    log = f'{current_input_key}(code:{current_input_key_code}) => {target_hid_usage_name}(code: {target_hid_usage_id})\n'
    write_log(log)

if __name__ == '__main__':
    main()
