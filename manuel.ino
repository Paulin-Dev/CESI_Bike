#include <ArduinoJson.h>
#include <Wire.h>
#include "rgb_lcd.h"
rgb_lcd lcd;

const unsigned int POSTE = 5;             // numéro du poste, à modifier

const unsigned int BUTTON_BLUE = 2;       // pin bouton bleu
const unsigned int LED_BLUE = 10;         // pin led bleue
bool state_blue = false;                  // état de la led bleu
bool pressed_blue = false;                // état du bouton bleu (pressé ou non) afin d'eviter le changement d'etat de la led si on reste appuyé

const unsigned int BUTTON_GREEN = 3;
const unsigned int LED_GREEN = 11; 
bool state_green = false;
bool pressed_green = false;

const unsigned int BUTTON_YELLOW = 4;   
const unsigned int LED_YELLOW = 12;
bool state_yellow = false;
bool pressed_yellow = false;

const unsigned int BUTTON_RED = 5;
const unsigned int LED_RED = 13;
bool state_red = false;
bool pressed_red = false;

const unsigned int BUTTON_WAIT = 100;     // délai (en ms) d'attente avant le prochain check du bouton (minimum 100)

void setup() {
  Serial.begin(9600);
  
  pinMode(BUTTON_BLUE, INPUT);
  pinMode(LED_BLUE, OUTPUT);
  digitalWrite(LED_BLUE, LOW);

  pinMode(BUTTON_GREEN, INPUT);
  pinMode(LED_GREEN, OUTPUT);
  digitalWrite(LED_GREEN, LOW);

  pinMode(BUTTON_YELLOW, INPUT);
  pinMode(LED_YELLOW, OUTPUT);
  digitalWrite(LED_YELLOW, LOW);

  pinMode(BUTTON_RED, INPUT);
  pinMode(LED_RED, OUTPUT); 
  digitalWrite(LED_RED, LOW);

  // affichage texte sur ecran lcd pour le poste 3
  if (POSTE == 3){
    lcd.begin(11, 2);
    lcd.print("  BACHELOR IA");
  }
}

// affiche des données sur le port serial en format json
void send_json(String color, String state){
  const size_t CAPACITY = JSON_ARRAY_SIZE(6);
  StaticJsonDocument<CAPACITY> doc;
  doc["poste"] = POSTE;
  doc["color"] = color;
  doc["state"] = state;
  serializeJson(doc, Serial);
  Serial.println("");
}


void action_blue(){
  // si le bouton est pressé
  if (digitalRead(BUTTON_BLUE)){
    // si il n'etait pas deja pressé
    if (!pressed_blue){
      // si la led est eteinte
      if (!state_blue) {
        // allume la led et envoie les donnees
        digitalWrite(LED_BLUE, HIGH);
        send_json("blue", "on");
        state_blue = true;
      } else {
        // sinon eteint la led et envoie les donnees
        digitalWrite(LED_BLUE, LOW);
        send_json("blue", "off");
        state_blue = false;
        }
      // delai avant la prochaine verification pour le bouton
      delay(BUTTON_WAIT);
      pressed_blue = true;
    }
  } else {pressed_blue = false;}
}

void action_green(){
  if (digitalRead(BUTTON_GREEN)){
    if (!pressed_green){
        if (!state_green) {
          digitalWrite(LED_GREEN, HIGH);
          send_json("green", "on");
          state_green = true;
        } else {
          digitalWrite(LED_GREEN, LOW);
          send_json("green", "off");
          state_green = false;
          }
       delay(BUTTON_WAIT);
       pressed_green = true;
    }
  } else {pressed_green = false;}
}

void action_yellow(){
  if (digitalRead(BUTTON_YELLOW)){
    if (!pressed_yellow){
        if (!state_yellow) {
          digitalWrite(LED_YELLOW, HIGH);
          send_json("yellow", "on");
          state_yellow = true;
        } else {
          digitalWrite(LED_YELLOW, LOW);
          send_json("yellow", "off");
          state_yellow = false;
          }
       delay(BUTTON_WAIT);
       pressed_yellow = true;
    }
  } else {pressed_yellow = false;}
}

void action_red(){
  if (digitalRead(BUTTON_RED)){
    if (!pressed_red){
        if (!state_red) {
          digitalWrite(LED_RED, HIGH);
          send_json("red", "on");
          state_red = true;
        } else {
          digitalWrite(LED_RED, LOW);
          send_json("red", "off");
          state_red = false;
          }
       delay(BUTTON_WAIT);
       pressed_red = true;
    }
  } else {pressed_red = false;}
}

// lit les donnees envoyées depuis le pc et effectue le changement d'etat des leds
void read_data(){
  if (Serial.available() > 0){
    String str = Serial.readString();
    if (str[1] == 'B'){
      if (str[2] == 'A'){
        digitalWrite(LED_BLUE, HIGH);
      } else {
        digitalWrite(LED_BLUE, LOW);
      }
    } else {
      if (str[2] == 'A'){
        digitalWrite(LED_RED, HIGH);
      } else {
        digitalWrite(LED_RED, LOW);
      }
    }
  } 
}

// commenter / décommenter pour activer / desactiver l'action des boutons sur les leds
void loop() {
  //action_blue();
  action_green();
  //action_yellow();
  //action_red();   
  read_data();
}
