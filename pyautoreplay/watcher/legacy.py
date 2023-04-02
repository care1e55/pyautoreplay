import time
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Optional

from tqdm import tqdm

from pyautoreplay.replay.screp.screp import Replay
from pyautoreplay.utils.action import Action


class ReplayError(Enum):
    EXPANSION_SCENARIO = 'expansion'
    FATAL = 'fatal'


class Actions(str, Enum):
    SINGLE_PLAYER = 's'
    EXPANSION = 'e'
    OK = 'o'
    REPLAY = 'r'
    DOWN = 'down'
    SPEEDUP = 'u'
    SWITCH_PLAYER = 'f5'
    EXIT = 'x'
    CANCEL = 'c'
    TAB = 'tab'
    SPACE = 'space'


class System(str, Enum):
    UBUNTU = 'ubuntu'
    WINDOWS = 'windows'


class ReplayWatcher:

    WATCHING = r'Autoreplay'

    def __init__(self, watching_path: str, action_handler: Action):
        self.watching_path = Path(watching_path)
        self.current_replay = None
        self.action = action_handler

    def watch(self, replay: Replay):
        """Sleep for duration"""
        for _ in tqdm(range(replay.duration), desc=f'Watching replay {replay.name} for {replay.duration} seconds'):
            time.sleep(1)
        self.exit_replay()

    def init_games_screen(self):
        self.action.do_action(Actions.SINGLE_PLAYER)\
            .do_action(Actions.EXPANSION)\
            .do_action(Actions.OK)
        return self

    def start_replay(self):
        time.sleep(3)
        self.action.do_action(Actions.REPLAY)\
            .do_action(Actions.DOWN)\
            .do_action(Actions.OK)
        return self

    def configure_replay(self):
        self.action.do_action(Actions.SPEEDUP)\
            .do_action(Actions.SPEEDUP)\
            .do_action(Actions.SWITCH_PLAYER)\
            .do_action(Actions.SWITCH_PLAYER)
        return self

    def exit_replay(self):
        self.action.do_action(Actions.EXIT)
        time.sleep(3)
        self.action.do_action(Actions.OK)\
            .do_action(Actions.CANCEL)\
            .do_action(Actions.CANCEL)

        return self

    def start_starcraft(self):
        for _ in range(15):
            self.action.do_action(Actions.TAB)
        self.action.do_action(Actions.SPACE)
        return self

    def exit_replays_screen(self):
        self.action.do_action(Actions.OK) \
            .do_action(Actions.CANCEL) \
            .do_action(Actions.CANCEL) \
            .do_action(Actions.CANCEL)
        return self

    @cached_property
    def error(self) -> Optional[ReplayError]:
        return None

    def move_to_watcing_dir(self, replay: Replay):
        replay.copy(self.watching_path / replay.path.name)

    def clean_watching_dir(self):
        for replay in self.watching_path.glob('*.rep'):
            replay.unlink()
