#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import time
import sys
import platform  # Zum Erkennen des Betriebssystems
from PIL import Image
import pygame
import configparser  # Importieren von configparser
from logging.handlers import RotatingFileHandler
import logging

script_path = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_path, "playMyPi.log")
playlist_path = os.path.join(script_path, "playlist.txt")
enable_logging = 0
max_run_time = 10
chromium_path = ""
stop_event = False

def setup_logging():
    """
    Set up logging configuration.

    Returns:
        logger (logging.Logger): The logger object.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=1)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def run():
    """
    Run the main program.

    This function reads the playlist file, processes the lines, and performs actions based on the line content.
    """
    global max_run_time, chrome_path, stop_event
    start_time = time.time()

    try:
        with open(playlist_path, "r") as file:
            lines = file.readlines()
            log_message(f"Anzahl der Zeilen in der Datei: {len(lines)}", "info")
            usable_lines = [line for line in lines if line.strip() and len(line.split('|')[0]) >= 3 and int(line.split('|')[1]) >= 5]
            if len(usable_lines) > 0:
                while True:  # Startet die Endlosschleife
                    current_time = time.time()
                    if max_run_time > 0 and (current_time - start_time) > max_run_time:
                        logger.info("Maximale Laufzeit erreicht. Das Skript wird beendet.", "info")
                        break
                    if stop_event: # Wenn die ESC-Taste gedrückt wird (stop_event = True) (def check_for_esc)
                        logger.info("Das Skript wird beendet.", "info")
                        break
                    for line in usable_lines:
                        line = line.strip()
                        title, duration = line.split('|')
                        duration = int(duration)
                        log_message(f"Titel: {title}, Dauer: {duration} Sekunden", "info")
                        # schwarzen Bildschirm anzeigen
                        display_black_screen(0.5)
                        if title.startswith("http://") or title.startswith("https://"):
                            open_chromium(title, duration)
                        elif title.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                            display_image_fullscreen(title, duration)
                        else:
                            log_message(f"Titel: {title}, Dauer: {duration} Sekunden", "info")

    except FileNotFoundError:
        log_message("Die Datei 'playlist.txt' wurde nicht gefunden.", "error")
    except ValueError as e:
        log_message(f"Fehler beim Verarbeiten der Datei: {e}", "error")

    sys.exit()

def display_image_fullscreen(image_path, duration):
    """
    Display an image in fullscreen.

    Args:
        image_path (str): The path to the image file.
        duration (int): The duration in seconds to display the image.
    """
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    img = Image.open(image_path)
    img = img.resize(screen.get_size(), Image.Resampling.LANCZOS)
    img_surf = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
    screen.blit(img_surf, (0, 0))
    pygame.display.flip()
    time.sleep(duration)
    pygame.quit()

def open_chromium(url, duration):
    """
    Open Chromium browser and display a URL or close it.

    Args:
        url (str): The URL to open in Chromium.
        duration (int): The duration in seconds to keep Chromium open.
    """
    global chromium_path
    if platform.system() == "Windows":
        log_message(f"Windows erkannt; {chromium_path}; Url: {url}", "info")
        subprocess.Popen([chromium_path, '--kiosk', url])
    else:
        # Für Linux/Raspbian
        log_message(f"Linux erkannt; Url: {url}", "info")
        subprocess.Popen(['chromium-browser', '--kiosk', url])
    time.sleep(duration)
    # Vor dem Schließen des Browsers schwarzen Bildschirm anzeigen
    display_black_screen(0.5)
    if platform.system() == "Windows":
        os.system('taskkill /IM chrome.exe /F')  # Chromium-Prozess auf Windows beenden
    else:
        os.system('pkill -o chromium-browser')  # Chromium-Prozess auf Linux/Raspbian beenden

def read_config():
    """
    Read the configuration from the ini file.

    Returns:
        max_run_time (int): The maximum run time in seconds.
        chrome_path (str): The path to the Chromium executable.
    """
    global enable_logging, max_run_time, chromium_path
    ini_path = os.path.join(script_path, "playMyPi.ini")
    config = configparser.ConfigParser()
    config.read(ini_path)
    max_run_time = int(config['DEFAULT'].get('max_run_time', 0)) * 60  # Konvertiert Minuten in Sekunden
    chromium_path = config['DEFAULT'].get('chrome_path', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
    enable_logging = int(config['DEFAULT'].get('enable_logging', 0))
    return 1

def check_chromium():
    """
    Check if Chromium is configured and available.

    Returns:
        int: 1 if Chromium is configured and available, 0 otherwise.
    """
    global chromium_path
    if platform.system() == "Windows":
        if chromium_path:
            log_message("Chromium path found in the ini file.", "info")
            if os.path.exists(chromium_path):
                log_message("Chromium is configured and available.", "info")
                return 1
            else:
                log_message(f"Chromium is configured but not available ({chromium_path}).", "error")
                return 0
        else:
            log_message("Chromium path not found in the ini file.", "error")
            return 0
    else:
        log_message("This function is only applicable for Windows.", "info")
        return 1

def log_message(message, log_type):
    """
    Log a message.

    Args:
        message (str): The message to log.
        log_type (str): The type of log message (error, info, warning).
    """
    global enable_logging
    logger = logging.getLogger()
    if enable_logging == True or enable_logging == 1:
        if log_type == "error":
            logger.error(message)
        elif log_type == "info":
            logger.info(message)
        else:
            logger.warning("Invalid log type specified.")
    print(f"[{log_type.upper()}] {message}")

def display_black_screen(duration=1):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill((0, 0, 0))  # Füllt den Bildschirm mit Schwarz
    pygame.display.flip()
    check_for_esc(duration)  # Wie lange der schwarze Bildschirm angezeigt wird
    pygame.quit()

def check_for_esc(duration):
    global stop_event
    start_time = time.time()
    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                stop_event = True
        time.sleep(0.1)  # Kurze Pause, um CPU-Nutzung zu reduzieren

if __name__ == '__main__':
    pygame.init()  # Initialisieren von pygame
    read_config()
    logger = setup_logging()
    log_message("Programm gestartet", "info")
    if check_chromium():
        run()
    pygame.quit()  # Stellen Sie sicher, dass pygame ordnungsgemäß beendet wird
