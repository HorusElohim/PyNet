from __future__ import annotations
from dataclasses import dataclass
from time import sleep, time_ns
import threading
from pynet import Node


@dataclass(repr=True)
class HeartbeatRequest:
    node_info: dict


@dataclass(repr=True)
class HeartbeatReply:
    pass


class Requester(Node):
    def __init__(self, name: str, url: Node.Url, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.req = self.new_requester(url, *args, **kwargs)
        self.heartbeat_req_thread = None

    def _heartbeat_req_loop(self, hertz=1):
        while self.req.is_open:
            start = time_ns()
            self._heartbeat_processing()
            # Ensure processing hertz
            sleep(1 / hertz - (time_ns() - start) * 1e-9)

    def _heartbeat_processing(self):
        disconnection = True
        if self.req.send(HeartbeatRequest(self.info)):
            if not self.req.receive() == self.Sock.RECV_ERROR:
                disconnection = False
        # Possible disconnections
        if disconnection:
            self.req.close()

    def start_heartbeat(self):
        self.heartbeat_req_thread = threading.Thread(target=self._heartbeat_processing)
        self.heartbeat_req_thread.start()

    def __del__(self):
        self.heartbeat_req_thread.join()


class Replier(Node):
    def __init__(self, name: str, url: Node.Url, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.rep = self.new_replier(url, *args, **kwargs)
        self.heartbeat_rep_thread = None

    def _heartbeat_rep_loop(self):
        while self.rep.is_open:
            disconnection = True
            hb = self.rep.receive()
            if not hb == self.Sock.RECV_ERROR:
                self.rep.send(HeartbeatReply())