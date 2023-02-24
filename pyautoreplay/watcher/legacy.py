import time
from enum import Enum
from pathlib import Path

import pyautogui
from tqdm import tqdm
from loguru import logger

from pyautoreplay.replay.screp.screp import Replay
from pyautoreplay.storage.storage import ReplayStorage


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

    WATCHING = r'Autoreplay'
    WINDOW = r'Brood War'

    def __init__(self, storage: ReplayStorage, system: System = System.UBUNTU):
        print(storage.replays_storage_path)
        print(self.WATCHING)
        # self.watching_path = Path(f'{storage.replays_storage_path}\\{self.WATCHING}')
        self.watching_path = storage.replays_storage_path / self.WATCHING
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
        # self.init_replay()
        # print(f'Watching replay {replay.name} for {replay.duration} seconds')
        for _ in tqdm(range(replay.duration), desc=f'Watching replay {replay.name} for {replay.duration} seconds'):
            time.sleep(1)
        self.exit_replay()

    def _do_action(self, key: str, delay: float = 0.2):
        window = self.window_manager.find_window(self.WINDOW)
        time.sleep(delay)
        self._press_key(key)

    @staticmethod
    def _press_key(key: str, delay: float = 1.0):
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)
        time.sleep(delay)

    def init_games_screen(self):
        self._do_action(Action.SINGLE_PLAYER)
        self._do_action(Action.EXPANSION)
        self._do_action(Action.OK)

    def init_replay(self):
        time.sleep(3)
        self._do_action(Action.REPLAY)
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

    def _move_to_watcing_dir(self, replay: Replay):
        replay.copy(self.watching_path / replay.path.name)

    def _clean_watching_dir(self):
        for replay in self.watching_path.glob('*.rep'):
            replay.unlink()
