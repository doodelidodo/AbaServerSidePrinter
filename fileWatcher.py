import os
import json
import logging
import pythoncom
import win32serviceutil
import win32event
import win32service
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import configparser
import shutil
from printing import get_printer, print_pdf

CONFIG = r'C:\Users\doodelidodo\PycharmProjects\AbaServerSidePrinter\AbaServPrinting.cfg'
LOGS_FOLDER = r'C:\Users\doodelidodo\PycharmProjects\AbaServerSidePrinter\logs'

if not os.path.exists(LOGS_FOLDER):
    os.makedirs(LOGS_FOLDER)

# Konfiguriere das Logging
log_file = os.path.join(LOGS_FOLDER, 'service.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file
)
logger = logging.getLogger()

parser = configparser.ConfigParser()
parser.read(CONFIG, encoding='utf-8')

WATCH_FOLDER = parser.get('Default', 'watchFolder')
IGNORE_FOLDERS = parser.get('Default', 'ignoreFolders')
PRINTERS = json.loads(parser.get('Default', 'printers'))


def move_file(source_file, destination_folder):
    # Überprüfen, ob der Zielordner existiert, andernfalls anlegen
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Datei in den Zielordner verschieben
    shutil.move(source_file, destination_folder)


def should_ignore(folder_name):
    return folder_name.lower() in IGNORE_FOLDERS


class FolderWatcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = os.path.normpath(event.src_path)
        if should_ignore(os.path.basename(os.path.dirname(file_path))):
            return

        if file_path.lower().endswith(".pdf"):
            folder_name = os.path.basename(os.path.dirname(file_path))
            try:
                printer = get_printer(folder_name, PRINTERS)
                print_pdf(printer, file_path)
                move_file(file_path, os.path.dirname(file_path) + "/archiv")
                logger.info(f"PDF-Datei gedruckt und verschoben: {file_path}")
            except:
                move_file(file_path, os.path.dirname(file_path) + "/error")
                logger.error(f"Fehler beim Drucken und Verschieben der PDF-Datei: {file_path}")


class AbaServPrintingService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'AbaServPrintingService'
    _svc_display_name_ = 'AbaServ Printing Service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.observer = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if self.observer:
            self.observer.stop()
            self.observer.join()

    def SvcDoRun(self):
        observer = Observer()
        event_handler = FolderWatcher()
        observer.schedule(event_handler, WATCH_FOLDER, recursive=True)
        observer.start()

        self.ReportServiceStatus(win32service.SERVICE_RUNNING)

        while True:
            pythoncom.PumpWaitingMessages()
            if win32event.WaitForSingleObject(self.hWaitStop, 0) == win32event.WAIT_OBJECT_0:
                observer.stop()
                observer.join()
                break


if __name__ == '__main__':
    if os.name == 'nt':
        if hasattr(win32serviceutil, 'HandleCommandLine'):
            win32serviceutil.HandleCommandLine(AbaServPrintingService)
        else:
            logging.error("Das 'pywin32' Paket ist erforderlich, um den Dienst zu installieren.")
    else:
        logging.error("Der Dienst kann nur unter Windows ausgeführt werden.")
