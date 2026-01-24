#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <BLEServer.h>
#include <BLE2902.h>

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"


class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      Serial.println("Uređaj je uspešno povezan!");
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};

#define VRX_PIN  4
#define VRY_PIN  3

int xValue= 0;
int yValue= 0;

unsigned long zadnje_vreme_pomeraja = 0;
const int pauza_izmedju_koraka = 200;

bool spreman_za_pomeraj = true;

void proveri_joystick() {
            int x = analogRead(VRX_PIN);
            int y = analogRead(VRY_PIN);

            if (millis() - zadnje_vreme_pomeraja > pauza_izmedju_koraka){
              bool registrovano = false;

              if (x < 500) {
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
              }

              if (y < 500){
                Serial.println("GORE");
                registrovano=true;
                std::string GORE = "GORE"; 
                pCharacteristic->setValue(GORE.c_str());
                pCharacteristic->notify();
              } 
              else if (y > 3500){
                Serial.println("DOLE");
                registrovano=true;
                std::string DOLE = "DOLE"; 
                pCharacteristic->setValue(DOLE.c_str());
                pCharacteristic->notify();
              }

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
  Serial.println("BLE se pokreće!");

  BLEDevice::init("Slovarica");
  BLEServer *pServer = BLEDevice::createServer();
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

  // https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml
  // Create a BLE Descriptor

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x0);  // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();
  Serial.println("Molimo povežite uređaj...");
}

void loop() {
    // notify changed value
    if (deviceConnected) {
      proveri_joystick();
      delay(10);
    }
    // disconnecting
    if (!deviceConnected && oldDeviceConnected) {
        delay(500); // give the bluetooth stack the chance to get things ready
        pServer->startAdvertising(); // restart advertising
        Serial.println("Uređaj više nije povezan! Molimo povežite uređaj...");
        oldDeviceConnected = deviceConnected;
    }
    // connecting
    if (deviceConnected && !oldDeviceConnected) {
        // do stuff here on connecting
        oldDeviceConnected = deviceConnected;
    }
}