#include <WiFi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

#define SCAN_TIME 120 // segundos
#define SERIAL_PRINT // comentar essa linha para desabilitar os prints

static              BLEUUID serviceUUID("0000ffe0-0000-1000-8000-00805f9b34fb");
BLEScan             *pBLEScan; // configura e inicia scan BLE
static String       nodo_mac      = "C8:FD:19:07:F2:29"; // so pra nao precisar pegar do dispositivo recebido e passar pra ca

static char*        ssid          = "duda";
static char*        password      = "duda5743";

static const int    max_counter   = 100; // quantidade de dados de advertising escaneadas
static int          max_time_wait = 4;  // intervalo de advertising
static long int     inicio, fim   = 0;  // controle de timeout para incrementar counter

uint32_t counter                  = 0;
uint8_t  start                    = 0;
uint8_t  LED                      = 2;
uint32_t increment_counter        = 0;
 
struct adv_data_st{
  int8_t rssi;
  uint32_t counter;  
} adv_data;

bool WIFI_Connect() {
  uint8_t error = 0;
  WiFi.begin(ssid, password);
#ifdef SERIAL_PRINT
  Serial.println("Conectando com rede Wi-Fi...");
#endif
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    if (error >= 8) break;
    error++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    #ifdef SERIAL_PRINT
      Serial.println("Conectado, enviando dados dos sensores");
    #endif
    return true;
  } else {
    #ifdef SERIAL_PRINT
      Serial.println("Erro na conexao, iniciando novo scan...");
    #endif
    return false;
  }
}

void toggle_LED(uint16_t ligado, uint16_t desligado, uint8_t counter_loop){
  uint8_t i = 0;
  do{
    digitalWrite(LED, HIGH);
    delay(ligado);
    digitalWrite(LED, LOW);
    delay(desligado);
    i ++;
  } while(i < counter_loop);
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

int HTTP_GET() {
  HTTPClient http;

  http.begin("http://192.168.0.13 ':5001/dummy_get");
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.GET(); // envia request

  #ifdef SERIAL_PRINT
    Serial.print("RETORNO http: ");
    Serial.println(httpCode);
  #endif

  http.end();
  return httpCode;
}

void connect_send(){
  static long int inicio, fim = 0;
  inicio = millis();
  if (WIFI_Connect() == false){
    WiFi.disconnect();
    return;
  }
  HTTP_Post(adv_data.rssi, adv_data.counter);
  WiFi.disconnect();
  fim               =  millis();
  int atraso        =  (fim - inicio)/1000;
  counter           += atraso/max_time_wait;
}

// funcao chamada no setup para travar todos os gws
// e inicar todos ao mesmo tempo
void dummy_connection(){
  WIFI_Connect();
  while(HTTP_GET() != 200);
  WiFi.disconnect();
}

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks{
    void onResult(BLEAdvertisedDevice advertisedDevice){
      if (advertisedDevice.haveServiceUUID() && advertisedDevice.getServiceUUID().equals(serviceUUID)) {
        advertisedDevice.getScan()->stop();
        
        fim                   = millis();
        int atraso            = (fim - inicio)/1000;
        increment_counter = 1 + atraso/max_time_wait;
        adv_data.counter      = counter += increment_counter;
        adv_data.rssi         = advertisedDevice.getRSSI();
                
        #ifdef SERIAL_PRINT
          Serial.printf("----------------\n");
          Serial.print("Valor incrementado de counter: ");
          Serial.println(increment_counter);
          Serial.printf("RSSI   : %d\n", adv_data.rssi);
          Serial.printf("MAC    : %s\n", advertisedDevice.getAddress().toString().c_str());
          Serial.printf("counter: %d\n", adv_data.counter);
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

void setup(){  
  Serial.begin(115200);
  pinMode(LED, OUTPUT);

  digitalWrite(LED, HIGH);
  dummy_connection();
  digitalWrite(LED, LOW);
  
  #ifdef SERIAL_PRINT
    Serial.printf("Iniciando scan BLE durante %d segs...\n", SCAN_TIME);
  #endif
}

void loop(){
  BLE_Init();
  inicio = millis();
  BLE_StartScan();
  
  //apos retorno da funcao de callback
  connect_send();
//#ifdef SERIAL_PRINT
//  Serial.print("Valor incrementado durante WIFI: ");
//  Serial.println(counter - adv_data.counter);
//  Serial.println("Reiniciando scan BLE...");
//#endif
}
