#include <WiFi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

#define SCAN_TIME 30 // segundos
#define SERIAL_PRINT // comentar essa linha para desabilitar os prints

static              BLEUUID serviceUUID("0000ffe0-0000-1000-8000-00805f9b34fb");
BLEScan             *pBLEScan; // configura e inicia scan BLE
static String       nodo_mac      = "C8:FD:19:07:F2:29";

static char*        ssid          = "duda";
static char*        password      = "duda5743";

static const int    max_counter   = 20; // quantidade de dados de advertising escaneadas
static int          max_time_wait = 4;  // intervalo de advertising
static long int     inicio, fim   = 0;  // controle de timeout para incrementar counter

int32_t  rssi_vector[max_counter] = {0};
uint32_t counter                  = 0;
uint8_t  start                    = 0;

bool WIFI_Connect() {
  WiFi.begin(ssid, password); 
  while (WiFi.status() != WL_CONNECTED) {
    delay(2000);
    #ifdef SERIAL_PRINT
      Serial.println("Conectando com rede Wi-Fi...");
    #endif
  }
  if (WiFi.status() == WL_CONNECTED) {
    #ifdef SERIAL_PRINT
      Serial.println("Conectado, enviando dados dos sensores");
    #endif
    return true;
  } else {
    #ifdef SERIAL_PRINT
      Serial.println("Erro na conexão!");
    #endif
    return false;
  }
}

void HTTP_Post(int rssi, unsigned int counter) {
  StaticJsonBuffer<1000> JSONbuffer;
  JsonObject& JSONencoder = JSONbuffer.createObject();
  
  String gateway_mac         = WiFi.macAddress();
  JSONencoder["gateway_mac"] = gateway_mac;
  JSONencoder["nodo_mac"]    = nodo_mac;
  JSONencoder["rssi"]        = rssi;
  JSONencoder["count"]       = counter;

  char JSONmessageBuffer[1000];
  JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));

  HTTPClient http;

  http.begin("http://192.168.0.13 ':5001/insere_medicao");
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST(JSONmessageBuffer); // envia request

  #ifdef SERIAL_PRINT
    Serial.print("RETORNO http: ");
    Serial.println(httpCode);
  #endif

  http.end();

  if (httpCode == 200) {
    #ifdef SERIAL_PRINT
        Serial.println("DADOS ENVIADOS PARA O BANCO!");
    #endif
  }
  else {
    #ifdef SERIAL_PRINT
        Serial.println("Erro no envio, ignorando dados.");
    #endif
  }
}

void connect_send(){
  if (WIFI_Connect() == false) return;
  for (int i = 0; i < max_counter; i++){
      if (rssi_vector[i] != 0) HTTP_Post(rssi_vector[i], i);    
  }
  WiFi.disconnect();
}

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks{
    void onResult(BLEAdvertisedDevice advertisedDevice){
      if (advertisedDevice.haveServiceUUID() && advertisedDevice.getServiceUUID().equals(serviceUUID)) {
        advertisedDevice.getScan()->stop();
        
        fim                   = millis();
        int atraso            = (fim - inicio)/1000;
        int increment_counter = 1 + atraso/max_time_wait;
        counter               += increment_counter;
        rssi_vector[counter]  = advertisedDevice.getRSSI();

        #ifdef SERIAL_PRINT
          Serial.printf("----------------\n");
          Serial.print("Valor incrementado de counter: ");
          Serial.println(increment_counter);
          Serial.printf("RSSI   : %d\n", advertisedDevice.getRSSI());
          Serial.printf("MAC    : %s\n", advertisedDevice.getAddress().toString().c_str());
          Serial.printf("counter: %d\n", counter);
        #endif
      }
    }
};

void BLE_Init(){
  BLEDevice::init(""); // inicia dispositivo BLE
  pBLEScan = BLEDevice::getScan(); // cria scan BLE
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks()); //confgiura funcao de callback no scan de um beacon
  pBLEScan->setActiveScan(true); //consome mais energia mas oferece scans mais rapidos
  pBLEScan->setInterval(0x50);
  pBLEScan->setWindow(0x30);
}

void BLE_StartScan(){
  pBLEScan->start(SCAN_TIME); // inicia scan BLE durante o periodo de SCAN_TIME 
}

void CheckMeasurements(){
  uint32_t     miss              = 0;
  uint32_t     max_counter_total = max_counter - 1;
  delay(500);
  Serial.printf("----------------\n");
  Serial.println("Vetor de RSSI: ");
  for (int i = 1; i < max_counter; i++){
    Serial.print(i);
    Serial.print(": ");
    Serial.println(rssi_vector[i]);
    miss += (rssi_vector[i] == 0) ? 1 : 0; 
  }
  Serial.printf("----------------\n");
  Serial.print("Num de medidas esperadas : ");
  Serial.println(max_counter_total);
  Serial.print("Num de medidas realziadas: ");
  Serial.println(max_counter_total - miss);
}

void setup(){  
  Serial.begin(115200);
  #ifdef SERIAL_PRINT
    Serial.printf("Iniciando scan BLE durante %d segs...\n", SCAN_TIME);
  #endif
}
void loop(){
  if (counter >= (max_counter-1)){
    #ifdef SERIAL_PRINT
      CheckMeasurements();
    #endif
//    connect_send();
    while (true){}
  }
  
  BLE_Init();
  inicio = millis();
  BLE_StartScan();
}
