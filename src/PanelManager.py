import os
import shutil
import subprocess

import gi

gi.require_version("Xfconf", "0")
from gi.repository import Xfconf

xfce4_panel = Xfconf.Channel.new("xfce4-panel")


def find_plugin(name):
    for key, value in xfce4_panel.get_properties("/plugins").items():
        if type(value) is str and name == value:
            return key

    return None


def get_actions_items():
    plugin = find_plugin("actions")
    items = xfce4_panel.get_string_list(f"{plugin}/items")
    items_obj = {
        "lock-screen": False,
        "switch-user": False,
        "separator": False,
        "suspend": False,
        "hibernate": False,
        "shutdown": False,
        "restart": False,
        "logout": True,
        "logout-dialog": False,
        "hybrid-sleep": False,
    }

    for i in items:
        key, value = i[1:], True if i[0] == "+" else False
        items_obj[key] = value

    return items_obj


def set_actions_item(key, value):
    # key = 'restart', 'shutdown'
    # value = '+' or '-'
    plugin = find_plugin("actions")
    items = xfce4_panel.get_string_list(f"{plugin}/items")

    changed = False
    for i in range(len(items)):
        if key == items[i][1:]:
            items[i] = f"{value}{key}"
            changed = True
            break

    if not changed:
        items.append(f"{value}{key}")

    xfce4_panel.set_arrayv(f"{plugin}/items", items)


def restore_default_actions():
    plugin = find_plugin("actions")
    items = [
        "-lock-screen",
        "-switch-user",
        "-separator",
        "-suspend",
        "-hibernate",
        "-separator",
        "-shutdown",
        "-restart",
        "-separator",
        "+logout",
        "-logout-dialog",
        "-hybrid-sleep",
    ]

    xfce4_panel.set_arrayv(f"{plugin}/items", items)


# Startup Icon
def get_startup_icon():
    whisker_plugin = find_plugin("whiskermenu")
    return xfce4_panel.get_string(f"{whisker_plugin}/button-icon")


def set_startup_icon(path):
    whisker_plugin = find_plugin("whiskermenu")
    xfce4_panel.set_string(f"{whisker_plugin}/button-icon", path)


DEFAULT_PANEL_DIR = "/etc/xdg/pardus/xfce4/panel"
DEFAULT_PANEL_XML = (
    "/etc/xdg/pardus/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml"
)


def defaults_available():
    """Whether the packaged default panel configuration is present.

    These files come from pardus-xfce-settings, which is not a declared
    dependency of this library. Restoring without them would delete the user's
    configuration and put nothing back.
    """
    return os.path.isdir(DEFAULT_PANEL_DIR) and os.path.isfile(DEFAULT_PANEL_XML)


def restore_default_settings():
    """Replace the user's panel configuration with the packaged defaults.

    Raises FileNotFoundError if the defaults are missing, before touching
    anything the user owns.
    """
    if not defaults_available():
        raise FileNotFoundError(
            "Default panel configuration not found under /etc/xdg/pardus/xfce4. "
            "Is pardus-xfce-settings installed?"
        )

    panel_dir = os.path.expanduser("~/.config/xfce4/panel")
    xml_path = os.path.expanduser(
        "~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml"
    )

    # The current configuration is about to be removed and cannot be
    # reconstructed, so keep a copy next to it.
    backup_dir = f"{panel_dir}.bak"
    if os.path.isdir(panel_dir):
        shutil.rmtree(backup_dir, ignore_errors=True)
        shutil.copytree(panel_dir, backup_dir, symlinks=True)
    if os.path.isfile(xml_path):
        shutil.copy2(xml_path, f"{xml_path}.bak")

    xfce4_panel.reset_property("/", True)

    # Chained with && so that a failure stops the sequence instead of carrying
    # on to the next step; check=True surfaces it to the caller.
    subprocess.run(
        "xfce4-panel --quit; "
        "pkill xfconfd; "
        f'rm -rf "{panel_dir}"/* "{xml_path}" && '
        f'cp -R "{DEFAULT_PANEL_DIR}"/* "{panel_dir}/" && '
        f'cp "{DEFAULT_PANEL_XML}" "{xml_path}" && '
        "(xfce4-panel &)",
        shell=True,
        check=True,
    )
