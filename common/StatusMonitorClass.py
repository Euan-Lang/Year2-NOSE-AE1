import string

# status monitor class used to keep track of output and any errors that can be outputed to client and server separately

class StatusMonitor:
    _status = ""
    _output = ""
    _additonal_output =""
    _errorMsg =""
    _continue_execution = True

    def set_status(self,status):
        self._status = status

    def set_output(self,output):
        self._output = output

    def break_execution(self):
        self._continue_execution = False

    def set_additonal_output(self,additional_output):
        self._additonal_output = additional_output

    def set_error(self,error_msg):
        self._errorMsg = error_msg
        self.set_status("Failure")
        self.break_execution()

    def get_status(self):
        return self._status

    def get_output(self):
        return self._output

    def get_additional_output(self):
        return self._additonal_output

    def get_error(self):
        return self._errorMsg

    def get_execution_state(self):
        return self._continue_execution

    def clear(self):
        self._status = ""
        self._output = ""
        self._additonal_output =""
        self._errorMsg =""
        self._continue_execution = True


active_status_monitor = StatusMonitor()
