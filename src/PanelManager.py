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


def restore_default_settings():
    xfce4_panel.reset_property("/", True)
    subprocess.run(
        """xfce4-panel --quit;
        pkill xfconfd;
        rm -rf ~/.config/xfce4/panel/* ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml;
        cp -R /etc/xdg/pardus/xfce4/panel/* ~/.config/xfce4/panel/;
        cp /etc/xdg/pardus/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml ~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml;
        (xfce4-panel &)""",
        shell=True,
    )
