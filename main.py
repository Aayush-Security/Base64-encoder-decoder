#!/usr/bin/python
#
#
#   Copyright (C) 2018 Aayush Trivedi <aayush_trivedi@hotmail.com>
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
import gtk
import b64converter as b64

class MainWindow(object):
    '''
    Window for the application. Users can either type the path to the file or
    use the "Choose" button to pick it from a dialog.

    The encode() and decode() methods translate directly to the CLI utility's
    functions.
    '''

    def encode(self, widget, data=None):
        '''
        Wrapper for b64converter.encode
        '''
        if self.lbl_file.get_text() == "":
            print "No file selected."
            self.statusbar.set_text("No file selected.")
        else:
            try:
                b64.encode(self.lbl_file.get_text())
                self.statusbar.set_text("Encoded to file %s" % 
                    self.lbl_file.get_text().split(os.sep)[-1] + ".txt")
            except IOError:
                print "File not found."
                self.statusbar.set_text("File not found.")

    def decode(self, widget, data=None):
        '''
        Wrapper for b64converter.decode
        '''
        if self.lbl_file.get_text() == "":
            print "No file selected."
            self.statusbar.set_text("No file selected.")
            return

        # Just so we prevent people from losing data if they don't
        # know very well what base64 is
        if not self.confirmnotxt.get_active():
            try:
                print self.lbl_file.get_text().split(".txt")[1]
            except IndexError:
                print "File doesn't look like base64 text"
                self.statusbar.set_text("This is not a text file. Check the box above to override.")
                return
        try:
            b64.decode(self.lbl_file.get_text())
            self.statusbar.set_text("Decoded to file %s" % 
                self.lbl_file.get_text().split(os.sep)[-1].split(".txt")[0])
        except IOError:
            print "File not found."
            self.statusbar.set_text("File not found.")

    def choose_file(self, widget, data=None):
        '''
        Launch file chooser dialog to easily pick a file.
        '''
        self.dialog = gtk.FileChooserDialog(
            title = "Choose a file",
            action = gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons = (
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                gtk.STOCK_OK, gtk.RESPONSE_OK
            )
        )
        self.chosen_file = self.dialog.run()
        if self.chosen_file == gtk.RESPONSE_OK:
            self.lbl_file.set_text(self.dialog.get_filename())
        else:
            print "Nothing changed."
        self.dialog.destroy()
    
    def destroy(self, widget, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        # Temporary storage for showing widgets later
        self.widgets = []

        # Widgets themselves...
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Base 64 Converter")
        self.window.set_default_size(420, 100)
        self.window.set_border_width(5)
        self.instructions = gtk.Label("Select a file and convert to or from base64!")
        self.widgets.append(self.instructions)
        self.btn_encode = gtk.Button("_Encode")
        self.widgets.append(self.btn_encode)
        self.btn_decode = gtk.Button("_Decode")
        self.widgets.append(self.btn_decode)
        self.lbl_file = gtk.Entry()
        self.widgets.append(self.lbl_file)
        self.btn_filechooser = gtk.Button("Choose file")
        self.widgets.append(self.btn_filechooser)
        self.statusbar = gtk.Label("Program OK")
        self.widgets.append(self.statusbar)
        self.confirmnotxt = gtk.CheckButton("_Ignore extension")
        self.widgets.append(self.confirmnotxt)
        self.confirmnotxtexplanation = gtk.Label(
            "By default only *.txt files can be decoded.\nCheck this box to decode any file."
        )
        self.widgets.append(self.confirmnotxtexplanation)

        # Widget containers
        self.vgrid = gtk.VBox(False, 2)
        self.file_row = gtk.HBox(False, 0)
        self.btn_row = gtk.HBox(True, 0)
        self.override_row = gtk.HBox(False, 1)
        self.widgets.append(self.vgrid)
        self.widgets.append(self.file_row)
        self.widgets.append(self.btn_row)
        self.widgets.append(self.override_row)

        # Connect buttons to interactions
        self.window.connect("destroy", self.destroy)
        self.btn_encode.connect("clicked", self.encode)
        self.btn_decode.connect("clicked", self.decode)
        self.btn_filechooser.connect("clicked", self.choose_file)

        # Pack, show and add everything to main window
        self.file_row.pack_start(self.lbl_file, True, True, 0)
        self.file_row.pack_start(self.btn_filechooser, False, False, 0)
        self.btn_row.pack_start(self.btn_encode, True, True, 0)
        self.btn_row.pack_start(self.btn_decode, True, True, 0)
        self.override_row.pack_start(self.confirmnotxtexplanation, True, True, 0)
        self.override_row.pack_start(self.confirmnotxt, False, False, 0)
        self.vgrid.pack_start(self.instructions, True, True, 0)
        self.vgrid.pack_start(self.file_row, False, False, 0)
        self.vgrid.pack_start(self.btn_row, False, False, 0)
        self.vgrid.pack_start(self.override_row, False, True, 0)
        self.vgrid.pack_start(self.statusbar, False, False, 0)

        for widget in self.widgets:
            widget.show()

        self.window.add(self.vgrid)
        self.window.show()

    def main(self):
        gtk.main()
        return 0

if __name__ == "__main__":
    window = MainWindow()
    window.main()
    print "Exit ok!"
