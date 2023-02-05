import json
import subprocess
from pathlib import Path
from typing import Dict, Any
import shutil

from pyautoreplay.replay.screp.model import ReplayModel


class Replay:
    FRAMES_PER_SECOND = 23.84

    def __init__(self, replay_path: Path):
        self.path = replay_path
        self.json = self._parse(self.path)
        self.replay = ReplayModel.parse_obj(self.json)

    # TODO: multiple storage support so not Path but ReplayPath of storage type
    def _parse(self, path) -> Dict[Any, Any]:
        _path_str = f"\"{str(path)}\""
        call_str = f'screp {_path_str}'  # call go script
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
        self.path.unlink()

    def copy(self, to_path: Path):
        shutil.copy(self.path, to_path)

    @property
    def duration(self) -> int:
        duration = self.replay.Header.Frames / self.FRAMES_PER_SECOND
        return int(round(duration, 0))

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def winner(self) -> str:
        raise NotImplementedError()

    @property
    def loser(self) -> str:
        raise NotImplementedError()
