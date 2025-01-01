from datetime import datetime

class writer:
        _directory = None
        _filename = None
        _name = None
        def __init__(self,directory,filename,name):
                self._filename = filename
                self._directory = directory
                self._name = name
        def logs(self,text):
                now = datetime.now()
                log_file = self._directory + "/" + self._filename + ".log"
                log_date = now.strftime("%m-%d-%Y %H:%M:%S %p")
                log = open(log_file, "a")  # append mode
                log.write("{}:{} - {}\n".format(log_date,self._name,text))
                log.close()
