import cups 
import os

class PrinterManager:
    def __init__(self, printer_name="SELPHY"):
        self.printer_name = printer_name
        self.conn = None
        self._connect()

    def _connect(self):
        try:
            # CUPS = common unix printing system - the standard Linux print server
            self.conn = cups.Connection()
            printers = self.conn.getPrinters()
            if self.printer_name not in printers:
                raise ValueError(f"Printer '{self.printer_name}' not found. Available printers: {list(printers.keys())}")
            else:
                print(f"Connected to printer: {self.printer_name}")
        except Exception as e:
            print(f"Failed to connect to CUPS: {e}")
            self.conn = None

    def print_file(self, file_path):
        if not os.path.isfile(file_path):
            print(f"File '{file_path}' does not exist.")
            return False

        if not self.conn:
            self._connect()
            if not self.conn:
                print("Not connected to CUPS. Cannot print.")
                return False

        try:
            options = {
                "media": "Postcard",
                "fit-to-page": "true"
            }

            job_id = self.conn.printFile(
                self.printer_name,
                file_path,
                "Photobooth Print",
                options
            )
            print(f"Print job submitted with ID: {job_id}")
            return True
        except Exception as e:
            print(f"Failed to print file {e}")
            return False