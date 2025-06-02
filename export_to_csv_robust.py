import serial
import csv
import time
from datetime import datetime
import sys
import os       # für Ordner-operation

# Konstanten
SERIAL_PORT = 'COM4'  # Für Windows
# SERIAL_PORT = '/dev/cu.usbmodem14101'  # Für Mac
BAUD_RATE = 115200
TIMEOUT = 1
RECORDING_DURATION = 30  # Sekunden
STARTUP_DELAY = 3  # Sekunden (erhöht für bessere Synchronisation)
# DATA  from arduino
HEADER = ['Timestamp', 'Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z']
DATA_LENGTH = 7

try:
    # Serial Port konfigurieren
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"Verbunden mit {SERIAL_PORT}")
except Exception as e:
    print(f"Fehler beim Öffnen der seriellen Verbindung: {e}")
    sys.exit(1)

# Stelle sicher, dass das data/ Verzeichnis existiert
os.makedirs('data', exist_ok=True)
# CSV-Datei im Ordner "data" erstellen
filename = f"data/sensordaten_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

print("Warte auf Arduino...")
# Erstmal ein paar Zeilen verwerfen, um sicherzustellen, dass wir frische Daten bekommen
for _ in range(10):
    if ser.in_waiting:
        ser.readline()

time.sleep(STARTUP_DELAY)   # Arduino Zeit zum Starten geben

print(f"Starte {RECORDING_DURATION}-Sekunden-Aufzeichnung...")
print("Drücken Sie Ctrl+C zum vorzeitigen Beenden...")
start_time = time.time()

try:
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Header explizit schreiben
        header = HEADER
        csv_writer.writerow(header)

        lines_written = 0
        
        while time.time() - start_time < RECORDING_DURATION:
            if ser.in_waiting:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    
                    if line and not line.startswith("Timestamp"):  # Header überspringen
                        # Debug: Zeige empfangene Zeile
                        print(f"Empfangen: {line}")

                        # Daten parsen
                        data = line.split(',')
                        
                        if len(data) == DATA_LENGTH:  # Nur vollständige Zeilen
                            csv_writer.writerow(data)
                            lines_written += 1
                            
                            # Buffer leeren
                            csvfile.flush()
                        
                except UnicodeDecodeError as e:
                    print(f"Dekodierungsfehler: {e}")
                    continue
                except Exception as e:
                    print(f"Fehler beim Verarbeiten der Zeile: {e}")
                    continue
        
        print(f"\n{lines_written} Datenzeilen geschrieben!")
        
except KeyboardInterrupt:
    print("\nAufzeichnung durch Benutzer beendet!")
except Exception as e:
    print(f"Fehler während der Aufzeichnung: {e}")
finally:
    ser.close()
    print(f"Datei gespeichert als: {filename}")
    print("\nZum Visualisieren:")
    print(f"python visualize_data.py {filename}")
