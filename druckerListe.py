import win32print


def get_available_printers():
    printers = []
    printer_info = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)

    for printer in printer_info:
        printers.append(printer[2])

    return printers


# Beispielaufruf
available_printers = get_available_printers()
for printer in available_printers:
    print(printer)
