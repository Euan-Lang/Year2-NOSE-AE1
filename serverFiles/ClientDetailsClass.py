import clientFiles.ClientClass 

#Sub-class of client used by the server for storing active client info

class ClientDetails(clientFiles.ClientClass.Client):
    def __init__(self,socket,address):
        super().__init__()
        self._socket = socket
        self._address = address

    def get_socket(self):
        return self._socket
    
    def get_address(self):
        return self._address
