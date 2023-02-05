from enum import Enum
from pathlib import Path
from random import shuffle
from typing import Iterable

from loguru import logger

from pyautoreplay.replay.replay import Replay


class ReplayStorage:
    # TODO: multiple storage support so not Path but ReplayPath of storage type

    ALL = 'ALL'
    WATCHING = 'watching'

    def __init__(self, replays_storage: Path):
        self.extension = '.rep'
        self.replays_storage = replays_storage
        self.replays_path = replays_storage / self.ALL
        self.watching_path = replays_storage / self.WATCHING

    def replays(self) -> Iterable:
        replays = list(self.replays_storage.glob(f'*{self.extension}'))
        shuffle(replays)
        for replay_path in replays:
            if not replay_path.is_file():
                continue
            logger.info('Watching replay: {}', replay_path)
            try:
                yield Replay(replay_path)
            except:
                continue

    def _move_to_watcing_dir(self, replay: Replay):
        replay.copy(self.watching_path / replay.path.name)

    def _clean_watching_dir(self):
        for replay in self.watching_path.glob('*.rep'):
            replay.unlink()
