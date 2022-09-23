from __future__ import annotations

from .. import Node
from . import ClientRequestRegistration, ClientReplyRegistration, ClientInfo, ClientsRegistered, SERVER_INFO
import traceback
import threading
import time


class Server(Node):
    replier_registration: Node.Replier
    requesters_alive: {str: Node.Requester}

    clients: ClientsRegistered
    active: bool

    def __init__(self):
        Node.__init__(self, SERVER_INFO.name)
        self.upnp = self.get_upnp()
        self.upnp.new_port_mapping(SERVER_INFO.local_ip, SERVER_INFO.registration_port, SERVER_INFO.registration_port)
        self.replier_registration = self.new_replier(SERVER_INFO.get_registration_url())
        self.registered_clients = ClientsRegistered()
        self.requesters_alive: {str: Node.Requester} = {}
        self.active = False
        self.threads = []
        self.timer_thread = None
        self.log.debug('done *')

    def start_keep_alive_timer(self):
        self.log.debug("starting keep_alive timer callback")
        self.timer_thread = threading.Thread(target=self._alive_callback_loop)
        self.timer_thread.start()

    def _alive_callback_loop(self):
        self.log.debug("alive_callback_loop callback has started")
        while self.active:
            time.sleep(1)
            self.log.debug("keep-alive request")
            for c_id, req in self.requesters_alive.items():
                req.send("OK")
                recv = req.receive()
                self.log.debug(f"keep-alive recv: {recv}")

    def start_registration_loop(self):
        self.threads.append(threading.Thread(target=self.registration_loop))
        self.threads[-1].start()

    def new_alive_requester(self, client_info: ClientInfo):
        self.log.debug(f'new_alive_requester: {client_info}')
        self.requesters_alive.update({client_info.id: self.new_requester(client_info.get_alive_url_for_server())})

    def registration_loop(self):
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
                self.new_alive_requester(msg.client)
            else:
                reply = "Unable to be process"
        except Exception as ex:
            reply = f"Failure -> {ex} \n {traceback.print_exc()}"
            self.log.error(f'Exception: {ex} \n {traceback.print_exc()}')

        return reply

    def join(self):
        for t in self.threads:
            t.join()
