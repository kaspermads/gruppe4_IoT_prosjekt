#include <WiFi.h>          // Library for wifi
#include <Wire.h>          // Library for I2C communication
#include "wifi_saturasjon.h"          // Include header file
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>   // Library for Json-used to convert data to string
#include <MAX30105.h>      // Library for O2 sensor
#include <spo2_algorithm.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define MAX_BRIGHTNESS 255
#define debug Serial
#define LED 2
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define MAX30105_I2C_ADDRESS 0x57
#define OLED_I2C_ADDRESS     0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32

int patientID = 1;
int serialMillis = 0;
uint32_t irBuffer[100]; //infrared LED sensor data
uint32_t redBuffer[100];  //red LED sensor data
int32_t bufferLength; //data length
int32_t spo2; //SPO2 value
int8_t validSPO2; //indicator to show if the SPO2 calculation is valid
int32_t heartRate; //heart rate value
int8_t validHeartRate; //indicator to show if the heart rate calculation is valid
bool shouldTransmitData;
bool sentData;

MAX30105 particleSensor;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET); //Defines the OLED display settings

 //Add a function that prints self defined string to the OLED display
void displayprint(const char* text)
{
  display.clearDisplay();
    display.setTextSize(1);             // Normal 1:1 pixel scale
    display.setTextColor(SSD1306_WHITE); // Draw white text
    display.setCursor(0,0);             // Start at top-left corner
    display.println(F(text));           //Prints the argument given in the function call to the screen
    display.display();                  //Updates the display
}

//Function to trigger data transmission
void triggerDataTransmission() {
  shouldTransmitData = true;
}

//Function for the actual data transmission
void dataTransmission(){
 if (WiFi.status() == WL_CONNECTED)
  {
    // Create a secure client connection
    WiFiClientSecure client;
    client.setCACert(rootCA); // Set the root CA certificate

    // Connect to the server
    if (client.connect(server, port))
    {
      displayprint("Connected to Server!");

      String url = "api/post_oxygen_saturation_data/"; // The URL to send the data to

      // The JWT token of the esp32handler user, this needs to be automated. The token expires after 5 days.
      // The esp32 handler only has access to post data, not view or edit data which is important for security.
      String token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNDgxNDAyLCJpYXQiOjE3MDAwNDk0MDIsImp0aSI6IjY3Y2M0NWI4YzI1ZDQ5ZjhiY2Q3MTQ2ODA0ODEzMWEyIiwidXNlcl9pZCI6MTB9.A_HCk3eP0qGfAOHirE26ewlxn94uqiQCMSN3Yc4Armc";

      // Send the HTTP POST request
      client.println("POST " + url + " HTTP/1.1");
      client.println("Host: " + String(server));
      client.println("Content-Type: application/json"); // This is important, as it tells the server what kind of data we are sending
      client.println("Authorization: Bearer " + token); // Send the JWT token in the header so that the server accepts the data
      client.println("Connection: close");              // Close the connection after the request is sent

      // Send the JSON data as a single line
      String jsonData = "{\"patient_id\":" + String(patientID) + ", \"oxygen_saturation\":" + String(spo2) + "}";
      client.println("Content-Length: " + String(jsonData.length())); // Send the length of the JSON data so the server knows when the data ends
      client.println();                                               // Empty line between headers and body of the request
      client.println(jsonData);                                       // Send the JSON data

      // Read all the lines of the reply from server and print them to Serial
      while (client.connected())
      {
        // Read the header line
        String line = client.readStringUntil('\n');
        if (line == "\r")
        {
          break;
        }
      }
      // If there are incoming bytes available
      while (client.available())
      {
        // Read incoming bytes until the server closes the connection
        String line = client.readStringUntil('\n');
        Serial.println(line);
      }
      displayprint("Data sent,\ndisconnected.");
    }
    else // If the connection failed
    {
      displayprint("Connection to Server failed!");
    }
  }
  else // If we are not connected to the patients Wi-Fi
  {
    displayprint("WiFi disconnected,\ncheck your internet connection.");
  }
}

