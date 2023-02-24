import re
from time import sleep

import win32gui

from pyautoreplay.window_manager import WindowManager


class WindowsWindowManager(WindowManager):
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handle = None

    def find_window(self, name: str):
        hwnd = win32gui.FindWindow(None, name)
        self._handle = hwnd
        self.focus()
        return hwnd

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)
        self.set_foreground()

    def focus(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)
