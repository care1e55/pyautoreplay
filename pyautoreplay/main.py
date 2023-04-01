import sys
from pathlib import Path
from loguru import logger

from pyautoreplay.storage.storage import ReplayStorage
from pyautoreplay.watcher.legacy import ReplayWatcher, System, ReplayError, Action

if __name__ == '__main__':
    storage_path = Path(sys.argv[1])
    watching_path = Path(sys.argv[2])
    logger.info('Starting replays from {}', storage_path)
    rs = ReplayStorage(storage_path)
    rw = ReplayWatcher(rs, watching_path, system=System.WINDOWS)

    for i, replay in enumerate(rs.replays()):
        rw.clean_watching_dir().move_to_watcing_dir(replay).init_games_screen().start_replay()
        if not rw.error:
            rw.configure_replay()\
                .watch(replay)\
                .exit_replay()\
                .do_action(Action.CANCEL)\
                .do_action(Action.CANCEL)
            continue
        if rw.error == ReplayError.EXPANSION_SCENARIO:
            rw\
                .do_action(Action.OK)\
                .do_action(Action.CANCEL)\
                .do_action(Action.CANCEL)\
                .do_action(Action.CANCEL)
        elif rw.error == ReplayError.FATAL:
            # reboot app
            pass
        else:
            raise 'Unknown error'
