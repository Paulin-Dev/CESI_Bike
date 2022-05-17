/*
Jouer un son avec un Grove Speaker
*/

#define SPEAKER 3   // pin du systeme audio

void setup()
{
  pinMode(SPEAKER, OUTPUT);
  digitalWrite(SPEAKER, LOW);
}

void sound(int note_index){
  int duration = 20;
  for(int i = 0; i < duration; i++){
    digitalWrite(SPEAKER, HIGH);
    delayMicroseconds(note_index);
    digitalWrite(SPEAKER, LOW);
    delayMicroseconds(note_index);
  }  
}

void loop()
{
  sound(1000);
}
