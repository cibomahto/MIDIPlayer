#include <MIDI.h>
#include <MIDIPlayer.h>
#include "Super_Mario_Brothers_nodrums_mid.h"
#include "Imperial_March_mid.h"


void setup() {
  MIDI.begin(4);            	// Launch MIDI with default options
				// input channel is set to 4
}

void loop() {
  Player.Play(Super_Mario_Brothers_nodrums_mid);
  Player.Play(Imperial_March_mid);
}
