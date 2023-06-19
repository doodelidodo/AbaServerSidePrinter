# AbaServerSidePrinter
 Da wir mit Abacus Server Side Printing verwenden möchten, haben ich dieses Script geschrieben. Es ist ein eifacher Watcher auf einem Ordner der konfiguriert werden kann.
 Der Watcher checkt in diesem Ordner, ob es eine neue PDF Datei gibt. Wenn ja checkt er, ob es nicht in einem Ignore Folder drin ist und druckt es dann auf dem Drucker aus, der in der Config definiert wurde. Das ganze kann als Windows Dienst registriert werden.

 Die Idee ist es, pro Drucker ein Unterordner zu machen und diesen dann in der Config so zu definieren. So muss man aus dem Abacus nur noch das PDF im richtigen Ordner ablegen, um es auf dem richtigen Drucker zu printen.

 Ist der Druck erfolgreich, wird es in diesem Ordner in den Ordner 'archiv' verschoben. 
 Ist der Druck NICHT erfolgreich, wird es in den Ordner 'error' verschoben


## Das Config File 

**watchFolder** = Welcher Hauptordner soll überwacht werden
**ignoreFolders** = jeder Ordner der so heisst, wird nicht überwacht. Standardmässig die error und archiv Ordner (wichtig, da das ganze ansonsten in ein Endlosloop läuft)
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
Wenn man nicht weiss, wie die Drucker genau heissen, kann mit dem Script **druckerListe** alle Drucker in der Console ausgeben lassen, die mit dem aktuellen PC verbunden sind.
