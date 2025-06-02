import pandas as pd
import numpy as np

def convert_sensor_data(filename):
    """
    Konvertiert Arduino Nicla Sense ME Rohdaten in physikalische Einheiten
    """
    # Daten laden
    df = pd.read_csv(filename)
    
    # Falls keine Header vorhanden, Spalten umbenennen
    if 'Col0' in df.columns:
        df.columns = ['Timestamp', 'Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z']
    
    # Konvertierung zu physikalischen Einheiten
    # Diese Werte sind Schätzungen - überprüfen Sie die Arduino_BHY2 Dokumentation für genaue Werte
    
    # Accelerometer: Annahme ±4g Bereich mit 16-bit Auflösung
    ACC_SCALE = 4.0 / 32768.0  # g pro LSB
    df['Acc_X_g'] = df['Acc_X'] * ACC_SCALE
    df['Acc_Y_g'] = df['Acc_Y'] * ACC_SCALE
    df['Acc_Z_g'] = df['Acc_Z'] * ACC_SCALE
    
    # Gyroscope: Annahme ±2000°/s Bereich mit 16-bit Auflösung
    GYRO_SCALE = 2000.0 / 32768.0  # °/s pro LSB
    df['Gyro_X_dps'] = df['Gyro_X'] * GYRO_SCALE
    df['Gyro_Y_dps'] = df['Gyro_Y'] * GYRO_SCALE
    df['Gyro_Z_dps'] = df['Gyro_Z'] * GYRO_SCALE
    
    # Zeit in Sekunden
    df['Time_sec'] = df['Timestamp'] / 1000.0
    df['Time_sec'] -= df['Time_sec'].iloc[0]  # Start bei 0
    
    return df

# Beispielnutzung
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        df = convert_sensor_data(sys.argv[1])
        print("Daten konvertiert!")
        print(df[['Time_sec', 'Acc_X_g', 'Acc_Y_g', 'Acc_Z_g', 'Gyro_X_dps', 'Gyro_Y_dps', 'Gyro_Z_dps']].head())
        
        # Speichern
        output_file = sys.argv[1].replace('.csv', '_converted.csv')
        df.to_csv(output_file, index=False)
        print(f"Konvertierte Daten gespeichert als: {output_file}")
