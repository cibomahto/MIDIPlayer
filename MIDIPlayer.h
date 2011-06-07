// Simple class to play back a midi file
// Written by Matt Mets in 2011, in support of Matthew Borgatti's Anywhere Organ
// This uses the 

#ifndef MIDIPLAYER_H
#define MIDIPLAYER_H

#include <MIDI.h>
#include <avr/pgmspace.h>

struct MIDIEvent {
  unsigned long time;
  kMIDIType type;
  uint8_t pitch;
  uint8_t velocity;
};


struct MIDISong {
  MIDIEvent* events;            // assumed to be in program space (define as PROGMEM)
  uint16_t lengthNotes;
  unsigned long lengthMillis;
};

class MIDIPlayer {
private:
  MIDISong* song;
  unsigned long startTime;
  uint16_t eventIndex;
  
  void getCurrentEvent(MIDIEvent& currentEvent);
  void StartTimer();
  void StopTimer();
public:
  void Play(MIDISong& song);
  void Stop();
};


extern MIDIPlayer Player;

#endif // MIDIPLAYER_H

