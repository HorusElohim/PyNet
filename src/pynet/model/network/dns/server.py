from __future__ import annotations

from .. import Node
from . import ClientRequestRegistration, ClientReplyRegistration, ClientInfo, ClientsRegistered, SERVER_INFO, KeepAliveRequest, KeepAliveReply
import traceback
import threading
import time
from zmq import EFSM

SLEEP_KEEP_ALIVE_SEC = 1


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
        self.reg_thread = None
        self.alive_thread = None
        self.log.debug('done *')

    def start_keep_alive_thread(self):
        self.log.debug("starting keep_alive thread")
        self.alive_thread = threading.Thread(target=self._keep_alive_callback_loop)
        self.alive_thread.start()

    def _keep_alive_callback_loop(self):
        self.log.debug("alive_callback_loop callback has started")
        while self.active:
            client_disconnected = []
            time.sleep(SLEEP_KEEP_ALIVE_SEC)
            notify_no_clients = True
            if len(self.requesters_alive) > 0:
                notify_no_clients = True
                self.log.debug("keep-alive request")
                for c_id, req in self.requesters_alive.items():
                    status = req.send(KeepAliveRequest(clients=self.registered_clients))
                    if status:
                        reply = req.receive()
                        if isinstance(reply, KeepAliveReply):
                            self.log.debug(f"keep-alive from {c_id}: OK")
                        else:
                            self.log.error(f"keep-alive from {c_id}: ERROR")
                    else:
                        self.log.error(f"keep-alive from {c_id}: disconnected")
                        client_disconnected.append(c_id)
                # Remove disconnected clients
                for c_id in client_disconnected:
                    self.log.debug(f"keep-alive removing -> {c_id}")
                    self.requesters_alive.pop(c_id)
                    self.registered_clients.remove(c_id)
            else:
                if notify_no_clients:
                    self.log.debug("keep-alive - no clients yet")
                    notify_no_clients = False

    def start_registration_loop(self):
        self.reg_thread = threading.Thread(target=self.registration_loop)
        self.reg_thread.start()

    def new_alive_requester(self, client_info: ClientInfo):
        self.log.debug(f'new_alive_requester: {client_info}')
        self.requesters_alive.update({client_info.id: self.new_requester(client_info.get_alive_url_for_server(), flags=[(self.Sock.Flags.rcv_timeout, 500)])})

    def registration_loop(self):
        self.log.debug('starting registration loop ...')
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
                if self.alive_thread is None:
                    self.start_keep_alive_thread()
            else:
                reply = "Unable to be process"
        except Exception as ex:
            reply = f"Failure -> {ex} \n {traceback.print_exc()}"
            self.log.error(f'Exception: {ex} \n {traceback.print_exc()}')

        return reply

    def join(self):
        self.reg_thread.join()
        self.alive_thread.join()
