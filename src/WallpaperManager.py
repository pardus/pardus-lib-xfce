#!/usr/bin/env python3

import os
import subprocess
import gi

gi.require_version("Gdk", "3.0")
from gi.repository import Xfconf, Gdk

wallpaper_dir = "/usr/share/backgrounds/"
desktop = Xfconf.Channel.new("xfce4-desktop")


def get_xfconf_screen_monitor_paths():
    # ["/backdrop/screen0/monitorVirtual-1/workspace0"]
    final_paths = []

    display = Gdk.Display.get_default()
    for s in range(display.get_n_screens()):
        screen = display.get_screen(s)

        for m in range(screen.get_n_monitors()):
            m_n = screen.get_monitor_plug_name(m)

            final_paths.append(f"/backdrop/screen{s}/monitor{m_n}/workspace0")

    return final_paths


def get_wallpapers():
    wallpapers = []
    # Add wallpapers to list
    for root, dirs, files in os.walk(wallpaper_dir):
        dirs.clear()
        for file_name in files:
            path = os.path.join(root, file_name)
            wallpapers.append(f"{path}")

    return wallpapers


def set_wallpaper(wallpaper):
    monitor_paths = get_xfconf_screen_monitor_paths()

    # Set wallpaper in all monitors
    for p in monitor_paths:
        last_image_path = f"{p}/last-image"
        desktop.set_string(last_image_path, wallpaper)


def get_resolution():
    output = subprocess.check_output("xrandr | grep '*'", shell=True).decode("utf-8")
    return output.strip().split(" ")[0]
