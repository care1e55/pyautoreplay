import sys
from loguru import logger

from pyautoreplay.utils.action import Action
from pyautoreplay.loader import IccupCommand
from pyautoreplay.storage.storage import ReplayStorage
from pyautoreplay.watcher.legacy import ReplayWatcher, System, ReplayError, Actions

WINDOW = r'Brood War'

if __name__ == '__main__':
    storage_path = sys.argv[1]
    watching_path = sys.argv[2]
    logger.info('Starting replays from {}', storage_path)
    a = Action(window=WINDOW, system=System.WINDOWS)
    rs = ReplayStorage(storage_path)
    rw = ReplayWatcher(watching_path, action_handler=a)
    start_iccup_command = IccupCommand(location='C:\\')

    for i, replay in enumerate(rs.replays()):
        rw.clean_watching_dir().move_to_watcing_dir(replay).init_games_screen().start_replay()
        if not rw.error:
            rw.configure_replay()\
                .watch(replay)\
                .exit_replay()
        elif rw.error == ReplayError.EXPANSION_SCENARIO:
            rw.exit_replays_screen()
            continue
        elif rw.error == ReplayError.FATAL:
            # TODO: close error window
            start_iccup_command.execute()
            rw.start_starcraft()
            continue
        else:
            raise 'Unknown error'
