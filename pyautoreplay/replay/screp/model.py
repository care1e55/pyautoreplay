from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Engine(BaseModel):
    Name: str
    ID: int
    ShortName: str


class Speed(BaseModel):
    Name: str
    ID: int


class Type(BaseModel):
    Name: str
    ID: int
    ShortName: str


class Type1(BaseModel):
    Name: str
    ID: int


class Race(BaseModel):
    Name: str
    ID: int
    ShortName: str
    Letter: int


class Color(BaseModel):
    Name: str
    ID: int
    RGB: int


class Player(BaseModel):
    SlotID: int
    ID: int
    Type: Type1
    Race: Race
    Team: int
    Name: str
    Color: Color
    Observer: bool


class Header(BaseModel):
    Engine: Engine
    Version: str
    Frames: int
    StartTime: str
    Title: str
    MapWidth: int
    MapHeight: int
    AvailSlotsCount: int
    Speed: Speed
    Type: Type
    SubType: int
    Host: str
    Map: str
    Players: List[Player]


class Type2(BaseModel):
    Name: str
    ID: int


class Reason(BaseModel):
    Name: str
    ID: int


class LeaveGameCmd(BaseModel):
    Frame: int
    PlayerID: int
    Type: Type2
    Reason: Reason


class Type3(BaseModel):
    Name: str
    ID: int


class ChatCmd(BaseModel):
    Frame: int
    PlayerID: int
    Type: Type3
    SenderSlotID: int
    Message: str


class StartLocation(BaseModel):
    X: int
    Y: int


class PlayerDesc(BaseModel):
    PlayerID: int
    LastCmdFrame: int
    CmdCount: int
    APM: int
    EffectiveCmdCount: int
    EAPM: int
    StartLocation: StartLocation
    StartDirection: int


class Computed(BaseModel):
    LeaveGameCmds: List[LeaveGameCmd]
    ChatCmds: List[ChatCmd]
    WinnerTeam: int
    RepSaverPlayerID: int
    PlayerDescs: List[PlayerDesc]


class ReplayModel(BaseModel):
    Header: Header
    Commands: Any
    MapData: Any
    Computed: Computed
