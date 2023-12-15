#include <Keypad.h>             //library for keypad
#include <LiquidCrystal_I2C.h>  //Library for screen
#include <WiFi.h>               // Library for wifi
#include <Wire.h>               // Library for I2C communication
#include "wifi.h"               // Include header file
#include <WiFiClientSecure.h>   //library for sending data to server
#include <ArduinoJson.h>        // Library for Json-used to convert data to string

// set the LCD number of columns and rows
int lcdColumns = 16;
int lcdRows = 2;

bool confirmOnce = true;
bool printed=true;

// set LCD address, number of columns and rows
LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows);

#define ROW_NUM 4     // four rows
#define COLUMN_NUM 4  // four columns

//values of information that is being sent
String systolic;
String diastolic;
String pulse;
//the id of the patient
String patientID = "2";

//where the struct should start
int c = 1;
//representing the digits on the keypad
char keys[ROW_NUM][COLUMN_NUM] = {
  { '1', '2', '3', 'A' },
  { '4', '5', '6', 'B' },
  { '7', '8', '9', 'C' },
  { '*', '0', '#', 'D' }
};

byte pin_rows[ROW_NUM] = { 13, 12, 14, 27 };       // GPIO19, GPIO18, GPIO5, GPIO17 connect to the row pins
byte pin_column[COLUMN_NUM] = { 26, 25, 33, 32 };  // GPIO16, GPIO4, GPIO0, GPIO2 connect to the column pins

Keypad keypad = Keypad(makeKeymap(keys), pin_rows, pin_column, ROW_NUM, COLUMN_NUM);  //making a map of the heys and pins

int serialMillis = 0;  //timer counter





void setup() {
  Serial.begin(9600);  //Begins serial communication
  // initialize LCD
  lcd.init();
  // turn on LCD backlight
  lcd.backlight();
  //setup wifi connection and portrays it to the lcd screen
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("connecting to");
    lcd.setCursor(0, 1);
    lcd.print("WiFi");
  }
  Serial.println("Connected to WiFi");
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("WiFi connected");
}

void sysword(){

lcd.setCursor(0, 0);         // wehere on lcd it should be printed
lcd.print("systolic value:");  // displays the value on screen
char key = keypad.getKey();    // the last button that has been pressed on the keypad
if (key) {                     // if a key has been pressed
  Serial.println(systolic);
  if (key == 'D') {  //if D, delete the saved value to the string
    int indexOfD = systolic.lastIndexOf('D');
    if (indexOfD != -1) {
      systolic.remove(indexOfD);
    } else {
      systolic = " ";
    }
  } else if (!((key == 'A') || (key == 'B') || (key == 'C') || (key == 'D') || (key == '#') || (key == '*'))) {  //if these keys have not been pressed
    systolic += key;                                                                                             //systolic value is the key that have been pressed
    lcd.clear();                                                                                                 //clears the display
    lcd.setCursor(0, 0);
    lcd.print("systolic value:");
    lcd.setCursor(0, 1);
    lcd.print(systolic);

    Serial.println(systolic);  //used for debugging
  }
  if (key == 'C') {   //if C then confirm and continue
    printed = false;  //reset the printing of the next word
    lcd.clear();
    c = 2;  //next in the struct
  }
}
}


void diaword() {

  lcd.setCursor(0, 0);
  lcd.print("diastolic value:");
  char key = keypad.getKey();

  if (key) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(diastolic);
    Serial.println(diastolic);
    if (key == 'D') {  //if d delete the saved value to the string
      int indexOfD = diastolic.lastIndexOf('D');
      if (indexOfD != -1) {
        diastolic.remove(indexOfD);
      } else {
        diastolic = "";
      }
    } else if (!((key == 'A') || (key == 'B') || (key == 'C') || (key == 'D') || (key == '#') || (key == '*'))) {  // if key is not one of these add it to the string
      diastolic += key;
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("diastolic value:");

      lcd.setCursor(0, 1);
      lcd.print(diastolic);
      Serial.println(diastolic);
    }
    if (key == 'C') {  //if C then confirm and continue
      printed = false;
      c = 3;
      lcd.clear();
    }
    if (key == 'B') {  //if B then go back
      c = 1;
    }
  }
}

void pulseword() {  // does the same as diaword

  lcd.setCursor(0, 0);
  lcd.print("pulse value:");
  char key = keypad.getKey();
  if (key) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("pulse value:");
    Serial.println(pulse);
    Serial.println(pulse);
    if (key == 'D') {  //if D, delete the saved value to the string
      int indexOfD = pulse.lastIndexOf('D');
      if (indexOfD != -1) {
        pulse.remove(indexOfD);
      } else {
        pulse = "";
      }
    } else if (!((key == 'A') || (key == 'B') || (key == 'C') || (key == 'D') || (key == '#') || (key == '*'))) {
      pulse += key;
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("pulse value:");
      lcd.setCursor(0, 1);
      lcd.print(pulse);
      Serial.println(pulse);
    }
  }

  if (key == 'C') {  //if C then confirm and continue
    printed = false;
    c = 4;
    lcd.clear();
  }
  if (key == 'B') {  //if B then go back
    c = 2;
  }
}

