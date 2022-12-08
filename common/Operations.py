import os
import clientFiles.ClientClass as Comparison_Class
import serverFiles.ClientDetailsClass as ServerClientClass
from common.StatusMonitorClass import active_status_monitor


def receive_data(user,no_bits=5000):
    
    def transfer_confirmation():#used after recieving data to infrom other party of sucessful receipt.
        user.get_socket().sendall("CONFIRM".encode('utf-8'))
        
    received_header_data = user.get_socket().recv(no_bits)
    if received_header_data == b'':
        active_status_monitor.set_error("No data recieved break in connection")
        return

    transfer_confirmation()

    receive_header_data_decoded = received_header_data.decode("utf-8")
    no_fields = int(receive_header_data_decoded)
    data = []
    for i in range(no_fields): #iterates for number of recieved field.
        data_packet =b''
        while True:
            received_data = user.get_socket().recv(no_bits)
            if "EOD".encode("utf-8") in received_data: #Ensures all data of a given field is recieved correctly.
                data_packet += received_data[:-3]
                break
            data_packet += received_data

        data.append(data_packet)
        transfer_confirmation()
    command = data[0].decode('utf-8')
    execute_command(user,command,*data[1:])




def send_data(user,command,*data):
    def transfer_confirmation(): #awaits confirmation from other party that sent data has been recieved.
       user.get_socket().recv(5000)

    data = list(data)
    no_fields=0
    if command == "list":
        if data != [None]:
            no_fields = len(data)+1
        else:
            no_fields = 1
        data.insert(0,"list".encode('utf-8'))
    
    elif command == "get":
        if data == None:
            active_status_monitor.set_error("No file")
        elif type(user) != ServerClientClass.ClientDetails:  #checks whether command is being executed by client or server.
                no_fields =2
                data.insert(0,"get".encode('utf-8'))
                data[1] = data[1].encode('utf-8')
        else:
            no_fields = 3
            data = data[0] #strips one nested layer of list
            data.insert(0,"get".encode('utf-8'))

    
    elif command == "put":
        if data == None:
            active_status_monitor.set_error("No file")
        elif type(user) == ServerClientClass.ClientDetails:
            no_fields = 2
            data.insert(0,"put".encode('utf-8'))
            data[1] =data[1].encode("utf-8")
        else:
            no_fields =3
            with open(data[0], 'rb') as f:# opens and reads binary data of desired file
                content = f.read()
                data.insert(0,"put".encode('utf-8'))
                data[1] = data[1].encode('utf-8')
                data.append(content)

    else:
        active_status_monitor.set_error("Command not recognised")

    
    if active_status_monitor.get_execution_state()== True:
        try:
            user.get_socket().sendall(str(no_fields).encode('utf-8'))
            transfer_confirmation()

            for i in range(no_fields):
                user.get_socket().sendall(data[i]+"EOD".encode('utf-8'))
                transfer_confirmation()
        except:
            active_status_monitor.set_error("Could not send all data, connection timmed out")




def execute_command(user,command=None,file_name=None,file_data=None):
    
    
    def put(user,*additional_data):
        def client(user,file_name):
            file_name = file_name.decode("utf-8")
            #code below used to set correct output for client display 
            active_status_monitor.set_output("put")
            active_status_monitor.set_status("success")
            active_status_monitor.set_additonal_output(f"\t {file_name} sent to server")
            user.close_connection()

        def server(user,file_name, file_data):
            file_name = file_name.decode('utf-8')
            if os.path.exists(file_name):

                active_status_monitor.set_error("File already exists")
                return
            else:
                with open(file_name,"wb") as f: #creates file on server and writes recieved binary data.
                    f.write(file_data)
                #code below used to set correct output for server display
                active_status_monitor.set_output("put")
                active_status_monitor.set_status("success")
                active_status_monitor.set_additonal_output(f"\t {file_name} recieved")
                user.send_data("put",file_name) #send response to client.
                
            
        #checks whether the command is being called by client or sever and executes accordinly.
        client(user,additional_data[0]) if type(user) != ServerClientClass.ClientDetails else server(user,additional_data[0],additional_data[1])


    def get(user,*additional_data):
        
        def client(user,file_name,file_data):
            file_name = file_name.decode('utf-8')
            if os.path.exists(file_name):

                active_status_monitor.set_error("File already exists")
                return
            else:
                with open(file_name,"wb") as f:
                    f.write(file_data)

            #code below used to set correct output for client display 
            active_status_monitor.set_output("get")
            active_status_monitor.set_status("success")
            active_status_monitor.set_additonal_output(f"\t {file_name} retrieved")

        def server(user,file_name):
            file_name =file_name.decode('utf-8')
            data =[]
            with open(file_name, 'rb') as f:
                content = f.read()
                data.append(file_name.encode('utf-8'))
                data.append(content)
                user.send_data("get",data)

            #code below used to set correct output for server display
            active_status_monitor.set_output("get")
            active_status_monitor.set_status("success")
            active_status_monitor.set_additonal_output(f"\t {file_name} served")

        #checks whether the command is being called by client or sever and executes accordinly.
        client(user,additional_data[0],additional_data[1]) if type(user) != ServerClientClass.ClientDetails else server(user,additional_data[0])
                

    def lst(user,*additional_data):
        def server(user):
            file_list = os.listdir()
            response = "\n".join(x for x in file_list)
            response_encoded = response.encode('utf-8')
            user.send_data("list",response_encoded) #send response to client.
            #code below used to set correct output for server display
            active_status_monitor.set_output("list")
            active_status_monitor.set_status("success")


        def client(user,lst):
            #code below used to set correct output for client display 
            active_status_monitor.set_output("list")
            active_status_monitor.set_status("success")
            active_status_monitor._additonal_output = "\n"+lst.decode('utf-8')


        #checks whether the command is being called by client or sever and executes accordinly.
        client(user, additional_data[0]) if type(user) != ServerClientClass.ClientDetails else server(user)


    # code below executes general command based on data passed from recieved data.   
    commands = {"put":put,"get":get,"list":lst}
    
    if command in commands:
        commands[command](user,file_name,file_data)
    


    