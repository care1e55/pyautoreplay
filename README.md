## Brood War Autoreplay

Prereqs:
- `ffmpeg`
- `rust`
- `go`
- `pyenv`
- `python3.9`

Preinstall:
1. Install `pyenv`
2. Install python 3.9
3. Activate python
4. Install `poetry`
5. `poetry shell`
6. `poetry install --extras 'win32gui'`

Start:
1. Unzip autorepack
2. Install CanRep or already installed
3. Start ICCup Brood War
4. Start CanRep
5. `.\start.bat`or
```bat
python .\pyautoreplay\main.py "C:\\autorep_pack\\starcraft\\replays\\ALL" "C:\\autorep_pack\\starcraft\\maps\\replays"
```


TODO:
- Error prone
- async chats
- startup script
- refactor files
- typer cli
- type anotations
- tests