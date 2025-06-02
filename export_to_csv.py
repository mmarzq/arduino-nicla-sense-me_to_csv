import serial
import csv
import time
from datetime import datetime

# Konstanten
SERIAL_PORT = 'COM4'  # Für Windows
# SERIAL_PORT = '/dev/cu.usbmodem14101'  # Für Mac
BAUD_RATE = 115200
TIMEOUT = 1
RECORDING_DURATION = 30  # Sekunden
STARTUP_DELAY = 2  # Sekunden

# Serial Port konfigurieren
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)

# CSV-Datei erstellen
filename = f"sensordaten_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

print("Warte auf Arduino...")
time.sleep(STARTUP_DELAY)  # Arduino Zeit zum Starten geben

print(f"Starte {RECORDING_DURATION}-Sekunden-Aufzeichnung...")
start_time = time.time()

with open(filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Header überspringen oder schreiben
    first_line = True
    
    while time.time() - start_time < RECORDING_DURATION:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                if first_line and "Timestamp" in line:
                    # Header schreiben
                    csv_writer.writerow(line.split(','))
                    first_line = False
                    csvfile.flush()  # Sofort in Datei schreiben
                elif not first_line and "Timestamp" not in line:
                    # Datenzeile schreiben
                    csv_writer.writerow(line.split(','))
                    csvfile.flush()  # Sofort in Datei schreiben
                    
                print(line)  # Zur Kontrolle

print(f"\nAufzeichnung beendet! Datei gespeichert als: {filename}")
ser.close()