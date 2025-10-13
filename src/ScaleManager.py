import subprocess

import gi

gi.require_version("Xfconf", "0")
from gi.repository import Xfconf

xsettings = Xfconf.Channel.new("xsettings")
xfce4_panel = Xfconf.Channel.new("xfce4-panel")
xfce4_desktop = Xfconf.Channel.new("xfce4-desktop")

default_dpi = 96


def set_scale(scaling_factor):
    new_dPI = default_dpi * scaling_factor
    xsettings.set_int("/Xft/DPI", int(new_dPI))

    subprocess.call(["xfce4-panel", "-r"])


def set_panel_size(px):
    xfce4_panel.set_uint("/panels/panel-1/size", px)


def set_panel_icon_size(px):
    xfce4_panel.set_uint("/panels/panel-1/icon-size", px)


def set_desktop_icon_size(px):
    xfce4_desktop.set_uint("/desktop-icons/icon-size", px)


def set_pointer_size(px):
    current_theme = xsettings.get_string("/Gtk/CursorThemeName", "Adwaita")
    xsettings.set_int("/Gtk/CursorThemeSize", px)
    xsettings.set_string("/Gtk/CursorThemeName", "Adwaita")
    xsettings.set_string("/Gtk/CursorThemeName", current_theme)


def get_scale():
    dpi = xsettings.get_int("/Xft/DPI", 96)
    return float(dpi / default_dpi)


def get_panel_size():
    return xfce4_panel.get_uint("/panels/panel-1/size", 34)


def get_panel_icon_size():
    return xfce4_panel.get_uint("/panels/panel-1/icon-size", 24)


def get_desktop_icon_size():
    return xfce4_desktop.get_uint("/desktop-icons/icon-size", 42)


def get_pointer_size():
    return xsettings.get_int("/Gtk/CursorThemeSize", 16)
