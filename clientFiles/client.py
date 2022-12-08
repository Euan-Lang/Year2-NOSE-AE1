from pydoc import cli
import sys
import os
#alteration to execution pathing allowing for python files to be seperated in folders 
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(ROOT_DIR)

import ClientClass 
from common.StatusMonitorClass import active_status_monitor


def main(host=None,port=None,command=None,file=None):
    active_status_monitor.clear()
    client = ClientClass.Client()
    client.connection_details(host,port)
    client.establish_connection()
    if active_status_monitor.get_execution_state()== True:
        client.send_data(command,file)
        if active_status_monitor.get_execution_state()== True:
            client.retrieve_data()
    client.close_connection()
    # print statments for displaying formatted results of given commmand
    print(f"({client.get_address()}   Port:{client.get_port()}): status: {active_status_monitor.get_status()}, ",end="")
    print(f"command:{active_status_monitor.get_output()}.{active_status_monitor.get_additional_output()}" if active_status_monitor.get_status() == "success" else f"Error: {active_status_monitor.get_error()}" )

    



main(*sys.argv[1:])
