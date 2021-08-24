import time
from tqdm import tqdm


class ReplayStub:
    def __init__(self, duration):
        self.duration = duration


def test_progressbar():
    replay = ReplayStub(10)
    for _ in tqdm(
            range(int(round(replay.duration + 5, 0))),
            desc=f'Watching replay for {replay.duration} seconds'
    ):
        time.sleep(1)


if __name__ == '__main__':
    test_progressbar()
