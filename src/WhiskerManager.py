import os

# PATHS
HOME_PATH = os.environ.get("HOME", None)
WHISKER_FILE_PATH = f"{HOME_PATH}/.config/xfce4/panel/whiskermenu-2.rc"

# READ FILE
config_file_data = ""
with open(WHISKER_FILE_PATH, "r") as file:
    config_file_data = file.read()


def set(key, value):
    global config_file_data

    lines = config_file_data.splitlines()
    for i in range(len(lines)):
        if key in lines[i]:
            print(f"{key} found: {lines[i]}")
            lines[i] = f"{key}={value}"

    config_file_data = "\n".join(lines)


def save_file():
    global config_file_data

    with open(WHISKER_FILE_PATH, "w") as file:
        file.write(config_file_data)


# print(config_file_data) before
# set("launcher-show-name", "true")
# print(config_file_data) after
