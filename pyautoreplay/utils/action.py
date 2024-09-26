import pyautogui
import time
from enum import Enum


class System(str, Enum):
    UBUNTU = 'ubuntu'
    WINDOWS = 'windows'


class Action:

    def __init__(self, window: str, system: System = System.UBUNTU):
        self.window = window
        if system == System.WINDOWS:
            from pyautoreplay.utils.window_manager.windows import WindowsWindowManager
            self.window_manager = WindowsWindowManager()
        elif system == System.UBUNTU:
            from pyautoreplay.utils.window_manager.debian import UbuntuWmctrlWindowManager
            self.window_manager = UbuntuWmctrlWindowManager()
        else:
            raise ValueError('No such window manager')

    def do_action(self, key: str, delay: float = 0.2):
        self.window_manager.find_window(self.window)
        time.sleep(delay)
        self._press_key(key)
        return self

    @staticmethod
    def _press_key(key: str, delay: float = 1.0):
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)
        time.sleep(delay)


