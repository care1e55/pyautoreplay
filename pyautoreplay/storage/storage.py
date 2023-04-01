from enum import Enum
from pathlib import Path
from random import shuffle
from typing import Iterable

from loguru import logger

from pyautoreplay.replay.screp.screp import Replay


class ReplayStorage:
    # TODO: multiple storage support so not Path but ReplayPath of storage type

    ALL = 'ALL'

    def __init__(self, replays_storage_path: str):
        self.extension = '.rep'
        self.replays_storage_path = Path(replays_storage_path)

    def replays(self) -> Iterable:
        replays = list(self.replays_storage_path.glob(f'*{self.extension}'))
        shuffle(replays)
        for replay_path in replays:
            if not replay_path.is_file():
                continue
            try:
                yield Replay(replay_path)
            except:
                continue
