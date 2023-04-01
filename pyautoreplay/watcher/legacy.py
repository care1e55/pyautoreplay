import time
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Optional

import pyautogui
from tqdm import tqdm

from pyautoreplay.replay.screp.screp import Replay
from pyautoreplay.storage.storage import ReplayStorage


class ReplayError(Enum):
    EXPANSION_SCENARIO = 'expansion'
    FATAL = 'fatal'


class Action(str, Enum):
    SINGLE_PLAYER = 's'
    EXPANSION = 'e'
    OK = 'o'
    REPLAY = 'r'
    DOWN = 'down'
    SPEEDUP = 'u'
    SWITCH_PLAYER = 'f5'
    EXIT = 'x'
    CANCEL = 'c'


class System(str, Enum):
    UBUNTU = 'ubuntu'
    WINDOWS = 'windows'


class ReplayWatcher:

    WATCHING = r'Autoreplay'
    WINDOW = r'Brood War'

    def __init__(self, storage: ReplayStorage, watching_path: str, system: System = System.UBUNTU):
        self.watching_path = Path(watching_path)
        self.current_replay = None
        if system == System.WINDOWS:
            from pyautoreplay.window_manager.windows import WindowsWindowManager
            self.window_manager = WindowsWindowManager()
        elif system == System.UBUNTU:
            from pyautoreplay.window_manager.debian import UbuntuWmctrlWindowManager
            self.window_manager = UbuntuWmctrlWindowManager()
        else:
            raise ValueError('No such window manager')

    def watch(self, replay: Replay):
        """Sleep for duration"""
        for _ in tqdm(range(replay.duration), desc=f'Watching replay {replay.name} for {replay.duration} seconds'):
            time.sleep(1)
        self.exit_replay()

    def do_action(self, key: str, delay: float = 0.2):
        self.window_manager.find_window(self.WINDOW)
        time.sleep(delay)
        self._press_key(key)

    @staticmethod
    def _press_key(key: str, delay: float = 1.0):
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)
        time.sleep(delay)

    def init_games_screen(self):
        self.do_action(Action.SINGLE_PLAYER)
        self.do_action(Action.EXPANSION)
        self.do_action(Action.OK)
        return self

    def start_replay(self):
        time.sleep(3)
        self.do_action(Action.REPLAY)
        self.do_action(Action.DOWN)
        self.do_action(Action.OK)
        return self

    def configure_replay(self):
        self.do_action(Action.SPEEDUP)
        self.do_action(Action.SPEEDUP)
        self.do_action(Action.SWITCH_PLAYER)
        self.do_action(Action.SWITCH_PLAYER)
        return self

    def exit_replay(self):
        self.do_action(Action.EXIT)
        time.sleep(3)
        self.do_action(Action.OK)
        return self

    @cached_property
    def error(self) -> Optional[ReplayError]:
        return None

    def move_to_watcing_dir(self, replay: Replay):
        replay.copy(self.watching_path / replay.path.name)

    def clean_watching_dir(self):
        for replay in self.watching_path.glob('*.rep'):
            replay.unlink()
