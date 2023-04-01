import sys
from pathlib import Path
from loguru import logger

from pyautoreplay.storage.storage import ReplayStorage
from pyautoreplay.watcher.legacy import ReplayWatcher, System

if __name__ == '__main__':
    storage_path = Path(sys.argv[1])
    watching_path = Path(sys.argv[2])
    logger.info('Starting replays from {}', storage_path)
    replays_storage_path = Path(storage_path)
    rs = ReplayStorage(replays_storage_path)
    rw = ReplayWatcher(rs, watching_path, system=System.WINDOWS)

    for i, replay in enumerate(rs.replays()):
        rw._clean_watching_dir()
        rw._move_to_watcing_dir(replay)
        rw.init_games_screen()
        rw.init_replay()
        rw.watch(replay)
        rw.exit_replay()
