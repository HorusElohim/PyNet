from __future__ import annotations

from . import SteadyNodeBase


class SteadyServerNode(SteadyNodeBase):
    def __init__(self, name: str, port: int, heartbeat_interval=5):
        super().__init__(name, self.Url.Remote(self.Url.SockType.Server, '*', port))
        self.heartbeat_interval = heartbeat_interval

    def process_new_message(self, in_msg) -> object:
        return "custom-processing"

    def _process_registration_request_msg(self, msg: SteadyNodeBase.RegistrationRequest):
        if msg.info.id in self.nodes:
            self.log.debug('received node registration of already connected node')
        else:
            self.log.debug(f'new node request registration: {msg.info}')
        # Update to connected and update heartbeat
        msg.info.connect()
        msg.info.touch_heartbeat()
        # Update the connected nodes
        self.nodes[msg.info.id] = msg.info

    def _process_heartbeat_reply(self, msg: SteadyNodeBase.HeartBeatReply):
        # Check heartbeat between thresholds
        last = self.nodes[msg.id].heartbeat_stamp
        stamp_diff = (msg.stamp - last) * 1e-9
        self.nodes[msg.id].heartbeat_stamp = msg.stamp
        # delta diff too high
        if stamp_diff > self.heartbeat_interval + 0.5:
            self.log.warning(f'Heartbeat from: {msg.id} too high {stamp_diff} on {self.heartbeat_interval + 0.5}')
        # Send reply
        self.send(self.heartbeat_reply_message)

    def process_communications(self):
        while True:
            msg = self.recv()

            # No new message exit
            if msg == self.Sock.RECV_ERROR:
                return

            # Process Registration request
            elif isinstance(msg, self.RegistrationRequest):
                self._process_registration_request_msg(msg)

            # Process Heartbeat Reply
            elif isinstance(msg, self.HeartBeatReply):
                self._process_heartbeat_reply(msg)

            # Custom Message Processing
            else:
                msg = self.process_new_message(msg)
                if msg:
                    self.send(msg)

    def request_heartbeat(self):
        self.send(self.heartbeat_request_message)
