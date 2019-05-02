#define SCAN_TIME 30 // seconds

// comment the follow line to disable serial message
#define SERIAL_PRINT

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

static BLEUUID serviceUUID("0000ffe0-0000-1000-8000-00805f9b34fb");
static int max_counter = 50;
static int max_time_wait = 4;
static long int inicio, fim = 0;

int32_t rssi_vector[100] = {0};

uint32_t counter = 0;

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks{
    void onResult(BLEAdvertisedDevice advertisedDevice){
      if (advertisedDevice.haveServiceUUID() && advertisedDevice.getServiceUUID().equals(serviceUUID)) {
        advertisedDevice.getScan()->stop();
        
        fim = millis();
        int atraso = (fim - inicio)/1000;
        int increment_counter = 1 + atraso/max_time_wait;
        counter += increment_counter;

        Serial.print("Valor incrementado de counter: ");
        Serial.println(increment_counter);
        
        rssi_vector[counter] = advertisedDevice.getRSSI();
        #ifdef SERIAL_PRINT
          Serial.printf("----------------\n");
          Serial.printf("RSSI: %d\n", advertisedDevice.getRSSI());
          Serial.printf("counter: %d\n", counter);
        #endif
      }
    }
};

void setup(){  
  Serial.begin(115200);
  #ifdef SERIAL_PRINT
    Serial.printf("Start BLE scan for %d seconds...\n", SCAN_TIME);
  #endif
}
void loop(){
  if (counter == (max_counter - 1)){
    #ifdef SERIAL_PRINT
      Serial.println("Vetor de RSSI: ");
      for (int i = 0; i < counter; i++){
        Serial.print(i);
        Serial.print(": ");
        Serial.println(rssi_vector[i]);   
      }
    #endif
    while (true){}
  }
  
  BLEDevice::init("");
  
  BLEScan *pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(0x50);
  pBLEScan->setWindow(0x30);
  
  inicio = millis();
  BLEScanResults foundDevices = pBLEScan->start(SCAN_TIME); //start scan
}
