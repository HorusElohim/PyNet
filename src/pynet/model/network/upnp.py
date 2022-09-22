import upnpclient
import socket

from .. import AbcEntity, Logger, Singleton


class UpnpRegistrationFailed(Exception):
    def __init__(self, logger: Logger):
        logger.log.error("UPNP Registration map failed! Please enable the NAT on your router page.")


class UpnpDeviceIsNone(Exception):
    def __init__(self, logger: Logger):
        logger.log.error("UPNP device is None. Be sure to call discovery or set auto_discover to True")


class Upnp(AbcEntity):
    def __init__(self, auto_discover=False, **kwargs):
        AbcEntity.__init__(self, entity_name='Upnp', **kwargs)
        self.devices = []
        self.device = None
        if auto_discover:
            self.discover()
        self.log.debug("done *")

    def safe_check_discovery_needed(self):
        if not self.device:
            self.discover()

    def discover(self):
        self.log.debug("discovering routers ... (can takes some seconds)")
        self.devices = upnpclient.discover()
        self.device = self.devices[0]
        if not self.device:
            raise UpnpDeviceIsNone(self)

    def get_public_ip(self):
        self.safe_check_discovery_needed()
        ip = self.device.WANIPConn1.GetExternalIPAddress()['NewExternalIPAddress'] if self.device else ''
        self.log.debug(f"public-ip : {ip}")
        return ip

    def get_local_ip(self):
        self.safe_check_discovery_needed()
        ip = socket.gethostbyname(socket.gethostname())
        self.log.debug(f"local-ip : {ip}")
        return ip

    def get_status(self):
        self.safe_check_discovery_needed()
        res = False
        if self.device:
            if 'Connected' in self.device.WANIPConn1.GetStatusInfo()["NewConnectionStatus"]:
                res = True
        self.log.debug(f"connected : {res}")
        return res

    def get_nat_sip(self) -> (bool, bool):
        self.safe_check_discovery_needed()
        nat, sip = False, False
        if self.device:
            status = self.device.WANIPConn1.GetNATRSIPStatus()
            nat = status["NewNATEnabled"]
            sip = status["NewRSIPAvailable"]
        self.log.debug(f"nat: {nat} sip:{sip}")
        return nat, sip

    def new_port_mapping(self, ip, internal_port, external_port):
        self.safe_check_discovery_needed()
        self.delete_port_mapping(ip, external_port)
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
        self.safe_check_discovery_needed()
        self.log.debug(f"deleting mapping: 0.0.0.0:{external_port} -> {ip}")
        self.device.WANIPConn1.DeletePortMapping(NewRemoteHost=ip, NewExternalPort=external_port, NewProtocol="TCP")

    def check_port_mapping(self, ip, external_port) -> bool:
        self.safe_check_discovery_needed()
        tmp = self.device.WANIPConn1.GetSpecificPortMappingEntry(NewRemoteHost=ip, NewExternalPort=external_port, NewProtocol="TCP")
        res = False
        if "NewEnabled" in tmp:
            res = tmp["NewEnabled"]
        self.log.debug(f"check_port_mapping: 0.0.0.0:{external_port} -> {ip} | {res}")
        return res


class UpnpSingleton(Upnp, metaclass=Singleton):
    pass


UPNP = UpnpSingleton(auto_discover=False)
