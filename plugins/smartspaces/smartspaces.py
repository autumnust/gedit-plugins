# -*- coding: utf-8 -*-

#  smartspaces.py
#
#  Copyright (C) 2006 - Steve Frécinaux
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330,
#  Boston, MA 02111-1307, USA.

from gi.repository import GObject, Gtk, Gdk, GtkSource, Gedit

class SmartSpacesPlugin(GObject.Object, Gedit.ViewActivatable):
    __gtype_name__ = "SmartSpacesPlugin"

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self, view):
        self._view = view

        self._handlers = [
            None,
            view.connect('notify::editable', self.on_notify),
            view.connect('notify::insert-spaces-instead-of-tabs', self.on_notify)
        ]

    def do_deactivate(self, view):
        for handler in self._handlers:
            if handler is not None:
                self._view.disconnect(handler)

    def update_active(self):
        # Don't activate the feature if the buffer isn't editable or if
        # we're using tabs
        active = self._view.get_editable() and \
                 self._view.get_insert_spaces_instead_of_tabs()

        if active and self._handlers[0] is None:
            self._handlers[0] = self._view.connect('key-press-event',
                                                   self.on_key_press_event)
        elif not active and self._handlers[0] is not None:
            self._view.disconnect(self._handlers[0])
            self._handlers[0] = None

    def on_notify(self, view, pspec):
        self.update_active()

    def get_real_indent_width(self):
        indent_width = self._view.get_indent_width()

        if indent_width < 0:
             indent_width = self._view.get_tab_width()

        return indent_width

    def on_key_press_event(self, view, event):
        # Only take care of backspace and shift+backspace
        mods = Gtk.accelerator_get_default_mod_mask()

        if event.key.keyval != Gdk.BackSpace or \
           event.key.state & mods != 0 and event.key.state & mods != Gdk.ModifierType.SHIFT_MASK:
            return False

        doc = view.get_buffer()
        if doc.get_has_selection():
            return False

        cur = doc.get_iter_at_mark(doc.get_insert())
        offset = cur.get_line_offset()

        if offset == 0:
            # We're at the begining of the line, so we can't obviously
            # unindent in this case
            return False

        start = cur.copy()
        prev = cur.copy()
        prev.backward_char()

        # If the previous chars are spaces, try to remove
        # them until the previous tab stop
        max_move = offset % self.get_real_indent_width()

        if max_move == 0:
            max_move = self.get_real_indent_width()

        moved = 0
        while moved < max_move and prev.get_char() == ' ':
            start.backward_char()
            moved += 1
            if not prev.backward_char():
                # we reached the start of the buffer
                break

        if moved == 0:
            # The iterator hasn't moved, it was not a space
            return False

        # Actually delete the spaces
        doc.begin_user_action()
        doc.delete(start, cur)
        doc.end_user_action()

        return True

# ex:ts=4:et:
