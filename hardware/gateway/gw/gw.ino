#define SCAN_TIME  10 // seconds

// comment the follow line to disable serial message
#define SERIAL_PRINT

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

#include <WiFi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

static char* ssid           = "duda";
static char* password       = "duda5743";
static bool  device_scanned = false;
int counter = 0;

struct adv_data_st{
//  const char * nodo_mac;
//  int    rssi;
    BLEAdvertisedDevice advertisedDevice;

}adv_data;

static BLEUUID serviceUUID("0000ffe0-0000-1000-8000-00805f9b34fb");

bool connect_wifi(){
    WiFi.begin(ssid, password); 
  
    while (WiFi.status() != WL_CONNECTED) { //Check for the connection
      delay(2000);
      #ifdef SERIAL_PRINT
        Serial.println("Conectando com rede Wi-Fi...");
      #endif
    }
    if(WiFi.status() == WL_CONNECTED){
      IPAddress ip;
      ip = WiFi.localIP();
      
      #ifdef SERIAL_PRINT
        Serial.println("Conectado, enviando dados dos sensores");
        Serial.print("IP GW: ");
        Serial.println(ip);
      #endif
      return true;
    }else{
      #ifdef SERIAL_PRINT
        Serial.println("Erro na conexão!");
      #endif
      return false;
    }
}

void send_data(){  
    StaticJsonBuffer<1000> JSONbuffer;   //Declaring static JSON buffer
    JsonObject& JSONencoder = JSONbuffer.createObject();

    String gateway_mac = WiFi.macAddress();
    
    #ifdef SERIAL_PRINT
//      Serial.println("GATEWAY_MAC: ");
//      Serial.println(gateway_mac);
    #endif

    JSONencoder["gateway_mac"] = gateway_mac;
    JSONencoder["nodo_mac"] = String(adv_data.advertisedDevice.getAddress().toString().c_str());
    JSONencoder["rssi"] = int(adv_data.advertisedDevice.getRSSI());
    JSONencoder["count"] = counter;
        
    char JSONmessageBuffer[1000];
    JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));

    HTTPClient http;
    
    http.begin("http://192.168.0.13:5001/insere_medicao");
    http.addHeader("Content-Type", "application/json");

    int httpCode = http.POST(JSONmessageBuffer);   //Send the request

    #ifdef SERIAL_PRINT
      Serial.print("RETORNO http: ");
      Serial.println(httpCode);
    #endif
    
    http.end();
    
    if (httpCode == 200){
      #ifdef SERIAL_PRINT
        Serial.println("DADOS ENVIADOS PARA O BANCO!");
      #endif
      counter++;
    }
    else {
      #ifdef SERIAL_PRINT
        Serial.println("Erro no envio, ignorando dados.");
      #endif
    }
}

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks{
    void onResult(BLEAdvertisedDevice advertisedDevice){
      if (advertisedDevice.haveServiceUUID() && advertisedDevice.getServiceUUID().equals(serviceUUID)) {
//        advertisedDevice.getScan()->stop();

        adv_data.advertisedDevice = advertisedDevice;
//        adv_data.nodo_mac = advertisedDevice.getAddress().toString().c_str();
//        adv_data.rssi = advertisedDevice.getRSSI();
        
        #ifdef SERIAL_PRINT
          Serial.printf("-------------------------------\n");
          Serial.printf("Advertised Device: %s\n", advertisedDevice.getName().c_str());
          Serial.printf("Address: %s\n", advertisedDevice.getAddress().toString().c_str());
          Serial.printf("RSSI: %d\n", advertisedDevice.getRSSI());
        #endif
        device_scanned = true;
        advertisedDevice.getScan()->stop();
      }
    }
};

void setup(){

  #ifdef SERIAL_PRINT
    Serial.begin(115200);
    Serial.println("ESP32 BLE Scanner");
  #endif
  BLEDevice::init("");
}
void loop(){
  #ifdef SERIAL_PRINT
    Serial.printf("-------------------------------\n");
    Serial.printf("Start BLE scan for %d seconds...\n", SCAN_TIME);
  #endif
  
//  BLEDevice::init("");
  
  BLEScan *pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(0x50);
  pBLEScan->setWindow(0x30);
  
  BLEScanResults foundDevices = pBLEScan->start(SCAN_TIME); //start scan

  if (device_scanned){
    connect_wifi();
    send_data();
    WiFi.disconnect();
    device_scanned = false;
  }
  
  #ifdef SERIAL_PRINT
    Serial.println("Scan done!");
  #endif
}
