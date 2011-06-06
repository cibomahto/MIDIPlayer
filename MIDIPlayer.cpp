#include "MIDIPlayer.h"
#include "WProgram.h"
#include "HardwareSerial.h"
#include <avr/interrupt.h>

#define MIDI_CHANNEL 1

MIDIPlayer Player;

void MIDIPlayer::StartTimer() {
   // Set up Timer 2 to generate interrupts on overflow, and start it.
  // The display is updated in the interrupt routine
  TCCR2A = 0;
  TCCR2B = (1<<CS22)|(1<<CS21)|(1<<CS21);
  TIMSK2 = (1<<TOIE2);  
}

void MIDIPlayer::StopTimer() {
  TIMSK2 &= ~(1<<TOIE2);  
}

MIDIEvent& MIDIPlayer::getCurrentEvent() {
  return this->song->events[eventIndex];
}

void MIDIPlayer::Play(MIDISong& song) {
  this->song = &song;
  
  startTime = millis();
  eventIndex = 0;

//  StartTimer();

  unsigned long songTime;
  
  while (eventIndex < this->song->lengthNotes) {
    songTime = millis() - startTime;
    
    if (getCurrentEvent().time < songTime) {
      // Run the event!
      switch (getCurrentEvent().type) {
        case NoteOn:
          digitalWrite(13,HIGH);
          MIDI.sendNoteOn(getCurrentEvent().pitch, getCurrentEvent().velocity, MIDI_CHANNEL);
          break;
        case NoteOff:
          digitalWrite(13,LOW);
          MIDI.sendNoteOff(getCurrentEvent().pitch, getCurrentEvent().velocity, MIDI_CHANNEL);
          break;
        // TODO: Support other kinds of things here?
      }
      eventIndex++;
    }
  }
  
  do {
    songTime = millis() - startTime;
  }
  while (songTime < this->song->lengthMillis);
}

void MIDIPlayer::Stop() {
  StopTimer();
}

uint8_t LEDState = 0;
uint8_t LED = 13;

ISR(TIMER2_OVF_vect)
{
  if (LEDState == 0) {
//    digitalWrite(LED,HIGH);
    LEDState = 1;
  }
  else {
//    digitalWrite(LED,LOW);
    LEDState = 0;
  }
}

