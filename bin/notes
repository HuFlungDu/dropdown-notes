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
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(text)
        scrolledwindow.add(self.textview)
        self.add(scrolledwindow)
        #We write to the file every ten milliseconds so that the process can easilly be killed without losing any information
        GObject.timeout_add(10,self.write_text)
        self.connect("key-press-event", self.keypress)

    def keypress(self,window,event):
        if event.keyval == Gdk.KEY_Escape:
            self.destroy()

    def write_text(self):
        ''' Take the text from the buffer and write it to a file. Nothing special. '''
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        with open(self.filepath,'w') as notesfile:
            notesfile.write(self.textbuffer.get_text(start, end, False))
        return True

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