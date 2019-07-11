#include <WiFi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

#define SCAN_TIME 600 // segundos
//#define SERIAL_PRINT // comentar essa linha para desabilitar os prints

static              BLEUUID serviceUUID("0000ffe0-0000-1000-8000-00805f9b34fb");
BLEScan             *pBLEScan; // configura e inicia scan BLE
static String       nodo_mac      = "C8:FD:19:07:F2:29"; // so pra nao precisar pegar do dispositivo recebido e passar pra ca

static char*        ssid          = "dd-wrt";
static char*        password      = "";

static const uint16_t    max_counter   = 400; // quantidade de dados de advertising escaneadas
static int               max_time_wait = 2;  // intervalo de advertising
static long int          inicio, fim   = 0;  // controle de timeout para incrementar counter

int8_t   rssi_vector[max_counter] ={0};
uint32_t counter                  = 0;
uint8_t  start                    = 0;
uint8_t  LED                      = 2;
int      increment_counter        = 0;
uint32_t miss                     = 0;

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
    String gateway_mac = WiFi.macAddress();
    Serial.print("GW MAC: ");
    Serial.println(gateway_mac);
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
//  Serial.print("GW MAC: ");
//  Serial.println(gateway_mac);
  JSONencoder["gateway_mac"] = gateway_mac;
  JSONencoder["nodo_mac"]    = nodo_mac;
  JSONencoder["rssi"]        = rssi;
  JSONencoder["count"]       = counter;

  char JSONmessageBuffer[1000];
  JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));

  HTTPClient http;

  http.begin("http://192.168.1.108 ':5001/insere_medicao");
  http.addHeader("Content-Type", "application/json");

  while(http.POST(JSONmessageBuffer) == 400);
  
  http.end();
}

int HTTP_GET() {
  HTTPClient http;
  
  http.begin("http://192.168.1.108 ':5001/dummy_get");
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
  delay(2000);
  if (WIFI_Connect() == false) return;
  for (int i = 0; i <= max_counter; i++){
      if (rssi_vector[i] != 0) HTTP_Post(rssi_vector[i], i);    
  }
  WiFi.disconnect();
}

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
  miss = 0;
  delay(500);
#ifdef SERIAL_PRINT
  Serial.printf("----------------\n");
  Serial.println("Vetor de RSSI: ");
#endif
  for (int i = 1; i <= max_counter; i++){
#ifdef SERIAL_PRINT
    Serial.print(i);
    Serial.print(": ");
    Serial.println(rssi_vector[i]);
#endif
    miss += (rssi_vector[i] == 0) ? 1 : 0;
  }
#ifdef SERIAL_PRINT
  Serial.printf("----------------\n");
  Serial.print("Num de medidas esperadas : ");
  Serial.println(max_counter);
  Serial.print("Num de medidas realziadas: ");
  Serial.println(max_counter - miss);
#endif
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
  if (counter >= max_counter){
    CheckMeasurements();

    digitalWrite(LED, HIGH);
    connect_send();
    digitalWrite(LED, LOW);
    while (true) toggle_LED(250,250, 0);  
  }
  
  BLE_Init();
  inicio = millis();
  BLE_StartScan();
}
