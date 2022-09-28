from __future__ import annotations

from . import SteadyNodeBase, NodeHeartbeatServer, NodeHeartbeatClient, NodeRegistration


class SteadyClientNode(SteadyNodeBase):
    def __init__(self, name: str, ip: str, port: int, *args, **kwarg):
        super().__init__(name, self.Url.Remote(self.Url.SockType.Client, ip, port), *args, **kwarg)
        self.registered = False
        self.register_callback(NodeHeartbeatServer, self._process_heartbeat_request)
        self.node_registration()

    def node_registration(self):
        self.log.info(f"Node registration to: {self.url}")
        self.send(NodeRegistration(info=self.node_info))

    def _process_heartbeat_request(self, msg: NodeHeartbeatServer):
        self.log.info(f"Heartbeat: {str(msg)}")
        # Save updated nodes
        self.nodes = msg.nodes
        # Send heartbeat reply
        self.send(NodeHeartbeatClient(identifier=self.node_info.identifier))

    def _respawn_check_(self):
        pass
