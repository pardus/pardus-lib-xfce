import gi

gi.require_version("Xfconf", "0")
from gi.repository import Xfconf

xsettings = Xfconf.Channel.new("xsettings")


def get_system_font():
    return xsettings.get_string("/Gtk/FontName", "")


def get_monospace_font():
    return xsettings.get_string("/Gtk/MonospaceFontName", "")


def set_system_font(font):
    xsettings.set_string("/Gtk/FontName", font)


def set_monospace_font(font):
    xsettings.set_string("/Gtk/MonospaceFontName", font)
