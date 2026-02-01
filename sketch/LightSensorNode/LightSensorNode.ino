// ---- Pin definitions ----
const int LDR_PIN = A0;
const int LED_PIN = 8;

// ---- Timing ----
unsigned long lastSend = 0;
const unsigned long intervalMs = 1000;   // 1 second telemetry

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);   // LED OFF by default

  Serial.begin(9600);
  delay(500);                   // allow serial to stabilise

  // Node startup message
  Serial.println("NODE=sam,STATUS=ready");
}

void loop() {
  unsigned long now = millis();

  // ---- Periodic telemetry (non-blocking) ----
  if (now - lastSend >= intervalMs) {
    lastSend = now;

    int lightValue = analogRead(LDR_PIN);

    // Standardised, self-describing payload
    Serial.print("NODE=sam,SENSOR=ldr,VALUE=");
    Serial.println(lightValue);
  }

  // ---- Command handling (bidirectional) ----
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // Acknowledge received command (useful for demo/debug)
    Serial.print("NODE=sam,ACK=");
    Serial.println(cmd);

    if (cmd == "LED=ON") {
      digitalWrite(LED_PIN, HIGH);
    }
    else if (cmd == "LED=OFF") {
      digitalWrite(LED_PIN, LOW);
    }
  }
}
