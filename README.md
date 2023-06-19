# AbaServerSidePrinter
Unser Abacus Server Side Printing Skript ermöglicht eine effiziente Druckautomatisierung. Der Watcher überwacht einen konfigurierbaren Ordner auf neue PDF-Dateien. Nach Prüfung auf relevante Unterordner druckt das Skript die Dateien auf den definierten Druckern. Erfolgreich gedruckte Dateien werden in den "Archiv"-Ordner verschoben, während fehlerhafte Ausdrucke in den "Error"-Ordner wandern. Dieses Skript kann als Windows-Dienst registriert werden, um kontinuierlichen Betrieb zu gewährleisten. Eine elegante Lösung für effizientes und problemloses Drucken.


## Das Config File 

**watchFolder** = Welcher Hauptordner soll überwacht werden <br>
**ignoreFolders** = jeder Ordner der so heisst, wird nicht überwacht. Standardmässig die error und archiv Ordner (wichtig, da das Ganze ansonsten in einen Endlosloop läuft) <br>
**printers** = pro Ordner braucht es einen Eintrag. Hier wird definiert, auf welchem Drucker das File dann geprintet werden muss. 

```watchFolder = C:/Users/medo/Documents/coding/AbaServPrinting/Test
ignoreFolders = ["error", "archiv"]
printers = [
    {
        "folder": "printer1",
        "printer": "\\\\SRV74\\FollowMe_SW"
    }]
```

## Printer Liste
Wenn man nicht weiss, wie die Drucker genau heissen, kann man mit dem Script **druckerListe.py** alle Drucker in der Console ausgeben lassen, die mit dem aktuellen PC verbunden sind.

## Logging
In einem fix definierten Ordner werden die Logs pro Tag für 7 Tage gespeichert. Man sieht welche Files gedruckt und verschoben werden konnten und welche in Error's gelaufen sind.
