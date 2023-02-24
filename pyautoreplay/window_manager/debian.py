import subprocess
import time
from abc import abstractmethod
from typing import List

from pyautoreplay.window_manager import WindowManager, Window, WmctrlWindow

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


class UbuntuWnckWindowManager(WindowManager):

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
        # window.window.activate(now)
        self.update()
        window.window.activate_transient(time.time())
        window.window.activate(time.time())
        window.window.make_above()
        window.window.pin()
        window.window.stick()
        window.window.needs_attention()
        window.window.or_transient_needs_attention()
        screen = Wnck.Screen.get_default()
        for ws in screen.get_workspaces():
            if ws.get_name == 'Workspace 2':
                ws.activate()
        screen.force_update()
        window.window.maximize()
        self.update()

    def update(self):
        Gtk.main_iteration()
        Gtk.main_iteration_do(False)

    def find_window(self, name: str, **kwargs):
        for window in self.windows:
            if window.name == name:
                return window


class UbuntuWmctrlWindowManager(WindowManager):

    def __init__(self):
        pass

    def run(self, call_str):
        # logger.info("Call script: {}", call_str) \
        # print("Call script: \n{}".format(call_str))
        p = subprocess.Popen(
            call_str,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        return [line.decode("utf-8") for line in p.stdout.readlines()]

    @property
    def windows(self) -> List:
        call_str = f'wmctrl -l'  # call go script
        windows_raw = self.run(call_str)
        windows = [WmctrlWindow(" ".join(window_line.split()[3:])) for window_line in windows_raw]
        return windows

    def focus(self, window):
        call_str = f'wmctrl -a {window.name}'
        self.run(call_str)

    def find_window(self, name: str, **kwargs):
        for window in self.windows:
            # print(window.name)
            if window.name == name:
                # self.focus(window)
                return window
        raise ValueError(f"Window {name} not found")
