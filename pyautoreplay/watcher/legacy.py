import time
from enum import Enum
from pathlib import Path
import pyautogui
from tqdm import tqdm
from loguru import logger

from pyautoreplay.replay import Replay
from pyautoreplay.window_manager.debian import UbuntuWindowManager
from pyautoreplay.window_manager.windows import WindowsWindowManager


class Action(str, Enum):
    SINGLE_PLAYER = 's'
    EXPANSION = 'e'
    OK = 'o'
    REPLAY = 'r'
    DOWN = 'down'
    SPEEDUP = 'u'
    SWITCH_PLAYER = 'f5'
    EXIT = 'x'


class System(str, Enum):
    UBUNTU = 'ubuntu'
    WINDOWS = 'windows'


class ReplayWatcher:

    def __init__(self, system: System = System.UBUNTU):
        if system == System.WINDOWS:
            self._window_mgr = WindowsWindowManager()
        elif system == System.UBUNTU:
            self._window_mgr = UbuntuWindowManager()
        else:
            raise ValueError('No such window manager')

    def watch(self, replay: Replay):
        self.init_replay()
        for _ in tqdm(range(replay.duration), desc=f'Watching replay for {replay.duration} seconds'):
            time.sleep(1)
        self.exit_replay()

    def _do_action(self, key: str):
        self._window_mgr.find_window("Brood War")
        self._press_key(key)

    @staticmethod
    def _press_key(key: str, delay: float = 1.0):
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)
        time.sleep(delay)

    def init_games_screen(self):
        time.sleep(5)
        self._do_action(Action.SINGLE_PLAYER)
        self._do_action(Action.EXPANSION)
        self._do_action(Action.OK)

    def init_replay(self):
        time.sleep(3)
        self._do_action(Action.REPLAY)
        self._do_action(Action.DOWN)
        self._do_action(Action.DOWN)
        self._do_action(Action.OK)
        self._do_action(Action.DOWN)
        self._do_action(Action.OK)
        self._do_action(Action.SPEEDUP)
        self._do_action(Action.SPEEDUP)
        self._do_action(Action.SWITCH_PLAYER)
        self._do_action(Action.SWITCH_PLAYER)

    def exit_replay(self):
        self._do_action(Action.EXIT)
        time.sleep(3)
        self._do_action(Action.OK)
