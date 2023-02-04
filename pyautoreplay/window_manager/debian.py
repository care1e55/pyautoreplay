import time

import gi

from pyautoreplay.window_manager import WindowManager

gi.require_version('Wnck', '3.0')
gi.require_version("Gtk", "3.0")
from gi.repository import Wnck, Gtk


class UbuntuWindowManager(WindowManager):

    def find_window(self, window_name: str, **kwargs):
        Gtk.main_iteration()
        Gtk.main_iteration_do(False)
        screen = Wnck.Screen.get_default()
        screen.force_update()
        windows = screen.get_windows()
        for w in windows:
            if w.get_name() == window_name:
                w.activate(int(time.time()))
