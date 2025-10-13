import os, subprocess
import shutil
from time import sleep

# PATHS
HOME_PATH = os.environ.get("HOME", None)
PLUGIN_RC_FILE_DIRECTORY = f"{HOME_PATH}/.config/xfce4/panel/"
PLUGIN_RC_FILE_PATH = f"{HOME_PATH}/.config/xfce4/panel/datetime-8.rc"
ETC_XDG_DATETIME_PATH = "/etc/xdg/pardus/xfce4/panel/datetime-8.rc"

# Copy the default config file if not exists:
if not os.path.exists(PLUGIN_RC_FILE_PATH):
    # Create directories if not exists
    os.makedirs(PLUGIN_RC_FILE_DIRECTORY, exist_ok=True)

    shutil.copyfile(ETC_XDG_DATETIME_PATH, PLUGIN_RC_FILE_PATH)

# Read config file
config_file_data = ""
with open(PLUGIN_RC_FILE_PATH, "r") as file:
    config_file_data = file.read()


def get(key):
    global config_file_data

    lines = config_file_data.splitlines()
    for i in range(len(lines)):
        if key in lines[i]:
            return lines[i].split("=")[-1]

    return None


def set(key, value):
    global config_file_data

    lines = config_file_data.splitlines()
    is_key_exists = False
    for i in range(len(lines)):
        if key in lines[i]:
            lines[i] = f"{key}={value}"
            is_key_exists = True
            break

    if not is_key_exists:
        lines.append(f"{key}={value}")

    config_file_data = "\n".join(lines)


def save_file():
    global config_file_data

    subprocess.run("xfce4-panel -q", shell=True)

    sleep(0.5)

    with open(PLUGIN_RC_FILE_PATH, "w") as file:
        file.write(config_file_data)

    subprocess.run("xfce4-panel &", shell=True)


def restore_default_settings():
    os.remove(PLUGIN_RC_FILE_PATH)
    shutil.copyfile(ETC_XDG_DATETIME_PATH, PLUGIN_RC_FILE_PATH)


def set_panel_clock(key, value):
    subprocess.call(
        [
            "/bin/sh",
            "-c",
            f'xfconf-query -c xfce4-panel -l | grep plugin | grep "{key}" | while read path; do xfconf-query -c xfce4-panel -p $path -s "{value}"; done',
        ]
    )
