from __future__ import annotations

from . import SteadyNodeBase


class SteadyServerNode(SteadyNodeBase):
    def __init__(self, name: str, port: int, heartbeat_interval=5):
        super().__init__(name, self.Url.Remote(self.Url.SockType.Server, '*', port))
        self.heartbeat_interval = heartbeat_interval

    def process_new_message(self, in_msg) -> object:
        return "custom-processing"

    def _process_registration_request_msg(self, msg: SteadyNodeBase.RegistrationRequest):
        new_node = False
        if msg.info.id not in self.nodes:
            new_node = True

        self.log.info(f'Node Registration from {"new" if new_node else "old"} : {msg.info}')
        # Update to connected and update heartbeat
        msg.info.connect()
        msg.info.touch_heartbeat()
        # Update the connected nodes
        self.nodes[msg.info.id] = msg.info
        self.log.info(f"Node Registration completed: {msg.info}")
        # Request first heartbeat
        self.request_heartbeat()

    def _process_heartbeat(self, msg: SteadyNodeBase.HeartBeatReply):
        # Check heartbeat between thresholds
        last = self.nodes[msg.id].heartbeat_stamp
        stamp_diff = (msg.stamp - last) * 1e-9
        self.nodes[msg.id].heartbeat_stamp = msg.stamp
        # delta diff too high
        if stamp_diff > self.heartbeat_interval + 0.5:
            self.log.warning(f'Heartbeat from: {msg.id} too high {stamp_diff} on {self.heartbeat_interval + 0.5}')
        self.log.info(f'{self.nodes[msg.id]}')

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
                self._process_heartbeat(msg)
                self.request_heartbeat()

            # Custom Message Processing
            else:
                msg = self.process_new_message(msg)
                if msg:
                    self.send(msg)

    def request_heartbeat(self):
        self.send(self.heartbeat_request_message)
