import json
import subprocess
import time
from enum import Enum
from pathlib import Path
from typing import Iterable, Dict, Any
import AppKit
import pyautogui


class Action(Enum):
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
        self.content = self._parse(replay_path)

    # TODO: multiple storage support so not Path but ReplayPath of storage type
    @staticmethod
    def _parse(replay_path: Path) -> Dict[Any, Any]:
        """call go script"""
        p = subprocess.Popen(
            f'resources/screp {replay_path}',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        # TODO: effective
        result_str = ''
        for line in p.stdout.readlines():
            result_str += line.decode("utf-8")
        return json.loads(result_str)

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
        for replay_path in self.replays_storage.glob('*.rep'):
            if not replay_path.is_file():
                continue
            yield Replay(replay_path)


class ReplayWatcher:
    BASE_GAME_PATH = Path('starcraft')
    WATCHING_DIR = Path('Watching')

    def __init__(self):
        pass

    def watch(self, replay: Replay):
        print(f'Watching replay for {replay.duration}')
        self.init_replay()
        time.sleep(replay.duration + 5)
        self.exit_replay()

    def _do_action(self, key: str):
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

    def init_replay(self):
        self.do_action(Action.REPLAY)
        # for _ in range(5):
        #     self.do_action(Action.DOWN)
        # self.do_action(Action.OK)
        self.do_action(Action.DOWN)
        self.do_action(Action.OK)
        self.do_action(Action.SPEEDUP)
        # self.do_action(Action.SPEEDUP)
        self.do_action(Action.SWITCH_PLAYER)
        self.do_action(Action.SWITCH_PLAYER)

    def exit_replay(self):
        self.do_action(Action.EXIT)
        self.do_action(Action.OK)

    def clean_watching_dir(self):
        pass


if __name__ == '__main__':
    replays_storage_path = Path('resources')

    rs = ReplayStorage(replays_storage_path)
    rw = ReplayWatcher()

    rw.init_games_screen()

    for replay in rs.replays():
        rw.watch(replay)
