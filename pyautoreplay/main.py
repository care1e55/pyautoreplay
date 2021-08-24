import sys
from pathlib import Path
from loguru import logger

from replay import ReplayStorage
from watcher import ReplayWatcher

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
