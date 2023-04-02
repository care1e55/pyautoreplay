import enum
import subprocess
from abc import abstractmethod


class Commands(enum.Enum):
    SCREP = 'screp'
    IICUP = 'iccup'
    STARCRAFT = 'starcraft'
    FFMPEG = 'ffmpeg'
    SESSION_QUERY = 'session_query'
    CANREP = 'canrep'
    APP = 'app'


commands_executions = {
    Commands.SCREP: '',
    Commands.STARCRAFT: '',
    Commands.FFMPEG: '',
    Commands.SESSION_QUERY: '',
    Commands.CANREP: '',
    Commands.APP: ''
}


class Command:
    @property
    @abstractmethod
    def execution_string(self) -> str:
        pass


class ScrepCommand(Command):
    def __init__(self, path: str):
        self.path = path

    @property
    def execution_string(self):
        _path_str = f"\"{str(self.path)}\""
        return f'screp {_path_str}'


class IccupCommand(Command):
    def __init__(self):
        pass

    @property
    def execution_string(self):
        return ''


class FfmpegCommand(Command):
    def __init__(self, twitch_token):
        self.twitch_token = twitch_token

    @property
    def execution_string(self):
        return f"""
            ffmpeg  -f gdigrab 
                    -s 640x480 
                    -framerate 25 
                    -i title="Brood War" 
                    -f dshow 
                    -i audio="CABLE Output (VB-Audio Virtual Cable)" 
                    -c:v libx264 
                    -preset fast 
                    -pix_fmt yuv420p 
                    -s 640x480 
                    -threads 0 
                    -f flv {self.twitch_token}
            """


class CanrepCommand(Command):
    def __init__(self):
        pass

    @property
    def execution_string(self):
        return ''


class CommandExecutor:
    @staticmethod
    def execute(command: Command):
        p = subprocess.Popen(
            command.execution_string,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        return ''.join([line.decode("utf-8") for line in p.stdout.readlines()])
