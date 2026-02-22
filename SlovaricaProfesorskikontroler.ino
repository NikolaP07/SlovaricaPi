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
#define BUTTON_PIN 26 
#define BUTTON_PIN2 25
#define SwitchButnn 33
#define pinCir 21
#define pinLat 19
const int a = 2, b = 4, c = 14, d = 12, e = 13, f = 5, g = 18;

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      Serial.println("Uređaj je uspešno povezan!");
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};
byte digits[10][7] = {
  {1,1,1,1,1,1,0}, // 0
  {0,1,1,0,0,0,0}, // 1
  {1,1,0,1,1,0,1}, // 2
  {1,1,1,1,0,0,1}, // 3
  {0,1,1,0,0,1,1}, // 4
  {1,0,1,1,0,1,1}, // 5
  {1,0,1,1,1,1,1}, // 6
  {1,1,1,0,0,0,0}, // 7
  {1,1,1,1,1,1,1}, // 8
  {1,1,1,1,0,1,1}  // 9
};


void displayNumber(int num) {
  digitalWrite(a, digits[num][0]);
  digitalWrite(b, digits[num][1]);
  digitalWrite(c, digits[num][2]);
  digitalWrite(d, digits[num][3]);
  digitalWrite(e, digits[num][4]);
  digitalWrite(f, digits[num][5]);
  digitalWrite(g, digits[num][6]);
}



unsigned long zadnje_vreme_pomeraja = 0;
const int pauza_izmedju_koraka = 200;

bool spreman_za_pomeraj = true;
int buttonState ;
int buttonStateSet ;
int SwitchPismo;
int counter=0;
bool cirilica=true;

void setup() {
  Serial.begin(115200);
  Serial.println("BLE se pokreće!");

  BLEDevice::init("SlovaricaProfesorskiKontroler");
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
  pinMode(BUTTON_PIN,  INPUT_PULLUP);
  pinMode(BUTTON_PIN2,  INPUT_PULLUP);
  pinMode(SwitchButnn,  INPUT_PULLUP);
  pinMode(a, OUTPUT); pinMode(b, OUTPUT); pinMode(c, OUTPUT);
  pinMode(d, OUTPUT); pinMode(e, OUTPUT); pinMode(f, OUTPUT);
  pinMode(g, OUTPUT);
  pinMode(pinCir, OUTPUT);
  pinMode(pinLat, OUTPUT);
  if(cirilica){
      digitalWrite(pinCir, HIGH);
      digitalWrite(pinLat, LOW);
  }else{
    digitalWrite(pinCir, LOW);
    digitalWrite(pinLat, HIGH);
  }
}
int incriment=HIGH;
int incriment2=HIGH;
int SwitchCheck=HIGH;

void loop() {
    // notify changed value
    if (deviceConnected) {
            buttonState = digitalRead( BUTTON_PIN);
            buttonStateSet = digitalRead( BUTTON_PIN2);
            SwitchPismo= digitalRead(SwitchButnn);

            if (millis() - zadnje_vreme_pomeraja > pauza_izmedju_koraka){
              bool registrovano = false;

              if (incriment == LOW &&  buttonState  == HIGH) {
               
                counter+=1;
                if(counter>2){
                  counter=0;
                }
               
              
              }

                displayNumber(counter);
                incriment= buttonState;
              
              if (incriment2 == LOW &&  buttonStateSet == HIGH){
                std::string DESNO;
                switch(counter) {
                    case 0:
                   Serial.println(counter);
                    registrovano=true;
                    DESNO = "0"; 
                    pCharacteristic->setValue(DESNO.c_str());
                    pCharacteristic->notify();
                  
                      break;
                    case 1:
                       Serial.println(counter);
                    registrovano=true;
                     DESNO = "1"; 
                    pCharacteristic->setValue(DESNO.c_str());
                    pCharacteristic->notify();
                    
                  
                      break;
                      case 2:
                       Serial.println(counter);
                    registrovano=true;
                     DESNO = "2"; 
                    pCharacteristic->setValue(DESNO.c_str());
                    pCharacteristic->notify();
                   
                      break;
                
                  }
               
              } 
               incriment2= buttonStateSet;
               if(SwitchCheck==LOW && SwitchPismo==HIGH){
              cirilica=!cirilica;
                Serial.println(counter);
                    registrovano=true;
                     std::string Pismo; 
                     if(cirilica){
                          Pismo="Cirilica";
                     }else{
                        Pismo="Latinica";
                     }
                    pCharacteristic->setValue(Pismo.c_str());
                    pCharacteristic->notify();

               }
               SwitchCheck=SwitchPismo;
                 if(cirilica){
                      digitalWrite(pinCir, HIGH);
                      digitalWrite(pinLat, LOW);
                  }else{
                    digitalWrite(pinCir, LOW);
                    digitalWrite(pinLat, HIGH);
                  }

              if (registrovano) {
                zadnje_vreme_pomeraja = millis();
              }
              Serial.print("buttonStateSet: ");
              Serial.print(buttonStateSet);
              Serial.print("\n");
              Serial.print("buttonState:");
              Serial.print(buttonState);
              Serial.print("\n");
              Serial.print("SwitchPismo :");
              Serial.print(SwitchPismo);
              Serial.print("\n");
              Serial.print("Cirilica ");
              Serial.print(cirilica);
              Serial.println();
              
            } 
            
      delay(50);
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