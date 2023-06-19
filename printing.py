import win32print


def print_pdf(printer_name, pdf_file_path):
    # Öffne den Drucker
    printer_handle = win32print.OpenPrinter(printer_name)

    try:
        # Erstelle den Druckauftrag
        job_info = {
            "pPrinterName": printer_name,
            "pDataType": "RAW"
        }

        # Öffne das PDF-File
        with open(pdf_file_path, "rb") as file:
            data = file.read()

        # Sende das PDF an den Drucker
        job_id = win32print.StartDocPrinter(printer_handle, 1, ("test", None, "RAW"))
        win32print.StartPagePrinter(printer_handle)
        win32print.WritePrinter(printer_handle, data)
        win32print.EndPagePrinter(printer_handle)
        win32print.EndDocPrinter(printer_handle)

    except Exception as e:
        print(f"Fehler beim Drucken: {e}")

    finally:
        win32print.ClosePrinter(printer_handle)


def get_printer(folder, printers):
    for fol in printers:
        if folder == fol['folder']:
            return fol['printer']