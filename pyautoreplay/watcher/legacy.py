import time
from enum import Enum
import pyautogui
from tqdm import tqdm
from loguru import logger

from pyautoreplay.replay.screp.screp import Replay
from pyautoreplay.storage.storage import ReplayStorage
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

    WATCHING = 'Autoreplay'

    def __init__(self, storage: ReplayStorage, system: System = System.UBUNTU):
        self.watching_path = storage.replays_storage_path / self.WATCHING
        if system == System.WINDOWS:
            self.window_manager = WindowsWindowManager()
        elif system == System.UBUNTU:
            self.window_manager = UbuntuWindowManager()
        else:
            raise ValueError('No such window manager')

    def watch(self, replay: Replay):
        self.init_replay()
        for _ in tqdm(range(replay.duration), desc=f'Watching replay for {replay.duration} seconds'):
            time.sleep(1)
        self.exit_replay()

    def _do_action(self, key: str):
        window = self.window_manager.find_window("Brood War")
        self.window_manager.focus(window)
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

    def _move_to_watcing_dir(self, replay: Replay):
        replay.copy(self.watching_path / replay.path.name)

    def _clean_watching_dir(self):
        for replay in self.watching_path.glob('*.rep'):
            replay.unlink()
