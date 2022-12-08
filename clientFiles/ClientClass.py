import socket
import common.Operations
from common.StatusMonitorClass import active_status_monitor


class Client:

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(20)

    
    def connection_details(self,addr,port):
        self._address = addr
        self._port = int(port)

    def establish_connection(self):
        try:
            self._socket.connect((self._address,self._port))
        except:
            active_status_monitor.set_error("Could not connect to server")
    
    def get_socket(self):
        return self._socket

    def send_data(self,command,file=None):
        common.Operations.send_data(self,command,file)

    def retrieve_data(self):
        common.Operations.receive_data(self)

    def get_address(self):
        return self._address

    def get_port(self):
        return self._port

    def close_connection(self):
        self._socket.close()
