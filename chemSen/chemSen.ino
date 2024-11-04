// ESP32 Code: Read analog data and send via Serial

const int sensorPin = A1;           // Use any ADC1 GPIO pin (e.g., GPIO 34)
const float referenceVoltage = 5;  // Reference voltage for conversion
const int adcResolution = 1023;      // 12-bit ADC resolution
int sensorValue = 0;                 // Variable to store the analog reading

void setup() {
  Serial.begin(115200);              // Start serial communication at 115200 baud
  pinMode(sensorPin, INPUT);         // Set the sensor pin as input
}

void loop() {
  sensorValue = analogRead(sensorPin);  // Read the analog value
  float voltage = convertToVoltage(sensorValue);  // Convert to voltage

  printSensorData(sensorValue, voltage);  // Print the raw value and voltage to Serial

  delay(100);  // 100ms delay between readings
}

// Function to convert ADC value to voltage
float convertToVoltage(int value) {
  return value * (referenceVoltage / adcResolution);
}

// Function to print sensor data to Serial
void printSensorData(int rawValue, float voltage) {
  Serial.print("Raw Value: ");
  Serial.print(rawValue);
  Serial.print("\tVoltage: ");
  Serial.println(voltage, 4);  // Print voltage with 4 decimal places
}
