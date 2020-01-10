#include<SPI.h>                   // spi library for connecting nrf
#include<RF24.h>                  // nrf library
#include <printf.h>

const int sol_x_ekseni = A0;
const int sol_y_ekseni = A1;
const int sag_x_ekseni = A2;
const int sag_y_ekseni = A3; 

int sol_x_durum;
int sol_y_durum;
int sag_x_durum;
int sag_y_durum;

RF24 radio(9,8) ;  // ce, csn pins    
void setup(void){
  radio.begin() ;
  radio.setPALevel(RF24_PA_MAX) ;
  radio.setChannel(0x60) ;
  radio.openWritingPipe(0xc2c2c2c2c2LL);
  radio.openReadingPipe(1, 0xe7e7e7e7e7LL);
  radio.enableDynamicPayloads() ;
  radio.startListening();
  printf_begin();
  Serial.begin(9600);
  radio.printDetails();
}

bool isDone;
uint8_t coordinates[2];
void loop(void){
  coordinates[0] = map(analogRead(sol_y_ekseni), 0, 1023, 0, 255);
  coordinates[1] = map(analogRead(sag_x_ekseni), 0, 1023, 0, 255);
  
  radio.stopListening();
  radio.write(&coordinates, sizeof(coordinates));
  radio.startListening();
  delay(1);
}
