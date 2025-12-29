const int LED_PIN = 13;

void setup() {
  Serial.begin(9600); 
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW); 
}
void loop() {
  if (Serial.available() > 0) {
    char incomingCommand = Serial.read();
    if (incomingCommand == 'T') {
      digitalWrite(LED_PIN, HIGH); 
      Serial.println("LED ON");
    } 
    else if (incomingCommand == 'F') {
      digitalWrite(LED_PIN, LOW); 
      Serial.println("LED OFF");
    }
  }
}
