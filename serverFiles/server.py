import sys
import os
#alteration to execution pathing allowing for python files to be seperated in folders 
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(ROOT_DIR)
import ServerClass
from common.StatusMonitorClass import active_status_monitor

def main(port=None):
    if port==None:
        active_status_monitor.set_error("No port Specified")
    else:
        server = ServerClass.Server(port)
        if active_status_monitor.get_execution_state() == True:
            print(active_status_monitor.get_output())
            while True: #Iterates to await new connections
                active_status_monitor.clear()
                connection_details = server.accept_connection()
                server.retrieve_data(connection_details)

                # print statments for displaying formatted results of given commmand
                print(f"({connection_details.get_address()[0]}   Port:{connection_details.get_address()[1]}): status: {active_status_monitor.get_status()}, ",end="")
                print(f"command:{active_status_monitor.get_output()}. {active_status_monitor.get_additional_output()}" if active_status_monitor.get_status() == "success" else f"Error: {active_status_monitor.get_error()}" )
                connection_details.get_socket().close()
                
        
            server.get_socket().close()
        else:
            print(active_status_monitor.get_error())
            


main(*sys.argv[1:2])