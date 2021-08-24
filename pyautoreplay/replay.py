import json
import subprocess
from pathlib import Path
from typing import Iterable, Dict, Any
from loguru import logger
import shutil
from random import shuffle


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