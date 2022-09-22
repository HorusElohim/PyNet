from __future__ import annotations

from .. import Node
from . import ClientRequestRegistration, ClientReplyRegistration, ClientInfo, ClientsRegistered, SERVER_INFO
import traceback


class Server(Node):
    replier_registration: Node.Replier
    requester_alive: Node.Requester

    clients: ClientsRegistered
    active: bool

    def __init__(self):
        Node.__init__(self, SERVER_INFO.name)
        self.upnp = self.get_upnp()
        self.upnp.new_port_mapping(SERVER_INFO.local_ip, SERVER_INFO.registration_port, SERVER_INFO.registration_port)
        self.replier_registration = self.new_replier(SERVER_INFO.get_registration_url())
        self.registered_clients = ClientsRegistered()
        self.active = False
        self.log.debug('done *')

    def start_registration_loop(self):
        self.log.debug('starting...')
        self.active = True
        while self.active:
            recv_msg = self.replier_registration.receive()
            send_msg = self.process_registration_msg(recv_msg)
            self.replier_registration.send(send_msg)

    def process_registration_msg(self, msg: object) -> object:
        self.log.debug(f'processing request: {msg}')
        reply = ''
        try:
            if isinstance(msg, ClientRequestRegistration):
                res = self.registered_clients.add(msg.client)
                reply = ClientReplyRegistration(result=res, clients=self.registered_clients)
            else:
                reply = "Unable to be process"
        except Exception as ex:
            reply = f"Failure -> {ex} \n {traceback.print_exc()}"
            self.log.error(f'Exception: {ex} \n {traceback.print_exc()}')

        return reply
