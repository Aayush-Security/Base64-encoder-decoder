#!/usr/bin/python
# 
# b64converter:
# Utility to convert to and from base64 encodings as a plaintext file.
# This program may be used either combined with a graphical utility or
# standalone as a CLI utility.
#
#   Copyright (C) 2015 Vitor S <https://notabug.org/kzimmermann>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import base64 as b64

def encode(infilename):
    '''
    Takes infile and encodes it into a plaintext base64 file, adding '.txt'
    to its original filename in the process
    '''
    with file(infilename, 'rb') as infile:
        with file(infilename + '.txt', 'w') as outfile:
            b64.encode(infile, outfile)
    print "Encoded %s to %s" % (infilename, infilename + '.txt')

def decode(infilename):
    '''
    Takes base64-encoded infile and decodes it to its original format. It will
    attempt to remove any '.txt' from the filename.
    '''
    decoded_filename = infilename.split(".txt")[0]
    with file(infilename, 'r') as infile:
        with file(decoded_filename, 'wb') as outfile:
            b64.decode(infile, outfile)
    print "Decoded %s to %s" % (infilename, infilename.split('.txt')[0])

# Auxilliary functions declared only if we're running in CLI mode:
if __name__ == "__main__":

    def shuffle(args):
        "Takes sys.argv and processes it to encode/decode function input"
        args.reverse()
        args.pop()
        args.pop()
        args.reverse()

    def getopts(args):
        "Returns a string containing the decision from parsing options"
        if "-h" in args:
            return "help"
        elif "-e" in args and "-d" in args:
            return "error"
        elif "-e" in args:
            return "encode"
        elif "-d" in args:
            return "decode"
        else:
            return "error"
    
    def helper():
        print "%s - a base64 decoder/encoder of files" % sys.argv[0]
        print "USAGE: %s [-e|-d|-h] FILE1 FILE2 ... FILEN" % sys.argv[0]
        print "Where:"
        print " -e: encodes FILES to base64 .txt files"
        print " -d: decodes base64 .txt FILES to their original encoding"
        print " -h: displays this help message"

    command = getopts(sys.argv)
    progname = sys.argv[0] # required. Read on for why...

    if command == "error":
        print "Error: invalid inputs"
        helper()
        sys.exit(1)

    if command == "help":
        helper()
        sys.exit(0)

    elif command == "encode":
        shuffle(sys.argv)
        for item in sys.argv:
            try:
                encode(item)
            except IOError:
                print "File not found: '%s'" % item 
                sys.exit(1)
                
        if len(sys.argv) == 1:
            print "1 file encoded."
        else:
            print "%s files encoded." % len(sys.argv)
        sys.exit(0)

    elif command == "decode":
        shuffle(sys.argv)
        for item in sys.argv:
            # If you don't check for this thing, you may overwrite this very
            # program! And if you don't have a backup, it can be *very*
            # annoying.
            try:
                decode(item)
            except IOError:
                print "File not found: '%s'" % item
                sys.exit(1)
        if len(sys.argv) == 1:
            print "1 file decoded."
        else:
            print "%s files decoded." % len(sys.argv)
        print "You may want to use the UNIX `file' command to find the format"
        sys.exit(0)
    else:
        print "Unknown error received. Exiting..."
