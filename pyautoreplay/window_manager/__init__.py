import time
from abc import abstractmethod


class Window:
    pass


class WnckWindow(Window):

    def __init__(self, window):
        self.window = window

    @property
    def name(self) -> str:
        return self.window.get_name()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class WmctrlWindow(Window):

    def __init__(self, name: str):
        self.name = name


class WindowManager:

    # @abstractmethod
    def focus(self, window):
        pass

    @abstractmethod
    def find_window(self, window_name: str, *args, **kwargs):
        """find a window by"""
        pass
