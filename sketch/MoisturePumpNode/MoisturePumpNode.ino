#include <LiquidCrystal.h>

// LCD pins: RS, E, D4, D5, D6, D7
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

const int moisturePin = A0;
const int pumpPin = 8;

// Calibration (adjust!)
const int dryValue = 1023;
const int wetValue = 350;

// --------------------
// Pump control functions
// --------------------
void pumpOn() {
  digitalWrite(pumpPin, HIGH);
}

void pumpOff() {
  digitalWrite(pumpPin, LOW);
}

void setup() {
  Serial.begin(9600);

  pinMode(pumpPin, OUTPUT);
  pumpOff(); // safety default

  lcd.begin(16, 2);
  lcd.print("Soil Monitor");
  delay(1500);
  lcd.clear();
}

void loop() {
  // ---- Read moisture ----
  int raw = analogRead(moisturePin);
  int moisture = map(raw, dryValue, wetValue, 0, 100);
  moisture = constrain(moisture, 0, 100);

  // ---- LCD ----
  lcd.setCursor(0, 0);
  lcd.print("Moisture: ");
  lcd.print(moisture);
  lcd.print("%   ");

  lcd.setCursor(0, 1);
  lcd.print("Raw: ");
  lcd.print(raw);
  lcd.print("    ");

  // ---- Serial output (Python reads this) ----
  Serial.print("MOISTURE=");
  Serial.println(moisture);

  // ---- Check for incoming commands ----
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "PUMP_ON") {
      pumpOn();
    }
    else if (cmd == "PUMP_OFF") {
      pumpOff();
    }
  }

  delay(1000);
}
