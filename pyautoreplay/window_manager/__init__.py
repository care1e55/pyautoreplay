from abc import abstractmethod


class WindowManager:

    @abstractmethod
    def find_window(self, class_name, window_name: str):
        """find a window by"""
        pass

    @abstractmethod
    def set_foreground(self):
        """put the window in the foreground"""
        pass
