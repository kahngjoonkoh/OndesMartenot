int sensorPin = A0;    // select the input pin for the potentiometer
int ledPin = 13;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor
int speakerPin = 3;
float knobPerimeter = 4.5;  // 4.5cm
float keyboardLength = 60;  // 60cm
float lengthPerNote = keyboardLength/50;
float maxAngle = 3600;  // 10 Turns
float maxRawInput = 1024;  // 1024 for Arduino Uno
int startFrequency = 110;  // A2


void setup() {
  Serial.begin(9600);
  pinMode(sensorPin, INPUT);
  pinMode(speakerPin, OUTPUT);
}

void loop() {
  sensorValue = analogRead(sensorPin);
  int frequency = getFrequency(getDistance(getAngle(sensorValue)));
  tone(speakerPin, frequency);
  Serial.println(String(sensorValue)+" "+String(frequency));
}

float getAngle(int rawInput){
  return float(rawInput)/maxRawInput*maxAngle;
}

float getDistance(float a){
  return a/float(360) * knobPerimeter;
}

int getFrequency(float d){
  float n = d/lengthPerNote;
  return int(startFrequency * pow(2, n/12));
}
