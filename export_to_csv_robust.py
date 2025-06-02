import serial
import csv
import time
from datetime import datetime
import sys

# Konstanten
SERIAL_PORT = 'COM4'  # Für Windows
# SERIAL_PORT = '/dev/cu.usbmodem14101'  # Für Mac
BAUD_RATE = 115200
TIMEOUT = 1
RECORDING_DURATION = 30  # Sekunden
STARTUP_DELAY = 2  # Sekunden

try:
    # Serial Port konfigurieren
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"Verbunden mit {SERIAL_PORT}")
except Exception as e:
    print(f"Fehler beim Öffnen der seriellen Verbindung: {e}")
    sys.exit(1)

# CSV-Datei erstellen
filename = f"sensordaten_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

print("Warte auf Arduino...")
time.sleep(STARTUP_DELAY)  # Arduino Zeit zum Starten geben

print(f"Starte {RECORDING_DURATION}-Sekunden-Aufzeichnung...")
print("Drücken Sie Ctrl+C zum vorzeitigen Beenden...")
start_time = time.time()

try:
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Header Flag
        header_written = False
        lines_written = 0
        
        while time.time() - start_time < RECORDING_DURATION:
            if ser.in_waiting:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    
                    if line:
                        # Debug: Zeige empfangene Zeile
                        print(f"Empfangen: {line}")
                        
                        # Daten parsen
                        data = line.split(',')
                        
                        # Header schreiben wenn noch nicht geschehen
                        if not header_written:
                            if "Timestamp" in line:
                                csv_writer.writerow(data)
                                header_written = True
                                print("Header geschrieben!")
                            else:
                                # Wenn kein Header kommt, erstelle einen
                                header = [f"Col{i}" for i in range(len(data))]
                                csv_writer.writerow(header)
                                header_written = True
                                # Schreibe auch die erste Datenzeile
                                csv_writer.writerow(data)
                                lines_written += 1
                        else:
                            # Normale Datenzeile
                            if "Timestamp" not in line:  # Überspringe wiederholte Header
                                csv_writer.writerow(data)
                                lines_written += 1
                        
                        # Wichtig: Buffer leeren
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
tutu