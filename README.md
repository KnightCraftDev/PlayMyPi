# PlayMyPi Projekt

## Überblick

Das PlayMyPi Projekt ist ein Python-Skript, das eine Playliste von Medieninhalten automatisch abspielt. Es liest eine Playlist-Datei, verarbeitet jede Zeile und führt Aktionen basierend auf dem Inhalt jeder Zeile aus. Das Skript ist flexibel konzipiert, um mit verschiedenen Medienformaten und Abspielzeiten zu arbeiten.

## Funktionen

- **Playlist-Verarbeitung:** Das Skript liest eine Playlist-Datei, die Medientitel und deren Dauer enthält. Jede Zeile der Datei repräsentiert ein Medienelement in der Form `Titel|Dauer`.
- **Zeitgesteuerte Ausführung:** Die maximale Laufzeit des Skripts kann konfiguriert werden. Das Skript beendet sich selbst, wenn die festgelegte maximale Laufzeit erreicht ist.
- **Notstopp:** Das Skript kann jederzeit gestoppt werden, wenn ein bestimmtes Ereignis eintritt (z.B. das Drücken der ESC-Taste).

## Voraussetzungen

- Python 3.x
- Zugriff auf eine Playlist-Datei im spezifizierten Format.

## Installation

1. Klonen Sie das Repository oder laden Sie die Quelldateien herunter.
2. Stellen Sie sicher, dass Python 3.x auf Ihrem System installiert ist.
3. Platzieren Sie Ihre Playlist-Datei (`playlist.txt`) im selben Verzeichnis wie das Skript oder geben Sie den Pfad zur Datei im Skript an.

## Benutzung

Um das Skript zu starten, öffnen Sie ein Terminal oder eine Kommandozeile und führen Sie den Befehl aus:

```bash
python playMyPi.py
```
Stellen Sie sicher, dass Sie den Pfad zur Playlist-Datei im Skript korrekt angegeben haben.

## Konfiguration
**max_run_time**: Legt die maximale Laufzeit des Skripts in Sekunden fest. Standardmäßig auf 0 gesetzt, was bedeutet, dass das Skript unendlich läuft, bis es manuell gestoppt wird.
**chrome_path**: Der Pfad zum Chrome/Chromium-Browser.
**enable_logging**: Wenn der Wert 1 ist, wird die Bildschirmausgabe zusätzlich in eine log-Datei geschrieben.

Hierzu lohnt sich ein Blick in die `playMyPi.example.ini`. Diese Datei kopieren und als `playMyPi.ini` im selben Pfad speichern und den eigenen Wünschen anpassen.

## Lizenz
Dieses Projekt ist unter der MIT Lizenz veröffentlicht. Weitere Informationen finden Sie in der LICENSE-Datei.

## Beitrag
Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder eröffnen Sie ein Issue, wenn Sie Verbesserungen vorschlagen möchten.

## Kontakt
Für Fragen und Anregungen können Sie ein Issue im GitHub-Repository eröffnen. 