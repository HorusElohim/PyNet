from __future__ import annotations

from . import SteadyNodeBase


class SteadyClientNode(SteadyNodeBase):
    def __init__(self, name: str, ip: str, port: int):
        super().__init__(name, self.Url.Remote(self.Url.SockType.Client, ip, port))
        self.registered = False
        self.registration()

    def registration(self):
        self.send(self.registration_request_message)

    def process_new_message(self, in_msg) -> object:
        return "custom-processing"

    def _process_heartbeat_request(self, msg: SteadyNodeBase.HeartBeatRequest):
        # Save updated nodes
        self.nodes = msg.nodes
        # Send heartbeat reply
        self.send(self.heartbeat_reply_message)

    def process_communications(self):
        while True:
            msg = self.recv()

            # No new message exit
            if msg == self.Sock.RECV_ERROR:
                return

            # Process Heartbeat Request
            elif isinstance(msg, self.HeartBeatRequest):
                self._process_heartbeat_request(msg)

            # Custom Message Processing
            else:
                msg = self.process_new_message(msg)
                if msg:
                    self.send(msg)
