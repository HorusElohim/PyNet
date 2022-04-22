from zmq import (
    Context, Socket, ZMQError,
    SUB, PUB, REQ, REP, PUSH, PULL,
    SUBSCRIBE
)
from enum import Enum
from typing import List
from ...common import Logger
from .channel import BaseChannel


class Connection:
    """
        Connection Class
        Used to manage the zmq socket

    """
    class Type(Enum):
        """
        Type of Connection
        """
        subscriber = SUB
        publisher = PUB
        replier = REP
        requester = REQ
        pusher = PUSH
        puller = PULL

    type: Type
    socket: Socket
    channel: BaseChannel
    open: bool = False
    bind_types: List[Type] = [Type.publisher, Type.replier, Type.puller]
    connect_types: List[Type] = [Type.subscriber, Type.requester, Type.pusher]

    def __init__(self, connection_type: Type, channel: BaseChannel, context: Context = Context()):
        """

        :param connection_type: Connection Type
        :param channel: Target Channel
        :param context: ZMQ Context

        """
        self.type = connection_type
        self.channel = channel
        self.socket = context.socket(self.type.value)
        self.logger = Logger()

        try:
            if self.type in self.bind_types:
                self.socket.bind(self.channel())
                self.logger().debug(f'{self.__class__.__name__}: BIND Socket')
            elif self.type in self.connect_types:
                self.socket.connect(self.channel())
                self.logger().debug(f'{self.__class__.__name__}: CONNECT Socket')
                if self.type is self.Type.subscriber:
                    self.socket.setsockopt(SUBSCRIBE, b'')
            else:
                self.logger().error(f'{self.__class__.__name__}: Zmq pattern not recognized {self.Type}')

            self.logger().debug(f'{self.__class__.__name__}: ready on channel ->{channel}')
            self.open = True

        except ZMQError as ex:
            self.open = False
            self.logger().error(f"{self.__class__.__name__}: Error init socket for class {self} Exception -> {ex}")
        finally:
            self.logger().debug(f'{self.__class__.__name__}: Constructed')
