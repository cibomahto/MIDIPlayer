#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
##################################
#
# mid2arduino.py, a MIDI to MIDIParser.pde song file converter
# by Matt Mets <mahto at cibomahto.com>
# Based on midi2cnc.py,
# by T. R. Gipson <drmn4ea at google mail>
# http://tim.cexx.org/?p=633
# Released under the GNU General Public License
#
##################################
#
# Includes midiparser.py module by Sean D. Spencer
# http://seandon4.tripod.com/
# This module is public domain.
#
##################################
#
# Hacked by Miles Lightwood of TeamTeamUSA to support
# the MakerBot Cupcake CNC - < m at teamteamusa dot com >
#
# Modified to handle multiple axes with the MakerBot 
# by H. Grote <hg at pscht dot com>
#
# Further hacked fully into 3 dimensions and generalised
# for multiple CNC machines by Michael Thomson
# <mike at m-thomson dot net>
# 
##################################
#
# More info on:
# http://groups.google.com/group/makerbotmusic
# 
##################################

# Requires Python 2.7
import argparse

import sys
import os.path
import math

# Import the MIDI parser code from the subdirectory './lib'
import lib.midiparser as midiparser



######################################
# Start of command line parsing code #
######################################

parser = argparse.ArgumentParser(description='Utility to process a Standard MIDI File (*.SMF/*.mid) to make a song that can be play back by Arduino.')

# Show the default values for each argument where available
#
parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

input=parser.add_argument_group('Input settings')
output=parser.add_argument_group('Output settings')

input.add_argument(
    '-infile', '--infile',
    default = './midi_files/input.mid',
    nargs   = '?',
    type    = argparse.FileType('r'),
    help    = 'the input MIDI filename'
)

input.add_argument(
    '-channels', '--channels',
    default = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    nargs   = '+',
    type    = int,
    choices = xrange(0,16),
    metavar = 'N',
    help    = 'list of MIDI channels you want to scan for event data'
)

input.add_argument(
    '-outfile', '--outfile',
    default = './song_files/output.h',
    nargs   = '?',
    type    = argparse.FileType('w'),
    help    = 'the output song filename'
)

output.add_argument(
    '-verbose', '--verbose',
    default = False,
    action  = 'store_true',
    help    = 'print verbose output to the terminal')

args = parser.parse_args()


suppress_comments = 0 # Set to 1 if your machine controller does not handle ( comments )


if os.path.getsize(args.infile.name) == 0:
    msg="Input file %s is empty! Aborting." % os.path.basename(args.infile.name)
    raise argparse.ArgumentTypeError(msg)

print "MIDI input file:\n    %s" % args.infile.name
print "Song output file:\n     %s" % args.outfile.name

tempo=None # should be set by your MIDI...

def main(argv):

    midi = midiparser.File(args.infile.name)
    
    print "\nMIDI file:\n    %s" % os.path.basename(args.infile.name)
    print "MIDI format:\n    %d" % midi.format
    print "Number of tracks:\n    %d" % midi.num_tracks
    print "Timing division:\n    %d" % midi.division

    noteEventList=[]
    all_channels=set()

    for track in midi.tracks:
        channels=set()
        for event in track.events:
            if event.type == midiparser.meta.SetTempo:
                tempo=event.detail.tempo
                if args.verbose:
                    print "Tempo change: " + str(event.detail.tempo)
            if ((event.type == midiparser.voice.NoteOn) and (event.channel in args.channels)): # filter undesired instruments
                if event.channel not in channels:
                    channels.add(event.channel)

                # NB: looks like some use "note on (vel 0)" as equivalent to note off, so check for vel=0 here and treat it as a note-off.
                if event.detail.velocity > 0:
                    noteEventList.append([event.absolute, 1, event.detail.note_no, event.detail.velocity])
                    if args.verbose:
                        print("Note on  (time, channel, note, velocity) : %6i %6i %6i %6i" % (event.absolute, event.channel, event.detail.note_no, event.detail.velocity) )
                else:
                    noteEventList.append([event.absolute, 0, event.detail.note_no, event.detail.velocity])
                    if args.verbose:
                        print("Note off (time, channel, note, velocity) : %6i %6i %6i %6i" % (event.absolute, event.channel, event.detail.note_no, event.detail.velocity) )
            if (event.type == midiparser.voice.NoteOff) and (event.channel in args.channels):

                if event.channel not in channels:
                    channels.add(event.channel)

                noteEventList.append([event.absolute, 0, event.detail.note_no, event.detail.velocity])
                if args.verbose:
                    print("Note off (time, channel, note, velocity) : %6i %6i %6i %6i" % (event.absolute, event.channel, event.detail.note_no, event.detail.velocity) )
            if event.type == midiparser.meta.TrackName: 
                if args.verbose:
                    print event.detail.text.strip()
            if event.type == midiparser.meta.CuePoint: 
                if args.verbose:
                    print event.detail.text.strip()
            if event.type == midiparser.meta.Lyric: 
                if args.verbose:
                    print event.detail.text.strip()
                #if event.type == midiparser.meta.KeySignature: 
                # ...

        # Finished with this track
        if len(channels) > 0:
            msg=', ' . join(['%2d' % ch for ch in sorted(channels)])
            print 'Processed track %d, containing channels numbered: [%s ]' % (track.number, msg)
            all_channels = all_channels.union(channels)

    # List all channels encountered
    if len(all_channels) > 0:
        msg=', ' . join(['%2d' % ch for ch in sorted(all_channels)])
        print 'The file as a whole contains channels numbered: [%s ]' % msg

    # We now have entire file's notes with abs time from all channels
    # We don't care which channel/voice is which, but we do care about having all the notes in order
    # so sort event list by abstime to dechannelify

    noteEventList.sort()
    print noteEventList
    # print len(noteEventList)

    # Start the output to file...
    # It would be nice to add some metadata here, such as who/what generated the output, what the input file was,
    # and important playback parameters (such as steps/in assumed and machine envelope).
    
    if suppress_comments == 0:
        args.outfile.write ("// Input file was " + os.path.basename(args.infile.name) + "\n")
   
    song_name = os.path.basename(args.infile.name).replace(".","_")

    args.outfile.write ("#ifndef " + song_name + "_\n")
    args.outfile.write ("#define " + song_name + "_\n\n")

    args.outfile.write ("#define " + song_name + "_EVENT_LENGTH " + str(len(noteEventList)) + "\n\n")

    args.outfile.write ("MIDIEvent " + song_name + "_events[" + song_name + "_EVENT_LENGTH] PROGMEM = {\n")

    for note in noteEventList:
        if note[1]==1: # Note on
            args.outfile.write(' {  %8d, NoteOn,  %3d, %3d},\n' % (note[0], note[2], note[3]))
            print 'Note on, time=%d, pitch=%d, velocity=%d' % (note[0], note[2], note[3])
        elif note[1]==0: # Note off
            args.outfile.write(' {  %8d, NoteOff, %3d, %3d},\n' % (note[0], note[2], note[3]))
            print 'Note off, time=%d, pitch=%d, velocity=%d' % (note[0], note[2], note[3])
    args.outfile.write ("};\n")

    args.outfile.write ("\nMIDISong " + song_name + " = {" + song_name + "_events, " + song_name + "_EVENT_LENGTH," + str(700) + "};\n\n")


    args.outfile.write ("#endif\n")

if __name__ == "__main__":
    main(sys.argv)
