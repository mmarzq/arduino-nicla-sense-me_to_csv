#include "Arduino_BHY2.h"

// Sensoren definieren
SensorXYZ accelerometer(SENSOR_ID_ACC);
SensorXYZ gyroscope(SENSOR_ID_GYRO);

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);
  
  // BHY2 initialisieren
  BHY2.begin();
  
  // Sensoren starten
  accelerometer.begin();
  gyroscope.begin();
  
  // CSV Header senden
  Serial.println("Timestamp,Acc_X,Acc_Y,Acc_Z,Gyro_X,Gyro_Y,Gyro_Z");
}

void loop() {
  // Sensordaten aktualisieren
  BHY2.update();
  
  // CSV Format: Timestamp,Wert1,Wert2,Wert3...
  Serial.print(millis());  // Timestamp in Millisekunden
  Serial.print(",");
  Serial.print(accelerometer.x());
  Serial.print(",");
  Serial.print(accelerometer.y());
  Serial.print(",");
  Serial.print(accelerometer.z());
  Serial.print(",");
  Serial.print(gyroscope.x());
  Serial.print(",");
  Serial.print(gyroscope.y());
  Serial.print(",");
  Serial.println(gyroscope.z());
  
  delay(50);
}