from __future__ import annotations
from dataclasses import dataclass
from time import time_ns
from typing import Dict
from enum import Enum

from ... import oneshot_str_hexhashing
from .. import SockUrl


@dataclass(repr=True, init=True)
class NodeInfo:
    class Status(Enum):
        disconnected = 0
        connected = 1

    name: str
    pub_ip: str
    local_ip: str
    url: SockUrl.Abc
    status: Status = Status.disconnected
    last_heartbeat_stamp: int = time_ns()
    _identifier: int = 0
    warning_counts: int = 0

    @property
    def identifier(self):
        if self._identifier == 0:
            self._identifier = oneshot_str_hexhashing(self.name + str(self.pub_ip))
        return self._identifier

    def connect(self):
        self.status = self.Status.connected

    def disconnect(self):
        self.status = self.Status.disconnected

    def is_heartbeat_valid(self, th_seconds: float):
        diff = (time_ns() - self.last_heartbeat_stamp) * 1e-9 < th_seconds
        if diff > th_seconds:
            self.warning_counts += 1
        return diff < th_seconds

    def touch_heartbeat(self):
        self.last_heartbeat_stamp = time_ns()


# Type Aliases
Nodes = Dict[int, NodeInfo]


@dataclass(repr=True, init=True)
class NodeRegistration:
    info: NodeInfo


@dataclass(repr=True, init=True)
class NodeHeartbeatServer:
    nodes: Nodes
    stamp: int = time_ns()


@dataclass(repr=True)
class NodeHeartbeatClient:
    identifier: int
    stamp: int = time_ns()

    def __init__(self, identifier):
        self.identifier = identifier
        self.stamp = time_ns()
