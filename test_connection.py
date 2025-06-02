import serial
import time

# Konstanten
SERIAL_PORT = 'COM4'
BAUD_RATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Verbunden mit {SERIAL_PORT}")
    
    print("\nEmpfange Daten für 10 Sekunden...\n")
    start_time = time.time()
    
    while time.time() - start_time < 10:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            print(f"Empfangen: {line}")
    
    ser.close()
    print("\nTest beendet!")
    
except Exception as e:
    print(f"Fehler: {e}")
