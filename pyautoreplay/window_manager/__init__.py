from abc import abstractmethod


class Window:

    def __init__(self, window):
        self.window = window

    @abstractmethod
    def focus(self):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class WindowManager:

    @abstractmethod
    def find_window(self, window_name: str, *args, **kwargs):
        """find a window by"""
        pass
