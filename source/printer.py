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
            return None

        if not self.conn:
            self._connect()
            if not self.conn:
                print("Not connected to CUPS. Cannot print.")
                return None

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
            return job_id
        except Exception as e:
            print(f"Failed to print file {e}")
            return None

    def _humanize_reason(self, reason):
        # e.g. "media-empty-error" -> "Media Empty"
        text = reason
        for suffix in ("-error", "-warning"):
            if text.endswith(suffix):
                text = text[: -len(suffix)]
                break
        return text.replace("-", " ").title()

    def get_job_status(self, job_id):
        """Returns (state, message) where state is 'printing', 'done', or 'error'."""
        try:
            if not self.conn:
                self._connect()
                if not self.conn:
                    return "error", "Lost connection to printer"

            attrs = self.conn.getJobAttributes(job_id)
            job_state = attrs.get("job-state")

            if job_state == cups.IPP_JOB_COMPLETED:
                return "done", ""

            if job_state in (cups.IPP_JOB_PENDING, cups.IPP_JOB_HELD, cups.IPP_JOB_PROCESSING):
                return "printing", ""

            # IPP_JOB_STOPPED / IPP_JOB_CANCELED / IPP_JOB_ABORTED
            message = attrs.get("job-printer-state-message") or ""
            if not message:
                reasons = attrs.get("job-printer-state-reasons") or []
                if isinstance(reasons, str):
                    reasons = [reasons]
                reasons = [r for r in reasons if r and r != "none"]
                if reasons:
                    message = ", ".join(self._humanize_reason(r) for r in reasons)
            if not message:
                message = "Printer error"
            return "error", message
        except Exception as e:
            print(f"Failed to get job status: {e}")
            return "error", "Lost connection to printer"