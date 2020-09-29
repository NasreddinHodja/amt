import os

import urwid

choices = os.listdir('/mnt/nasHDD/manga/')

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]

    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.appen(urwid.AttrMap(button, None, focus_map='reversed'))

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    response = urwid.Text([u'You choose', choice, u'\n'])
    done = urvid.Button(u'Ok')
    urwid.connect_signal(done, 'click', exit_program)
    main.original_widget = urwid.Filler(urwid.Pile([response,
                                                    urwid.AttrMap(done,
                                                                  None,
                                                                  focus_map='reversed')]))
