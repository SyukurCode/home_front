from datetime import datetime
import os

class Writer:
    def __init__(self, directory, filename, name):
        self._directory = directory
        self._filename = filename
        self._name = name

    def logs(self, text):
        now = datetime.now()
        
        # Semak dan buat direktori jika tidak wujud
        if not os.path.isdir(self._directory):
            os.makedirs(self._directory, exist_ok=True)

        # Gunakan os.path.join() supaya lebih selamat
        log_file = os.path.join(self._directory, self._filename + ".log")
        log_date = now.strftime("%m-%d-%Y %H:%M:%S %p")

        # Gunakan with open() supaya fail ditutup secara automatik
        with open(log_file, "a") as log:
            log.write(f"{log_date}:{self._name} - {text}\n")
