import json
import subprocess
from pathlib import Path
from typing import Dict, Any
from loguru import logger
import shutil
from functools import cached_property


class Replay:
    FRAMES_PER_SECOND = 23.84

    def __init__(self, replay_path: Path):
        self.replay_path = replay_path
        self._replay_path_str = f"\"{str(replay_path)}\""

    # TODO: multiple storage support so not Path but ReplayPath of storage type
    @cached_property
    def content(self) -> Dict[Any, Any]:
        call_str = f'screp {self._replay_path_str}'  # call go script
        # logger.info("Call script: {}", call_str) \
        # print("Call script: \n{}".format(call_str))
        p = subprocess.Popen(
            call_str,
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
    def duration(self) -> int:
        duration = self.content['Header']['Frames'] / self.FRAMES_PER_SECOND
        return int(round(duration, 0)

    @property
    def winner(self) -> str:
        raise NotImplementedError()

    @property
    def loser(self) -> str:
        raise NotImplementedError()
