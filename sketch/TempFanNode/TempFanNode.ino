#include <DHT.h>
#include <LiquidCrystal.h>

const int rs = 12, en = 11, d4 = 7, d5 = 6, d6 = 5, d7 = 4;

#define DHT_Type DHT11

int DHT_Pin = 2;
int Fan_Pin = 3;
int temp_threshold = 30;

DHT HT(DHT_Pin, DHT_Type);
LiquidCrystal LCD(rs, en, d4, d5, d6, d7);

bool isFahrenheit = false;
unsigned long lastReadTime = 0;
const long interval = 2000;

void setup() {
  Serial.begin(9600);
  HT.begin();
  LCD.begin(16, 2);
  
  pinMode(Fan_Pin, OUTPUT); 
}

void lcd_loop(float h, float t) {
  LCD.setCursor(0, 0);

 LCD.clear(); 
 LCD.print("Humidity: ");
 LCD.print(h);
 LCD.print("%");
 LCD.setCursor(0,1);
 LCD.print("Temp: ");
 LCD.print(t);
 LCD.print(isFahrenheit ? "F" : "C");
}

void loop() {
  unsigned long currentMillis = millis();


  if (currentMillis - lastReadTime >= interval) {
    lastReadTime = currentMillis;
    float h = HT.readHumidity();
    float t = HT.readTemperature(isFahrenheit);

    
    if (!isnan(h) && !isnan(t)) {
      Serial.print(h);
      Serial.print(",");
      Serial.print(t);
      Serial.print(",");
      Serial.println(temp_threshold);
      lcd_loop(h, t);
    }
  }

  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '3') digitalWrite(Fan_Pin, LOW);
    if (command == '4') digitalWrite(Fan_Pin, HIGH);
    if (command == '6') {
      temp_threshold -= 1;
    }
    if (command == '5') {
      temp_threshold += 1;
    }
  }
}