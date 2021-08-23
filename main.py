import json
import subprocess
import sys
import time
from enum import Enum
from pathlib import Path
from typing import Iterable, Dict, Any
import pyautogui
from tqdm import tqdm
from loguru import logger
import shutil
import win32gui
import re
from random import shuffle


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)


class Action(str, Enum):
    SINGLE_PLAYER = 's'
    EXPANSION = 'e'
    OK = 'o'
    REPLAY = 'r'
    DOWN = 'down'
    SPEEDUP = 'u'
    SWITCH_PLAYER = 'f5'
    EXIT = 'x'


class Replay:
    FRAMES_PER_SECOND = 23.84

    def __init__(self, replay_path: Path):
        self.replay_path = replay_path
        self.content = self._parse(replay_path)

    # TODO: multiple storage support so not Path but ReplayPath of storage type
    @staticmethod
    def _parse(replay_path: Path) -> Dict[Any, Any]:
        """call go script"""
        p = subprocess.Popen(
            f'screp {replay_path}',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        # TODO: effective
        result_str = ''
        for line in p.stdout.readlines():
            result_str += line.decode("utf-8")
        return json.loads(result_str)

    def remove(self):
        self.replay_path.unlink()

    def copy(self, to_path: Path):
        shutil.copy(self.replay_path, to_path)

    @property
    def duration(self) -> float:
        return self.content['Header']['Frames'] / self.FRAMES_PER_SECOND

    @property
    def winner(self) -> str:
        pass

    @property
    def loser(self) -> str:
        pass


class ReplayStorage:
    # TODO: multiple storage support so not Path but ReplayPath of storage type
    def __init__(self, replays_storage: Path):
        self.replays_storage = replays_storage

    def replays(self) -> Iterable:
        replays = list(self.replays_storage.glob('*.rep'))
        shuffle(replays)
        for replay_path in replays:
            if not replay_path.is_file():
                continue
            logger.info('Watching replay: {}', replay_path)
            try:
                yield Replay(replay_path)
            except:
                continue


class ReplayWatcher:

    def __init__(self, base_game_path: Path):
        self._window_mgr = WindowMgr()
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
        self._window_mgr.set_foreground()
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


if __name__ == '__main__':
    storage_path = Path(sys.argv[1])
    base_game_path = Path(sys.argv[2])
    logger.info('Starting replays from {}', storage_path)
    replays_storage_path = Path(storage_path)
    rs = ReplayStorage(replays_storage_path)
    rw = ReplayWatcher(base_game_path)

    rw.init_games_screen()

    for replay in rs.replays():
        if replay:
            rw.watch(replay)
