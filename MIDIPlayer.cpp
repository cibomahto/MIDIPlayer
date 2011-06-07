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

void MIDIPlayer::getCurrentEvent(MIDIEvent& currentEvent) {
  currentEvent.time = pgm_read_dword(&song->events[eventIndex].time);
  currentEvent.type = (kMIDIType)pgm_read_byte(&song->events[eventIndex].type);
  currentEvent.pitch = pgm_read_byte(&song->events[eventIndex].pitch);
  currentEvent.velocity = pgm_read_byte(&song->events[eventIndex].velocity);

//  currentEvent.time = song->events[eventIndex].time;
//  currentEvent.type = song->events[eventIndex].type;
//  currentEvent.pitch = song->events[eventIndex].pitch;
//  currentEvent.velocity = song->events[eventIndex].velocity;
}

void MIDIPlayer::Play(MIDISong& song) {
  this->song = &song;
  
  startTime = millis();
  eventIndex = 0;

  unsigned long songTime;
  MIDIEvent currentEvent;
  
  getCurrentEvent(currentEvent);
  
  while (eventIndex < this->song->lengthNotes) {
    songTime = millis() - startTime;
       
    if (currentEvent.time < songTime) {
      // Run the event!
      switch (currentEvent.type) {
        case NoteOn:
          MIDI.sendNoteOn(currentEvent.pitch, currentEvent.velocity, MIDI_CHANNEL);
          break;
        case NoteOff:
          MIDI.sendNoteOff(currentEvent.pitch, currentEvent.velocity, MIDI_CHANNEL);
          break;
        // TODO: Support other kinds of things here?
      }
      eventIndex++;
      getCurrentEvent(currentEvent);
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

// TODO: It might be nice to offload this to a background thread?
//uint8_t LEDState = 0;
//uint8_t LED = 13;
//
//ISR(TIMER2_OVF_vect)
//{
//  if (LEDState == 0) {
////    digitalWrite(LED,HIGH);
//    LEDState = 1;
//  }
//  else {
////    digitalWrite(LED,LOW);
//    LEDState = 0;
//  }
//}

