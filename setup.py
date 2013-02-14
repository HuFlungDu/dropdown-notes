from distutils.core import setup
try:
    from gi.repository import Gtk, Gdk, GObject

    setup(
        name="notes",
        version='0.1',
        scripts=["bin/notes"]
    )
except:
    print "GTK3/Gobject introspection requirements not met, please install GTK3/GObject introspection before installing this program."