void checkIfValid() {  // function that checks if the length of the value stored in the string are not inhumanly large or irregularly small, wich will conclude with that the value typed in is wrong
  //this function does not work, dont know why, but is not important as long as values are correctly typed in
  char key = keypad.getKey();
  if ((systolic.length() > 3) || (systolic.length() < 2)) {
    Serial.println('your sys number is invalid, try again');
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("sys invalid");
    lcd.setCursor(0, 1);
    lcd.print("try again");

    c = 1;  // have to write the value anew since it is not valid
  }

  if ((diastolic.length() > 3) || (diastolic.length() < 2)) {
    Serial.println('your dia number is invalid, try again');
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Dia invalid");
    lcd.setCursor(0, 1);
    lcd.print("try again");

    c = 2;  // have to write the value anew since it is not valid
  }

  if ((pulse.length() > 3) || (pulse.length() < 2)) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("pulse invalid");
    lcd.setCursor(0, 1);
    lcd.print("try again");
    Serial.println("your pulse number is invalid, try again");
    c = 3;  // have to write the value anew since it is not valid
  }
  c = 5;
}

void confirmData() {
  char key = keypad.getKey();
  if (confirmOnce = true) {  //
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Values confirmed");
    lcd.setCursor(0, 1);
    lcd.print("C continue");
    confirmOnce = false;

    if (key == 'C') {  // press c for confirm
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Forwarding...");
      dataTransmission();  //starts sending data
    }
  }
}
void check() {

  switch (c) {
    case 1:

      sysword();

      break;

    case 2:

      diaword();

      break;

    case 3:

      pulseword();

      break;

    case 4:
      checkIfValid();

      break;

    case 5:

      confirmData();

      break;

    case 6:
      //new test press B
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("B: for");
      lcd.setCursor(0, 1);
      lcd.print("new test");
      char key = keypad.getKey();
      if (key == 'B') {
        diastolic = "";
        systolic = "";
        pulse = "";
        c = 1;
      }
  }
}

void loop() {


  check();
}


void dataTransmission() {
  if (WiFi.status() == WL_CONNECTED) {
    // Create a secure client connection
    WiFiClientSecure client;
    client.setCACert(rootCA);  // Set root CA certificate aka the token


    if (client.connect(server, port))  // Connect to the server

    {
      Serial.println("Connected to server!");
      String url = "/api/post_blood_pressure_data/";  // The URL to send the data to


      // The etoken used to get connection to the server
      String token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyNzI0ODE4LCJpYXQiOjE3MDIyOTI4MTgsImp0aSI6IjYzODM2M2E3ZWE3MjQ4NzI4ZDU2MzlmZTBlYmViOWQ1IiwidXNlcl9pZCI6MTB9.fxj6Ecnxa8xD-S9FzhzU7bDNWCihCSTdWA7c6MT59oU";


      client.println("POST " + url + " HTTP/1.1");  // Send the HTTP POST request
      client.println("Host: " + String(server));
      client.println("Content-Type: application/json");  // This is important, as it tells the server what kind of data we are sending, json format
      client.println("Authorization: Bearer " + token);  // Send the token in the header so that the server accepts the data
      client.println("Connection: close");               // Close the connection after the request is sent

      // Send the JSON data as a single line
      String jsonData = "{\"patient_id\":" + String(patientID) + ", \"systolic\":" + String(systolic) + ", \"diastolic\":" + String(diastolic) + ", \"pulse\":" + String(pulse) + "}";
      client.println("Content-Length: " + String(jsonData.length()));  // Send the length of the data so the server knows when the data ends
      client.println();                                                // Empty line between headers and body of the request
      client.println(jsonData);                                        // Send the JSON data

      // Read all the lines of the reply from server and print them to Serial
      while (client.connected()) {
        // Read the header line
        String line = client.readStringUntil('\n');
        if (line == "\r") {
          Serial.println("Headers");
          break;
        }
      }
      // If there are incoming bytes available
      while (client.available()) {
        // Read incoming bytes until the server closes the connection
        String line = client.readStringUntil('\n');
        Serial.println(line);
      }
      client.stop();
      Serial.println("disconnected");
    } else  // If the connection failed
    {
      Serial.println("Connection to website failed");
    }
  } else  // If we are not connected to the patients Wi-Fi
  {
    Serial.println("WiFi Disconnected");
  }

  c = 6;
}


//https://esp32io.com/tutorials/esp32-keypad
//https://randomnerdtutorials.com/esp32-esp8266-i2c-lcd-arduino-ide/
//https://github.com/espressif/arduino-esp32/blob/master/libraries/WiFiClientSecure/examples/WiFiClientSecure/WiFiClientSecure.ino
//https://randomnerdtutorials.com/esp32-https-requests/
