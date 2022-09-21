import upnpclient
import socket

from .. import AbcEntity, Logger


class UpnpRegistrationFailed(Exception):
    def __init__(self, logger: Logger):
        logger.log.error("UPNP Registration map failed! Please enable the NAT on your router page.")


class UpnpDeviceIsNone(Exception):
    def __init__(self, logger: Logger):
        logger.log.error("UPNP device is None. Be sure to call discovery or set auto_discover to True")


class Upnp(AbcEntity):
    def __init__(self, auto_discover=True, **kwargs):
        AbcEntity.__init__(self, entity_name='Upnp', **kwargs)
        self.devices = []
        self.device = None
        if auto_discover:
            self.discover()
        self.log.debug("done *")

    def discover(self):
        self.log.debug("discovering routers ... (can takes some seconds)")
        self.devices = upnpclient.discover()
        self.device = self.devices[0]

    def get_public_ip(self):
        if not self.device:
            raise UpnpDeviceIsNone(self)
        ip = self.device.WANIPConn1.GetExternalIPAddress()['NewExternalIPAddress'] if self.device else ''
        self.log.debug(f"public-ip : {ip}")
        return ip

    def get_local_ip(self):
        if not self.device:
            raise UpnpDeviceIsNone(self)
        ip = socket.gethostbyname(socket.gethostname())
        self.log.debug(f"public-ip : {ip}")
        return ip

    def get_status(self):
        if not self.device:
            raise UpnpDeviceIsNone(self)
        res = False
        if self.device:
            if 'Connected' in self.device.WANIPConn1.GetStatusInfo()["NewConnectionStatus"]:
                res = True
        self.log.debug(f"connected : {res}")
        return res

    def get_nat_sip(self) -> (bool, bool):
        if not self.device:
            raise UpnpDeviceIsNone(self)
        nat, sip = False, False
        if self.device:
            status = self.device.WANIPConn1.GetNATRSIPStatus()
            nat = status["NewNATEnabled"]
            sip = status["NewRSIPAvailable"]
        self.log.debug(f"nat: {nat} sip:{sip}")
        return nat, sip

    def new_port_mapping(self, ip, internal_port, external_port):
        if not self.device:
            raise UpnpDeviceIsNone(self)
        self.log.debug(f"asking mapping: 0.0.0.0:{external_port} -> {ip}:{internal_port}")
        self.device.WANIPConn1.AddPortMapping(
            NewRemoteHost='0.0.0.0',
            NewExternalPort=external_port,
            NewProtocol='TCP',
            NewInternalPort=internal_port,
            NewInternalClient=ip,
            NewEnabled='1',
            NewPortMappingDescription='Testing',
            NewLeaseDuration=10000)
        res = self.check_port_mapping(ip, external_port)
        if not res:
            raise UpnpRegistrationFailed(self)
        return res

    def delete_port_mapping(self, ip, external_port):
        if not self.device:
            raise UpnpDeviceIsNone(self)
        self.log.debug(f"deleting mapping: 0.0.0.0:{external_port} -> {ip}")
        self.device.WANIPConn1.DeletePortMapping(NewRemoteHost=ip, NewExternalPort=external_port, NewProtocol="TCP")

    def check_port_mapping(self, ip, external_port) -> bool:
        if not self.device:
            raise UpnpDeviceIsNone(self)
        tmp = self.device.WANIPConn1.GetSpecificPortMappingEntry(NewRemoteHost=ip, NewExternalPort=external_port, NewProtocol="TCP")
        res = False
        if "NewEnabled" in tmp:
            res = tmp["NewEnabled"]
        self.log.debug(f"check_port_mapping: 0.0.0.0:{external_port} -> {ip} | {res}")
        return res
