#include <MIDI.h>
#include "MIDIPlayer.h"
#include "input_mid.h"

#define LED 13   		// LED pin on Arduino board
#define FAN_0_PIN 3


#define TEST_SONG_EVENT_LENGTH 18

MIDIEvent testSongEvents[TEST_SONG_EVENT_LENGTH] PROGMEM = {
  {   0, NoteOn,  61, 99},
  { 20, NoteOff, 61,   100},
  {   50, NoteOn,  65, 101},
  {   50, NoteOn,  67, 102},
  { 200, NoteOff, 61,   103},
  { 200, NoteOff, 65,   104},
  { 200, NoteOff, 67,   105},
};
  

MIDISong testSong = {testSongEvents, TEST_SONG_EVENT_LENGTH, 700};


void setup() {
  pinMode(LED, OUTPUT);
  
  MIDI.begin(4);            	// Launch MIDI with default options
				// input channel is set to 4
}


void loop() {
  
  Player.Play(Super_Mario_Brothers_nodrums_mid);
  Player.Play(Imperial_March_mid);
//  Player.Play(testSong);
}
