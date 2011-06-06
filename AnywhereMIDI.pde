#include <MIDI.h>
#include "MIDIPlayer.h"
//#include "input_mid.h"

#define LED 13   		// LED pin on Arduino board
#define FAN_0_PIN 3


#define TEST_SONG_EVENT_LENGTH 14

MIDIEvent testSongEvents[TEST_SONG_EVENT_LENGTH] = {
  {   0, NoteOn,  61, 100},
  {  50, NoteOff, 61,   0},
  { 100, NoteOn,  62, 100},
  { 150, NoteOff, 62,   0},
  { 200, NoteOn,  63, 100},
  { 250, NoteOff, 63,   0},
  { 300, NoteOn,  64, 100},
  { 350, NoteOff, 64,   0},
  { 400, NoteOn,  65, 100},
  { 450, NoteOff, 65,   0},
  { 500, NoteOn,  66, 100},
  { 550, NoteOff, 66,   0},
  { 600, NoteOn,  67, 100},
  { 650, NoteOff, 67,   0},
};
  

MIDISong testSong = {testSongEvents, TEST_SONG_EVENT_LENGTH, 700};

// Play a major scale warmup pattern


void setup() {
  pinMode(LED, OUTPUT);
  
  MIDI.begin(4);            	// Launch MIDI with default options
				// input channel is set to 4
}


void loop() {
//  Player.Play(input_mid);
  Player.Play(testSong);
}
