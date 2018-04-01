#!/usr/bin/env python2
"""
Small Python 2 script to reload GTK2 themes.

This uses Python2 since this requires 'send_clientmessage_toall()'
which isn't available in Python 3.

Original source: https://crunchbang.org/forums/viewtopic.php?id=39646
"""
try:
    import gtk
except ImportError:
    print("[ERROR] gtk_reload: GTK reload requires PyGTK.")
    exit(1)


def gtk_reload():
    """Reload GTK2 themes."""
    events = gtk.gdk.Event(gtk.gdk.CLIENT_EVENT)
    data = gtk.gdk.atom_intern("_GTK_READ_RCFILES", False)
    events.data_format = 8
    events.send_event = True
    events.message_type = data
    events.send_clientmessage_toall()


gtk_reload()
