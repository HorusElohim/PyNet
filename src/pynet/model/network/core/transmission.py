from zmq import ZMQError
from typing import Union
from ...common import Logger
from . import Packet, Connection, DataHandle
from typing import Any

LOGGER = Logger()


class Transmission:
    @staticmethod
    def recv(conn: Connection, raw: bool = False) -> object:
        if raw:
            return Transmission._recv_(conn)
        else:
            received = Transmission._recv_(conn)
            if received and isinstance(received, Packet):
                return received.data
            else:
                return None

    @staticmethod
    def check_connection_is_open(conn: Connection) -> bool:
        if conn.open:
            return True
        else:
            LOGGER().debug(f"Transmission: the connection is close -> {conn}")
            return False

    @staticmethod
    def _recv_(conn: Connection) -> Union[Packet, Any]:
        if Transmission.check_connection_is_open(conn):
            try:
                obj = DataHandle.decode(conn.socket.recv())  # type: ignore[arg-type]
                LOGGER().debug(f"Transmission: _recv_ -> {obj}")
                return obj
            except ZMQError as ex:
                LOGGER().error(f"Transmission: Error _recv_ -> {ex}")
                return None
        return None

    @staticmethod
    def _send_(conn: Connection, obj: object) -> bool:
        if Transmission.check_connection_is_open(conn):
            try:
                LOGGER().debug(f"Transmission: _send_ -> {obj}")
                conn.socket.send(DataHandle.encode(obj))
                LOGGER().debug("Transmission: _send_ completed")
                return True
            except ZMQError as ex:
                LOGGER().error(f"Transmission: Error _send_ -> {ex}")
                return False
        else:
            return False

    @staticmethod
    def _recv_packet(conn: Connection) -> Union[Packet, Any]:
        if Transmission.check_connection_is_open(conn):
            try:
                pkt = DataHandle.decode(conn.socket.recv())  # type: ignore[arg-type]
                LOGGER().debug(f"Transmission: recv_packet -> {pkt}")
                return pkt
            except ZMQError as ex:
                LOGGER().error(f"Transmission: Error recv_packet -> {ex}")
                return None
        return None

    @staticmethod
    def send(conn: Connection, obj: object, as_packet: bool = True) -> bool:
        if as_packet:
            if not isinstance(obj, Packet):
                obj = Transmission.create_packet(conn, obj)
        return Transmission._send_(conn, obj)

    @staticmethod
    def send_data(conn: Connection, data: object) -> bool:
        if Transmission.check_connection_is_open(conn):
            return Transmission.send_packet(conn, Transmission.create_packet(conn, data))
        return False

    @staticmethod
    def send_packet(conn: Connection, pkt: Packet) -> bool:
        if Transmission.check_connection_is_open(conn):
            try:
                LOGGER().debug(f"Transmission: send_packet -> {pkt}")
                conn.socket.send(DataHandle.encode(pkt))
                LOGGER().debug("Transmission: send_packet completed")
                return True
            except ZMQError as ex:
                LOGGER().error(f"Transmission: Error send_packet -> {ex}")
                return False
        else:
            return False

    @staticmethod
    def create_packet(conn: Connection, data: object = None) -> Packet:
        return conn.create_packet(data=data)
