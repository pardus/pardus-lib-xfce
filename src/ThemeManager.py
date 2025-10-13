import os, pwd

import gi

gi.require_version("Xfconf", "0")
from gi.repository import Xfconf

xsettings = Xfconf.Channel.new("xsettings")
xfwm4 = Xfconf.Channel.new("xfwm4")

USER = pwd.getpwuid(os.getuid()).pw_name

theme_path = ["/usr/share/themes/", f"/home/{USER}/.themes/"]


def get_theme_list():
    themes = []
    window_themes = []

    for path in theme_path:
        try:
            files = os.scandir(path)
            for file in files:
                if file.is_dir():
                    themes.append(file.name)

                    if os.path.isdir(f"{path}/{file.name}/xfwm4"):
                        window_themes.append(file.name)
        except FileNotFoundError as error:
            pass

    themes.sort()
    window_themes.sort()
    return [themes, window_themes]


def set_theme(theme):
    xsettings.set_string("/Net/ThemeName", theme)


def set_window_theme(theme):
    xfwm4.set_string("/general/theme", theme)


def set_icon_theme(theme):
    xsettings.set_string("/Net/IconThemeName", theme)


def get_theme():
    return xsettings.get_string("/Net/ThemeName", "")


def get_window_theme():
    return xfwm4.get_string("/general/theme", "")


def get_icon_theme():
    return xsettings.get_string("/Net/IconThemeName", "")
