const int greenLED = 4;
const int redLED   = 5;
const int buzzer   = 18;

enum State {
  NORMAL,
  WARNING,
  CRITICAL
};

State currentState = NORMAL;
State validatedState = NORMAL;

unsigned long previousMillis = 0;
bool ledState = LOW;

// ⭐⭐⭐⭐⭐ CRITICAL TIMER
unsigned long drowsyStartTime = 0;
bool drowsyTimerRunning = false;

const unsigned long CRITICAL_CONFIRM_TIME = 650;//0.65s

void setup() {
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(buzzer, OUTPUT);

  Serial.begin(9600);
}

void loop() {

  // ✅ RECEIVE SERIAL DATA
  if (Serial.available()) {
    char received = Serial.read();

    if (received == 'A') {
      currentState = NORMAL;
      drowsyTimerRunning = false;
    }

    else if (received == 'W') {
      currentState = WARNING;
      drowsyTimerRunning = false;
    }

    else if (received == 'D') {
      currentState = CRITICAL;
    }
  }

  unsigned long currentMillis = millis();

  // ✅ VALIDATE CRITICAL ⭐⭐⭐⭐⭐
  if (currentState == CRITICAL) {

    if (!drowsyTimerRunning) {
      drowsyStartTime = currentMillis;
      drowsyTimerRunning = true;
    }

    if (currentMillis - drowsyStartTime >= CRITICAL_CONFIRM_TIME) {
      validatedState = CRITICAL;
    }

  } else {
    validatedState = currentState;
    drowsyTimerRunning = false;
  }

  // ✅ OUTPUT LOGIC
  switch (validatedState) {

    case NORMAL:
      digitalWrite(greenLED, HIGH);
      digitalWrite(redLED, LOW);
      digitalWrite(buzzer, LOW);
      break;

    case WARNING:
      digitalWrite(greenLED, LOW);
      digitalWrite(buzzer, LOW);

      if (currentMillis - previousMillis >= 800) {
        previousMillis = currentMillis;
        ledState = !ledState;
        digitalWrite(redLED, ledState);
      }
      break;

    case CRITICAL:
      digitalWrite(greenLED, LOW);
      digitalWrite(buzzer, HIGH);

      if (currentMillis - previousMillis >= 250) {
        previousMillis = currentMillis;
        ledState = !ledState;
        digitalWrite(redLED, ledState);
      }
      break;
  }
}