from __future__ import annotations
from time import time_ns

from . import SteadyNodeBase, NodeRegistration, NodeHeartbeatServer, NodeHeartbeatClient


class SteadyServerNode(SteadyNodeBase):
    def __init__(self, name: str, port: int, *args, **kwargs):
        super().__init__(name, self.Url.Remote(self.Url.SockType.Server, '*', port), *args, **kwargs)
        self.register_callback(NodeRegistration, self._process_registration_request_msg)
        self.register_callback(NodeHeartbeatClient, self._process_heartbeat)

    def _process_registration_request_msg(self, msg: NodeRegistration):
        new_node = False
        if msg.info.identifier not in self.nodes:
            new_node = True

        self.log.info(f'Node Registration from {"new" if new_node else "old"} : {msg.info}')
        # Update to connected and update heartbeat
        msg.info.connect()
        # Update the connected nodes
        self.nodes[msg.info.identifier] = msg.info
        self.log.info(f"Node Registration completed: {self.nodes}")
        # Reply heartbeat
        self.send(NodeHeartbeatServer(nodes=self.nodes))

    def _process_heartbeat(self, msg: NodeHeartbeatClient):
        warning = True
        stamp_diff = (time_ns() - self.nodes[msg.identifier].last_heartbeat_stamp) * 1e-9
        if self.nodes[msg.identifier].is_heartbeat_valid(self.spin_interval + 0.5):
            warning = False
        self.log.info(f'Heartbeat from: {msg.identifier}, {stamp_diff}s on {self.spin_interval + 0.5}s interval - {"WARNING" if warning else "OK"}')
        # Update heartbeat stamp
        self.nodes[msg.identifier].touch_heartbeat()
        # Reply heartbeat
        self.send(NodeHeartbeatServer(nodes=self.nodes))

    def _check_heartbeats(self):
        for nid, ninfo in self.nodes.items():
            pass

