#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <BLEServer.h>
#include <BLE2902.h>
#include <Bounce2.h>

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
BLECharacteristic* phoneCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/
int connectedClients = 0;
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#define CHARACTERISTIC_UUIDPhone "beb5483e-36e1-4688-b7f5-ea07361b26b9"

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      if (connectedClients >= 2 ){
        Serial.println("Odbijen treći klijent! Limit je 2 uredjaja.");
        pServer->disconnect(pServer->getConnId());
        return;
      }
      
      connectedClients ++;
      deviceConnected = true;
        
      if (connectedClients == 1){
        Serial.println("Prvi uređaj je uspešno povezan!");
      } else if (connectedClients == 2){
          Serial.println("Drugi uređaj je isto uspešno povezan!");
          BLEDevice::getAdvertising()->stop();
      } 
    };

    void onDisconnect(BLEServer* pServer) {
      if (connectedClients > 0){
          connectedClients--;
      }

      deviceConnected = (connectedClients > 0);
    }
};
#define VRX_PIN  4
#define VRY_PIN  2
#define Button_PIN 21

int xValue= 0;
int yValue= 0;
int buttonState= 0;
int currentState;  
int lastState = HIGH; 
Bounce taster = Bounce();

unsigned long zadnje_vreme_pomeraja = 0;
const int pauza_izmedju_koraka = 200;
static int poslednji_broj_klijenata = -1;
bool prvo_pokretanje = true;

bool spreman_za_pomeraj = true;


void proveri_joystick() {
            int x = analogRead(VRX_PIN);
            int y = analogRead(VRY_PIN);
            currentState = digitalRead(Button_PIN);

            if (millis() - zadnje_vreme_pomeraja > pauza_izmedju_koraka){
              bool registrovano = false;

            

              if (x < 500 ) {
                Serial.println("LEVO");
                registrovano=true;
                std::string LEVO = "LEVO"; 
                pCharacteristic->setValue(LEVO.c_str());
                pCharacteristic->notify();
              } 
              else if (x > 3500){
                Serial.println("DESNO");
                registrovano=true;
                std::string DESNO = "DESNO"; 
                pCharacteristic->setValue(DESNO.c_str());
                pCharacteristic->notify();
              }else if (y < 500){
                Serial.println("GORE");
                registrovano=true;
                std::string GORE = "GORE"; 
                pCharacteristic->setValue(GORE.c_str());
                pCharacteristic->notify();
              }else if (y > 3500){
                Serial.println("DOLE");
                registrovano=true;
                std::string DOLE = "DOLE"; 
                pCharacteristic->setValue(DOLE.c_str());
                pCharacteristic->notify();
              }else{
                registrovano=true;
                std::string DOLE = "SREDINA"; 
                pCharacteristic->setValue(DOLE.c_str());
                pCharacteristic->notify();
              }
                if (lastState == LOW && currentState == HIGH) {
              Serial.println("TASTER");
              std::string DUGME = "TASTER";
              pCharacteristic->setValue(DUGME.c_str()); 
              pCharacteristic->notify();
               }
               lastState =currentState;

              if (registrovano) {
                zadnje_vreme_pomeraja = millis();
              }

            } 
            
            if (x > 1500 && x < 2500  && y > 1500 && y < 2500) {
              
              zadnje_vreme_pomeraja = 0;
            }
}


void setup() {
  Serial.begin(115200);

  delay(5000);

  Serial.println("BLE se pokreće!");
  delay(1000);

  taster.attach(Button_PIN, INPUT_PULLUP);
  taster.interval(25);

  BLEDevice::init("Slovarica");
  pServer = BLEDevice::createServer();
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pServer->setCallbacks(new MyServerCallbacks());


  // Create a BLE Characteristic
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_WRITE  |
                      BLECharacteristic::PROPERTY_NOTIFY |
                      BLECharacteristic::PROPERTY_INDICATE
                    );
  phoneCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUIDPhone,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_WRITE  |
                      BLECharacteristic::PROPERTY_NOTIFY |
                      BLECharacteristic::PROPERTY_INDICATE
                    );
  BLE2902 *pBLE2902;
  pBLE2902 = new BLE2902();
  pBLE2902->setNotifications(true);
  pBLE2902->setIndications(true);
  pCharacteristic->addDescriptor(pBLE2902);
  BLE2902 *pBLE2902Phone;
  pBLE2902Phone = new BLE2902();
  pBLE2902Phone->setNotifications(true);
  pBLE2902Phone->setIndications(true);
  phoneCharacteristic->addDescriptor(pBLE2902Phone);


  // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
  // Create a BLE Descriptor

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();
  std::string PISMO = "0_0_/_/"; 
  phoneCharacteristic->setValue(PISMO.c_str());
  phoneCharacteristic->notify();

}

void loop() {
  // notify changed value
    if (deviceConnected) {
      proveri_joystick();
      delay(10);
    }
    // disconnecting
    if (connectedClients != poslednji_broj_klijenata) {
      if (connectedClients == 0) {
        BLEDevice::startAdvertising();
        if (prvo_pokretanje){
          delay(500);
          Serial.println("Molimo povežite uređaje...");
          } else {
            Serial.println("Uređaji više nisu povezani! Molimo povežite uređaje...");
          }
        } 
      else if (connectedClients == 1) {
          delay(500); // give the bluetooth stack the chance to get things ready
          BLEDevice::startAdvertising(); // restart advertising

          if (poslednji_broj_klijenata == 2){
              Serial.println("Jedan uredjaj se odvezao! Molimo povežite ga opet...");
          } else {
              Serial.println("Jedan uredjaj je povezan! Molimo povežite i drugi uređaj...");
          }
          prvo_pokretanje = false;
      } else if (connectedClients == 2){
        delay(500);
        Serial.println("Oba uredjaja su povezana...");
        
      }

      poslednji_broj_klijenata = connectedClients;
      oldDeviceConnected = deviceConnected;
    }
}
