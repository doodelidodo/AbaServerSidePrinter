import os
import json
import logging
from logging.handlers import TimedRotatingFileHandler
from warnings import catch_warnings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import configparser
import shutil
from printing import get_printer, print_pdf

CONFIG = r'C:\Users\medo\Documents\coding\AbaServPrinting\AbaServerSidePrinter\AbaServPrinting.cfg'
LOGS_FOLDER = r'C:\Users\medo\Documents\coding\AbaServPrinting\AbaServerSidePrinter\logs'  

if not os.path.exists(LOGS_FOLDER):
    os.makedirs(LOGS_FOLDER)

# Konfiguriere das Logging
log_file = os.path.join(LOGS_FOLDER, 'service.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        TimedRotatingFileHandler(log_file, when='midnight', backupCount=7)
    ]
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


# Wurzelordner und Unterordner, die überwacht werden sollen
root_folder = WATCH_FOLDER

# Erstelle den Observer und weise den EventHandler zu
observer = Observer()
event_handler = FolderWatcher()

# Füge den Observer hinzu und starte die Überwachung
observer.schedule(event_handler, root_folder, recursive=True)
observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()

observer.join()
