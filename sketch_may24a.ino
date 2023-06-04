
void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(9600);
}

void loop() {
  // Read the voltage from your sensor
  float voltage = analogRead(A0) * (5.0 / 1023.0);
  
  // Get the current time
  unsigned long currentTime = micros();
  
 Serial.print(currentTime);
  Serial.print(",");
  Serial.println(voltage, 4); 
  delayMicroseconds(1000000 / 400);
}
