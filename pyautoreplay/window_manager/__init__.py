from abc import abstractmethod


class WindowManager:

    @abstractmethod
    def find_window(self, window_name: str, *args, **kwargs):
        """find a window by"""
        pass
