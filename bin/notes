#!/usr/bin/python2

'''
This code is released into public domain with no explicit or implied waranty.
Use this code at your own risk, I am not to be held responsible if this code in any way causes damage to you/your computer/your loved ones.
'''

from gi.repository import Gtk, Gdk, GObject
import os
import signal

#Creating files for settings and whatnot. Allows for windows even though this app is unix only, it's just code I have lying around.
projectname = "dropdownnotes"
if os.name != "posix":
    from win32com.shell import shellcon, shell
    homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
else:
    homedir = os.path.join(os.path.expanduser("~"), ".config")
settingsdirectory = os.path.join(homedir,projectname)
if not os.path.isdir(settingsdirectory):
    os.mkdir(settingsdirectory)
notesfilepath = os.path.join(settingsdirectory,"notes")
lockfilepath = os.path.join(settingsdirectory,".lock")

#Create the notes file, so the read below will work during first run
if not os.path.isfile(notesfilepath):
    open(notesfilepath,'w').close()
#Read the notes file
with open(notesfilepath,'r') as notesfile:
    notes = notesfile.read()


class Notes(Gtk.Window):
    ''' A window that contains only a scrolled window and a text field. '''
    def __init__(self,text, filepath):
        Gtk.Window.__init__(self, title="Dropdown Notes")
        self.filepath = filepath
        self.set_default_size(400, 200)
        #Infinite sized window
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.textbuffer = UndoableBuffer()
        self.textview = Gtk.TextView.new_with_buffer(self.textbuffer)
        # self.textbuffer = self.textview.get_buffer()
        self.textbuffer.begin_not_undoable_action()
        self.textbuffer.set_text(text)
        self.textbuffer.end_not_undoable_action()
        scrolledwindow.add(self.textview)
        self.add(scrolledwindow)
        #Close on escape
        self.connect("key-press-event", self.keypress)
        #Write out whenever the buffer is edited
        self.textbuffer.connect("changed", self.buffer_changed)

    def keypress(self,window,event):

        default_modmask = Gtk.accelerator_get_default_mod_mask()

        #Close on escape
        if event.keyval == Gdk.KEY_Escape:
            self.destroy()
        elif (event.keyval == Gdk.KEY_z or event.keyval == Gdk.KEY_Z) and (event.state & default_modmask) == Gdk.ModifierType.CONTROL_MASK:
            self.textbuffer.undo()
        elif (((event.keyval == Gdk.KEY_z or event.keyval == Gdk.KEY_Z) and (event.state & default_modmask) == (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK)) or 
              ((event.keyval == Gdk.KEY_z or event.keyval == Gdk.KEY_Z) and (event.state & default_modmask) == Gdk.ModifierType.CONTROL_MASK)):
            self.textbuffer.redo()

    def buffer_changed(self, *args):
        ''' Whenever the text is changed, write it '''
        self.write_text()
    def write_text(self):
        ''' Take the text from the buffer and write it to a file. Nothing special. '''
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        with open(self.filepath,'w') as notesfile:
            notesfile.write(self.textbuffer.get_text(start, end, False))

def on_kill(*args):
    window = args[0];
    start = window.textbuffer.get_start_iter()
    end = window.textbuffer.get_end_iter()
    with open(notesfilepath,'w') as notesfile:
        notesfile.write(window.textbuffer.get_text(start, end, False))
    Gtk.main_quit()

#Not used anymore, but not terrible to have around, maybe I'll add options later
def check_pid(pid):        
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True



""" gtk textbuffer with undo functionality """

#Copyright (C) 2009 Florian Heinle
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

class UndoableInsert(object):
    """something that has been inserted into our textbuffer"""
    def __init__(self, text_iter, text, length):
        self.offset = text_iter.get_offset()
        self.text = text
        self.length = length
        if self.length > 1 or self.text in ("\r", "\n", " "):
            self.mergeable = False
        else:
            self.mergeable = True

class UndoableDelete(object):
    """something that has ben deleted from our textbuffer"""
    def __init__(self, text_buffer, start_iter, end_iter):
        self.text = text_buffer.get_text(start_iter, end_iter, False)
        self.start = start_iter.get_offset()
        self.end = end_iter.get_offset()
        # need to find out if backspace or delete key has been used
        # so we don't mess up during redo
        insert_iter = text_buffer.get_iter_at_mark(text_buffer.get_insert())
        if insert_iter.get_offset() <= self.start:
            self.delete_key_used = True
        else:
            self.delete_key_used = False
        if self.end - self.start > 1 or self.text in ("\r", "\n", " "):
            self.mergeable = False
        else:
            self.mergeable = True

