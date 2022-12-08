import socket
import serverFiles.ClientDetailsClass 
import common.Operations
from common.StatusMonitorClass import active_status_monitor

class Server:
    def __init__(self,port):
        self._port = int(port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        try:
            self._socket.bind(("localhost", self._port))
            self._socket.listen(5)
            self._addr = self._socket.getsockname()
            active_status_monitor.set_output(f"Server started on {self._addr[0]} at port: {self._addr[1]}")
        except:
            active_status_monitor.set_error("Incorrect port or port in use, try a diffrent port number")

    def accept_connection(self):
        client_socket, client_address = self._socket.accept()
        return serverFiles.ClientDetailsClass.ClientDetails(client_socket,client_address) #creates an instance of client details to store details of active connetions.

    def retrieve_data(self,connection_details):
        common.Operations.receive_data(connection_details)

    
    def get_port(self):
        return self.port
    
    def get_socket(self):
        return self._socket