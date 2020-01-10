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
  //radio.powerUp() ;
  radio.startListening();
  printf_begin();
  Serial.begin(9600);
  radio.printDetails();
}

bool isDone;
char coordinates[30];
char sol_x[5];
char sol_y[5];
char sag_x[5];
char sag_y[5];
void loop(void){
  sol_x_durum = analogRead(sol_x_ekseni);
  sol_y_durum = analogRead(sol_y_ekseni);
  sag_x_durum = analogRead(sag_x_ekseni);
  sag_y_durum = analogRead(sag_y_ekseni);

  itoa(sol_x_durum, sol_x, 10);
  itoa(sol_y_durum, sol_y, 10);
  itoa(sag_x_durum, sag_x, 10);
  itoa(sag_y_durum, sag_y, 10);

  strcpy(coordinates, sol_x);
  strcat(coordinates, ",");
  strcat(coordinates, sol_y);
  strcat(coordinates, ",");
  strcat(coordinates, sag_x);
  strcat(coordinates, ",");
  strcat(coordinates, sag_y);

  Serial.println(coordinates);
  
  radio.stopListening();
  isDone = radio.write(&coordinates, sizeof(coordinates));
  radio.startListening();
  delay(1);
}