class UndoableBuffer(Gtk.TextBuffer):
    """text buffer with added undo capabilities

    designed as a drop-in replacement for gtksourceview,
    at least as far as undo is concerned"""
    
    def __init__(self):
        """
        we'll need empty stacks for undo/redo and some state keeping
        """
        Gtk.TextBuffer.__init__(self)
        self.undo_stack = []
        self.redo_stack = []
        self.not_undoable_action = False
        self.undo_in_progress = False
        self.connect('insert-text', self.on_insert_text)
        self.connect('delete-range', self.on_delete_range)

    @property
    def can_undo(self):
        return bool(self.undo_stack)

    @property
    def can_redo(self):
        return bool(self.redo_stack)

    def on_insert_text(self, textbuffer, text_iter, text, length):
        def can_be_merged(prev, cur):
            """see if we can merge multiple inserts here

            will try to merge words or whitespace
            can't merge if prev and cur are not mergeable in the first place
            can't merge when user set the input bar somewhere else
            can't merge across word boundaries"""
            WHITESPACE = (' ', '\t')
            if not cur.mergeable or not prev.mergeable:
                return False
            elif cur.offset != (prev.offset + prev.length):
                return False
            elif cur.text in WHITESPACE and not prev.text in WHITESPACE:
                return False
            elif prev.text in WHITESPACE and not cur.text in WHITESPACE:
                return False
            return True

        if not self.undo_in_progress:
            self.redo_stack = []
        if self.not_undoable_action:
            return
        undo_action = UndoableInsert(text_iter, text, length)
        try:
            prev_insert = self.undo_stack.pop()
        except IndexError:
            self.undo_stack.append(undo_action)
            return
        if not isinstance(prev_insert, UndoableInsert):
            self.undo_stack.append(prev_insert)
            self.undo_stack.append(undo_action)
            return
        if can_be_merged(prev_insert, undo_action):
            prev_insert.length += undo_action.length
            prev_insert.text += undo_action.text
            self.undo_stack.append(prev_insert)
        else:
            self.undo_stack.append(prev_insert)
            self.undo_stack.append(undo_action)
        
    def on_delete_range(self, text_buffer, start_iter, end_iter):
        def can_be_merged(prev, cur):
            """see if we can merge multiple deletions here

            will try to merge words or whitespace
            can't merge if prev and cur are not mergeable in the first place
            can't merge if delete and backspace key were both used
            can't merge across word boundaries"""

            WHITESPACE = (' ', '\t')
            if not cur.mergeable or not prev.mergeable:
                return False
            elif prev.delete_key_used != cur.delete_key_used:
                return False
            elif prev.start != cur.start and prev.start != cur.end:
                return False
            elif cur.text not in WHITESPACE and \
               prev.text in WHITESPACE:
                return False
            elif cur.text in WHITESPACE and \
               prev.text not in WHITESPACE:
                return False
            return True

        if not self.undo_in_progress:
            self.redo_stack = []
        if self.not_undoable_action:
            return
        undo_action = UndoableDelete(text_buffer, start_iter, end_iter)
        try:
            prev_delete = self.undo_stack.pop()
        except IndexError:
            self.undo_stack.append(undo_action)
            return
        if not isinstance(prev_delete, UndoableDelete):
            self.undo_stack.append(prev_delete)
            self.undo_stack.append(undo_action)
            return
        if can_be_merged(prev_delete, undo_action):
            if prev_delete.start == undo_action.start: # delete key used
                prev_delete.text += undo_action.text
                prev_delete.end += (undo_action.end - undo_action.start)
            else: # Backspace used
                prev_delete.text = "%s%s" % (undo_action.text,
                                                     prev_delete.text)
                prev_delete.start = undo_action.start
            self.undo_stack.append(prev_delete)
        else:
            self.undo_stack.append(prev_delete)
            self.undo_stack.append(undo_action)

    def begin_not_undoable_action(self):
        """don't record the next actions
        
        toggles self.not_undoable_action"""
        self.not_undoable_action = True        

    def end_not_undoable_action(self):
        """record next actions
        
        toggles self.not_undoable_action"""
        self.not_undoable_action = False
    
    def undo(self):
        """undo inserts or deletions

        undone actions are being moved to redo stack"""
        if not self.undo_stack:
            return
        self.begin_not_undoable_action()
        self.undo_in_progress = True
        undo_action = self.undo_stack.pop()
        self.redo_stack.append(undo_action)
        if isinstance(undo_action, UndoableInsert):
            start = self.get_iter_at_offset(undo_action.offset)
            stop = self.get_iter_at_offset(
                undo_action.offset + undo_action.length
            )
            self.delete(start, stop)
            self.place_cursor(start)
        else:
            start = self.get_iter_at_offset(undo_action.start)
            self.insert(start, undo_action.text)
            stop = self.get_iter_at_offset(undo_action.end)
            if undo_action.delete_key_used:
                self.place_cursor(start)
            else:
                self.place_cursor(stop)
        self.end_not_undoable_action()
        self.undo_in_progress = False

    def redo(self):
        """redo inserts or deletions

        redone actions are moved to undo stack"""
        if not self.redo_stack:
            return
        self.begin_not_undoable_action()
        self.undo_in_progress = True
        redo_action = self.redo_stack.pop()
        self.undo_stack.append(redo_action)
        if isinstance(redo_action, UndoableInsert):
            start = self.get_iter_at_offset(redo_action.offset)
            self.insert(start, redo_action.text)
            new_cursor_pos = self.get_iter_at_offset(
                redo_action.offset + redo_action.length
            )
            self.place_cursor(new_cursor_pos)
        else:
            start = self.get_iter_at_offset(redo_action.start)
            stop = self.get_iter_at_offset(redo_action.end)
            self.delete(start, stop)
            self.place_cursor(start)
        self.end_not_undoable_action()
        self.undo_in_progress = False



if __name__ == '__main__': 
    #Lock isn't quite the right word for it, it used to be a lock, we just want to see if there is already one running, and if there is, kill it so we can start our new one
    if os.path.isfile(lockfilepath):
        #Check if lock is stale
        with open(lockfilepath,'r') as lockfile:
            try:
                pid = int(lockfile.readline())
                os.kill(pid,signal.SIGKILL)
                killedpid, stat = os.waitpid(pid, os.WNOHANG)
                if killedpid == 0:
                    print "Failed to kill old process, exiting."
            except:
                pass

    with open(lockfilepath,'w') as lockfile:
        lockfile.write(str(os.getpid()))
    window = Notes(notes, notesfilepath)
    window.connect("delete-event", on_kill)
    window.connect("destroy", on_kill)
    window.show_all()
    Gtk.main()
    os.remove(lockfilepath)