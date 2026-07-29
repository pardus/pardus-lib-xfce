import os, subprocess
import shutil
from time import sleep

# PATHS
HOME_PATH = os.environ.get("HOME", None)
PLUGIN_RC_FILE_DIRECTORY = f"{HOME_PATH}/.config/xfce4/panel/"
PLUGIN_RC_FILE_PATH = f"{HOME_PATH}/.config/xfce4/panel/datetime-8.rc"
ETC_XDG_DATETIME_PATH = "/etc/xdg/pardus/xfce4/panel/datetime-8.rc"

def defaults_available():
    """Whether the packaged default plugin configuration is present.

    It comes from pardus-xfce-settings, which is not a declared dependency of
    this library, so it can legitimately be missing.
    """
    return os.path.exists(ETC_XDG_DATETIME_PATH)


def _seed_config_file():
    """Copy the packaged defaults into the user's config, if there is anything
    to copy. Missing defaults are not an error here: the plugin settings simply
    start out empty."""
    if os.path.exists(PLUGIN_RC_FILE_PATH) or not defaults_available():
        return

    # Create directories if not exists
    os.makedirs(PLUGIN_RC_FILE_DIRECTORY, exist_ok=True)

    shutil.copyfile(ETC_XDG_DATETIME_PATH, PLUGIN_RC_FILE_PATH)


def _read_config_file():
    try:
        with open(PLUGIN_RC_FILE_PATH, "r") as file:
            return file.read()
    except FileNotFoundError:
        return ""


# Seed and read the config file. Neither step may raise: this module is
# imported at application start-up, so a failure here takes down the whole UI
# before it is shown.
_seed_config_file()
config_file_data = _read_config_file()


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
    global config_file_data

    if not defaults_available():
        raise FileNotFoundError(
            f"Default datetime plugin configuration not found at "
            f"{ETC_XDG_DATETIME_PATH}. Is pardus-xfce-settings installed?"
        )

    # copyfile overwrites, so there is no need to remove the current file
    # first - and removing it first would leave the user with nothing if the
    # copy went on to fail.
    shutil.copyfile(ETC_XDG_DATETIME_PATH, PLUGIN_RC_FILE_PATH)

    # Drop the stale in-memory copy, otherwise the next save_file() would write
    # the pre-restore configuration back out.
    config_file_data = _read_config_file()


def set_panel_clock(key, value):
    subprocess.call(
        [
            "/bin/sh",
            "-c",
            f'xfconf-query -c xfce4-panel -l | grep plugin | grep "{key}" | while read path; do xfconf-query -c xfce4-panel -p $path -s "{value}"; done',
        ]
    )
