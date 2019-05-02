#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

#define SCAN_TIME 30 // segundos
#define SERIAL_PRINT // comente essa linha para desabilitar os prints

static BLEUUID serviceUUID("0000ffe0-0000-1000-8000-00805f9b34fb");

static char*  ssid          = "daniel";
static char*  password      = "v3gLNNK9";

static String nodo_mac      = "00:15:85:14:9c:09";
static String gateway_mac   = WiFi.macAddress();


static int    max_counter   = 50; // quantidade de dados de advertising escaneadas
static int    max_time_wait = 4;  // intervalo de advertising
static long int inicio, fim = 0;  // controle de timeout para incrementar counter

int32_t rssi_vector[max_counter]    = {0};
uint32_t counter                    = 0;


bool connect_wifi() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(2000);
    #ifdef SERIAL_PRINT
      Serial.println("Conectando com rede Wi-Fi...");
    #endif
  }
  if (WiFi.status() == WL_CONNECTED) {
    IPAddress ip;
    ip = WiFi.localIP();

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

void send_data(int32_t rssi, uint32_t counter) {
  StaticJsonBuffer<1000> JSONbuffer;   //Declaring static JSON buffer
  JsonObject& JSONencoder = JSONbuffer.createObject();

  JSONencoder["gateway_mac"] = gateway_mac;
  JSONencoder["nodo_mac"]    = nodo_mac;
  JSONencoder["rssi"]        = rssi
  JSONencoder["count"]       = counter;

  char JSONmessageBuffer[1000];
  JSONencoder.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));

  HTTPClient http;

  http.begin("http://192.168.0.14 ':5001/insere_medicao");
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST(JSONmessageBuffer);   //Send the request

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

void send_data(){
  connect_wifi();
  for (int i = 0; i < max_counter; i++){
      if (rssi_vector[i] != 0) send_data(rssi_vector[i], i);    
  }
  WiFi.disconnect();
}

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks{
    void onResult(BLEAdvertisedDevice advertisedDevice){
      if (advertisedDevice.haveServiceUUID() && advertisedDevice.getServiceUUID().equals(serviceUUID)) {
        advertisedDevice.getScan()->stop();
        fim = millis();
        
        int atraso            = (fim - inicio)/1000;
        int increment_counter = 1 + atraso/max_time_wait;
        counter               += increment_counter;
        rssi_vector[counter]  = advertisedDevice.getRSSI();
                
        #ifdef SERIAL_PRINT
          Serial.printf("----------------\n");
          Serial.print("Valor incrementado de counter: ");
          Serial.println(increment_counter);
          Serial.printf("RSSI   : %d\n", advertisedDevice.getRSSI());
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
  if (counter == (max_counter)){
    #ifdef SERIAL_PRINT
      Serial.println("Vetor de RSSI: ");
      for (int i = 0; i < counter; i++){
        Serial.print(i);
        Serial.print(": ");
        Serial.println(rssi_vector[i]);   
      }
    #endif
//    send_data();
    while (true){}
  }
  
  BLEDevice::init("");
  
  BLEScan *pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(0x50);
  pBLEScan->setWindow(0x30);
  
  inicio                      = millis();
  BLEScanResults foundDevices = pBLEScan->start(SCAN_TIME); //start scan
}
