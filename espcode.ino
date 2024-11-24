#include <Arduino.h>
#include <WiFi.h>               // For ESP32
#include <Firebase_ESP_Client.h>

// Provide the token generation process info.
#include "addons/TokenHelper.h"
// Provide the RTDB payload printing info and other helper functions.
#include "addons/RTDBHelper.h"

// Insert your network credentials
#define WIFI_SSID "ROCKSTAR"
#define WIFI_PASSWORD "1234567890"

// Insert Firebase project API Key
#define API_KEY "AIzaSyCPJkx4VP3JcATqa2RlEm2nMNp8v0Gw4Jc"

// Insert RTDB URL
#define DATABASE_URL "https://smart-bin-afa36-default-rtdb.asia-southeast1.firebasedatabase.app/" 

// Define Firebase Data object
FirebaseData fbdo;

FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
bool signupOK = false;

// Define pins for the ultrasonic sensors
#define TRIG_PIN_1 5  // TRIG pin for the first sensor
#define ECHO_PIN_1 18 // ECHO pin for the first sensor
#define TRIG_PIN_2 19 // TRIG pin for the second sensor
#define ECHO_PIN_2 21 // ECHO pin for the second sensor

void setupUltrasonicPins() {
  pinMode(TRIG_PIN_1, OUTPUT);
  pinMode(ECHO_PIN_1, INPUT);
  pinMode(TRIG_PIN_2, OUTPUT);
  pinMode(ECHO_PIN_2, INPUT);
}

float measureDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  float distance = (duration * 0.0343) / 2; // Convert to centimeters
  return distance;
}

void setup() {
  Serial.begin(115200);
  setupUltrasonicPins();

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  // Assign the Firebase credentials
  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;

  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("Firebase sign-up OK");
    signupOK = true;
  } else {
    Serial.printf("Firebase sign-up failed: %s\n", config.signer.signupError.message.c_str());
  }

  config.token_status_callback = tokenStatusCallback;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop() {
  float distance1 = measureDistance(TRIG_PIN_1, ECHO_PIN_1);
  float distance2 = measureDistance(TRIG_PIN_2, ECHO_PIN_2);

  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 1000 || sendDataPrevMillis == 0)) {
    sendDataPrevMillis = millis();

    // Store Distance1 in Firebase
    if (Firebase.RTDB.setFloat(&fbdo, "Ultrasonic_Sensor/Sensor1", distance1)) {
      Serial.print("Distance from Sensor1: ");
      Serial.println(distance1);
    } else {
      Serial.println("Failed to store Sensor1 data");
      Serial.println("Reason: " + fbdo.errorReason());
    }

    // Store Distance2 in Firebase
    if (Firebase.RTDB.setFloat(&fbdo, "Ultrasonic_Sensor/Sensor2", distance2)) {
      Serial.print("Distance from Sensor2: ");
      Serial.println(distance2);
    } else {
      Serial.println("Failed to store Sensor2 data");
      Serial.println("Reason: " + fbdo.errorReason());
    }
  }
}
