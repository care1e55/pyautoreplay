import time
from enum import Enum
from pathlib import Path
import pyautogui
from tqdm import tqdm
from loguru import logger
from replay import Replay
from window_manager.debian import UbuntuWindowManager


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

    def __init__(self, base_game_path: Path, system: System = System.UBUNTU):
        if system == System.WINDOWS:
            self._window_mgr = WindowsWindowManager()
        elif system == System.UBUNTU:
            self._window_mgr = UbuntuWindowManager()
        else:
            raise ValueError('No such window manager')
        self.watching_path = base_game_path / 'maps' / 'replays' / 'watching'

    def watch(self, replay: Replay):
        watching_replay_path = self.watching_path / replay.replay_path.name
        logger.info(f"Copying {replay.replay_path} to {watching_replay_path}")
        self._clean_watching_dir()
        replay.copy(watching_replay_path)
        self.init_replay()
        for _ in tqdm(
                range(int(round(replay.duration, 0))),
                desc=f'Watching replay for {replay.duration} seconds'
        ):
            time.sleep(1)
        self.exit_replay()
        watching_replay_path.unlink()

    def _clean_watching_dir(self):
        for replay in self.watching_path.glob('*.rep'):
            replay.unlink()

    def _do_action(self, key: str):
        self._window_mgr.find_window_wildcard("Brood War")
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
