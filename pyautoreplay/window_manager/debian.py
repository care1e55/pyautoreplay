import time
from abc import abstractmethod


from pyautoreplay.window_manager import WindowManager, Window

import gi

gi.require_version('Wnck', '3.0')
gi.require_version("Gtk", "3.0")
from gi.repository import Wnck, Gtk


class UbuntuWindow(Window):

    def focus(self):
        self.window.activate(int(time.time()))

    @property
    def name(self) -> str:
        return self.window.get_name()


class UbuntuWindowManager(WindowManager):

    def __init__(self):
        pass

    @property
    def focused_window(self):
        self.update()
        screen = Wnck.Screen.get_default()
        screen.force_update()
        return screen.get_active_window()

    @property
    def windows(self):
        screen = Wnck.Screen.get_default()
        screen.force_update()
        windows = [Window(window) for window in screen.get_windows()]
        return windows

    def focus(self, window):
        window.window.activate(time.time())

    def update():
        Gtk.main_iteration()
        Gtk.main_iteration_do(False)

    def find_window(self, name: str, **kwargs):
        for window in self.windows:
            if window.name == name:
                return window
