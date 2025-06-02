import pandas as pd
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 2:
    print("Benutzung: python visualize_data.py <csv_datei>")
    sys.exit(1)

filename = sys.argv[1]

try:
    # CSV-Datei laden
    df = pd.read_csv(filename)
    print(f"Datei geladen: {filename}")
    print(f"Anzahl Zeilen: {len(df)}")
    print(f"Spalten: {list(df.columns)}")
    
    if len(df) == 0:
        print("Die Datei ist leer!")
        sys.exit(1)
    
    # Erste paar Zeilen anzeigen
    print("\nErste 5 Zeilen:")
    print(df.head())
    
    # Überprüfen ob die erwarteten Spalten vorhanden sind
    if 'Timestamp' in df.columns:
        # Verwende die Original-Spaltennamen
        time_col = 'Timestamp'
        acc_x_col = 'Acc_X'
        acc_y_col = 'Acc_Y'
        acc_z_col = 'Acc_Z'
        gyro_x_col = 'Gyro_X'
        gyro_y_col = 'Gyro_Y'
        gyro_z_col = 'Gyro_Z'
    else:
        # Verwende generische Spaltennamen
        print("\nHinweis: Keine Header gefunden, verwende generische Spaltennamen")
        print("Annahme: Col0=Timestamp, Col1=Acc_X, Col2=Acc_Y, Col3=Acc_Z, Col4=Gyro_X, Col5=Gyro_Y, Col6=Gyro_Z")
        
        # Spalten umbenennen für bessere Lesbarkeit
        df.columns = ['Timestamp', 'Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z']
        
        time_col = 'Timestamp'
        acc_x_col = 'Acc_X'
        acc_y_col = 'Acc_Y'
        acc_z_col = 'Acc_Z'
        gyro_x_col = 'Gyro_X'
        gyro_y_col = 'Gyro_Y'
        gyro_z_col = 'Gyro_Z'
    
    # Konvertiere Timestamp zu Sekunden (von Millisekunden)
    df['Time_sec'] = df[time_col] / 1000.0
    
    # Visualisierung
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Beschleunigungssensor
    ax1.plot(df['Time_sec'], df[acc_x_col], label='X', alpha=0.7)
    ax1.plot(df['Time_sec'], df[acc_y_col], label='Y', alpha=0.7)
    ax1.plot(df['Time_sec'], df[acc_z_col], label='Z', alpha=0.7)
    ax1.set_ylabel('Beschleunigung (raw)')
    ax1.set_title('Beschleunigungssensor')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Gyroskop
    ax2.plot(df['Time_sec'], df[gyro_x_col], label='X', alpha=0.7)
    ax2.plot(df['Time_sec'], df[gyro_y_col], label='Y', alpha=0.7)
    ax2.plot(df['Time_sec'], df[gyro_z_col], label='Z', alpha=0.7)
    ax2.set_ylabel('Winkelgeschwindigkeit (raw)')
    ax2.set_xlabel('Zeit (s)')
    ax2.set_title('Gyroskop')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Statistiken ausgeben
    print("\n=== Statistiken ===")
    print(f"Aufnahmedauer: {df['Time_sec'].iloc[-1] - df['Time_sec'].iloc[0]:.1f} Sekunden")
    print(f"Anzahl Datenpunkte: {len(df)}")
    print(f"Durchschnittliche Abtastrate: {len(df) / (df['Time_sec'].iloc[-1] - df['Time_sec'].iloc[0]):.1f} Hz")
    
except Exception as e:
    print(f"Fehler: {e}")
    import traceback
    traceback.print_exc()