void setup() {
  Serial.begin(115200); //Begins serial communication
  Wire.begin();
  pinMode(4,OUTPUT);
  pinMode(21, PULLUP);
  pinMode(22, PULLUP);
  digitalWrite(4, HIGH);

  sentData = false;

    if (!display.begin(0x3C, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;) {
      // Don't proceed, loop forever
    }
  }

  display.display();

  WiFi.begin(ssid, password); //This function connects the unit to the defined network
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    displayprint("Connecting to WiFi...");
  }
    displayprint("Connected to WiFi!");

  if (particleSensor.begin() == false)
  {
    displayprint("MAX30102 was not found.\nPlease check wiring/power.");
    while (1);
  }
   
 if (!particleSensor.begin(Wire, 100000, 0x57)) //Use defined I2C port
  {
    displayprint("MAX30102 was not found.\nPlease check wiring/power.");
    while (1);
  }

  displayprint("Attach sensor to finger with rubber band.\nStarting to read in \n10 seconds.");
  delay(10000);

  byte ledBrightness = 60;
  byte sampleAverage = 4;
  byte ledMode = 2;
  byte sampleRate = 100;
  int pulseWidth = 411;
  int adcRange = 4096;

  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); //Configure sensor with these settings

}

void loop() {

  if(sentData == false){
    bufferLength = 100; //buffer length of 100 stores 4 seconds of samples running at 25sps

    //read the first 100 samples, and determine the signal range
    for (byte i = 0 ; i < bufferLength ; i++)
    {
      while (particleSensor.available() == false) //do we have new data?
        particleSensor.check(); //Check the sensor for new data

      redBuffer[i] = particleSensor.getRed();
      irBuffer[i] = particleSensor.getIR();
      particleSensor.nextSample(); //We're finished with this sample so move to next sample

      //Prints to Serial for troubleshooting of the unit.
      Serial.print(F("red="));
      Serial.print(redBuffer[i], DEC);
      Serial.print(F(", ir="));
      Serial.println(irBuffer[i], DEC);
      displayprint("Reading.");
    }

    //Calculate heart rate and SpO2 after first 100 samples (first 4 seconds of samples)
    maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);

    //Continuously taking samples from MAX30102.  Heart rate and SpO2 are calculated every 1 second
    if (shouldTransmitData) {
      //Dumping the first 25 sets of samples in the memory and shift the last 75 sets of samples to the top
      for (byte i = 25; i < 100; i++) {
        redBuffer[i - 25] = redBuffer[i];
        irBuffer[i - 25] = irBuffer[i];
      }

      //take 25 sets of samples before calculating the heart rate.
      for (byte i = 75; i < 100; i++)
      { 
        while (particleSensor.available() == false) //do we have new data?
          particleSensor.check(); //Check the sensor for new data

        redBuffer[i] = particleSensor.getRed();
        irBuffer[i] = particleSensor.getIR();
        particleSensor.nextSample(); //We're finished with this sample so move to next sample

        //send samples and calculation result to terminal program through UART
        displayprint("Reading.");
        Serial.print(F("red="));
        Serial.print(redBuffer[i], DEC);
        Serial.print(F(", ir="));
        Serial.print(irBuffer[i], DEC);
        Serial.print(F(", HR="));
        Serial.print(heartRate, DEC);
        Serial.print(F(", HRvalid="));
        Serial.print(validHeartRate, DEC);
        Serial.print(F(", SPO2="));
        Serial.print(spo2, DEC);
        Serial.print(F(", SPO2Valid="));
        Serial.println(validSPO2, DEC);
        displayprint("Reading..");
      }

      //After gathering 25 new samples recalculate HR and SP02
      maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2, &validSPO2, &heartRate, &validHeartRate);
    }

      displayprint("Reading.");
      Serial.print(F(", HR="));
      Serial.print(heartRate, DEC);
      Serial.print(F(", HRvalid="));
      Serial.print(validHeartRate, DEC);
      Serial.print(F(", SPO2="));
      Serial.print(spo2, DEC);
      Serial.print(F(", SPO2Valid="));
      Serial.println(validSPO2, DEC);
      displayprint("Reading..");
      if (validSPO2 == 1 && spo2 > 90)
      {
      triggerDataTransmission();
      dataTransmission();
      sentData = true;
      } 
  }
  else
  {
    displayprint("Data has been sent to server. You can now turn off the device.");
  }
    //Reset the flag to prevent continuous transmission
    shouldTransmitData = false;
    display.clearDisplay();
  }

  //Some example code is used from the SPO2 example in this library: https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library