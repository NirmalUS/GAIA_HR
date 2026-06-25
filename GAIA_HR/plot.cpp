#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>

const unsigned int localUdpPort = 12345;

char packetBuffer[255];
WiFiUDP udp;

float ReceiverValue[] = {1500, 1000, 1500, 1500, 0, 0, 0, 0};
int ChannelNumber = 0;

// Failsafe
unsigned long lastPrintTime = 0;
unsigned long lastPacketTime = 0;
const unsigned long FAILSAFE_TIMEOUT = 500;
bool isConnected = false;


void read_receiver(void){
  // IP address 192.168.4.1
  int packetsize = udp.parsePacket();
  bool  newDatareceived = false;
  
  if (packetsize > 0){
    while (packetsize > 0){
      int len = udp.read(packetBuffer, 255);
      if (len > 0){
        packetBuffer[len] = 0;
      }
      packetsize = udp.parsePacket();
    }
    int val1 = 0, val2 = 0, val3 = 0, val4 = 0;
    int parsedItems = sscanf(packetBuffer, "%4d%4d%4d%4d", &val1, &val2, &val3, &val4);

    if (parsedItems == 4){
      ReceiverValue[0] = val1; // Yaw
      ReceiverValue[1] = val2; // Throttle
      ReceiverValue[2] = val3; // Roll
      ReceiverValue[3] = val4; // Pitch
    
      newDatareceived = true;
      isConnected = true;
      lastPacketTime = millis();
    }
  }

  if (newDatareceived && (millis() - lastPrintTime > 100)){
    Serial.print(">CH1:");
    Serial.print(ReceiverValue[0]);

    Serial.print(">CH2:");
    Serial.print(ReceiverValue[1]);

    Serial.print(">CH3:");
    Serial.print(ReceiverValue[2]);

    Serial.print(">CH4:");
    Serial.println(ReceiverValue[3]);

    lastPrintTime = millis();
  }
}

void radio_failsafe(){
  if (isConnected && (millis() - lastPacketTime > FAILSAFE_TIMEOUT)){
    ReceiverValue[0] = 1500;
    ReceiverValue[1] = 1000;
    ReceiverValue[2] = 1500;
    ReceiverValue[3] = 1500;

    isConnected = false;
    digitalWrite(21, LOW);
  }
  if (isConnected){
    digitalWrite(21, HIGH);
  }
}


void setup() {
  Serial.begin(115200);
  pinMode(21, OUTPUT);
  digitalWrite(21, HIGH);

  WiFi.mode(WIFI_AP);
  WiFi.disconnect();
  delay(100);

  if (WiFi.softAP(ssid, password)){
    Serial.println("AP Created");
  }
  else{
    Serial.println("AP creation failed");
    digitalWrite(21, LOW);
  }

  // Begin UDP listening
  udp.begin(localUdpPort);

  delay(2000);
}

void loop() {
  read_receiver();
  radio_failsafe();

  delay(10);
}
