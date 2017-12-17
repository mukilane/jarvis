# Main File

# Assistant Dependencies
import argparse
import os.path
import json
import threading
import google.oauth2.credentials

from time import sleep
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

import commands

class MyAssistant(object):
    def __init__(self, window):
        self.window = window
        self._task = threading.Thread(target=self._run_task)
        self._can_start_conversation = True
        self._assistant = None
    
    def start(self):
        self._task.start()
    
    def _run_task(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument(
            '--credentials',
            type=existing_file,
            metavar='OAUTH2_CREDENTIALS_FILE',
            default=os.path.join(
                os.path.expanduser('~/.config'),
                'google-oauthlib-tool',
                'credentials.json'
            ),
            help='Path to store and read OAuth2 credentials')
        args = parser.parse_args()
        with open(args.credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None, **json.load(f))

        with Assistant(credentials) as assistant:
            self._assistant = assistant
            for event in assistant.start():
                self._process_event(event)

    def process_command(self, cmd):
        if cmd == 'google':
            commands.Sound('up')
            self._assistant.stop_conversation()
        elif cmd == 'sound down':
            commands.Sound('down')
            self._assistant.stop_conversation()
    
    def _process_event(self, event):

        if event.type == EventType.ON_START_FINISHED:
            self.window.printTranscript(event, 'LEFT')
        elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            self.window.printTranscript("Listening...", 'LEFT')
        elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
            self.window.printTranscript(event.args, 'RIGHT')
            # self.process_command(event.args['text'].lower())
        elif event.type == EventType.ON_RESPONDING_STARTED:
            self.window.printTranscript(event, 'LEFT')
        elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
            self.window.printTranscript("Done.", 'LEFT')
    
    def _on_button_pressed(self):
        if self._can_start_conversation:
            self._assistant.start_conversation()

class Exchange(Gtk.ListBoxRow):
    def __init__(self, data, align):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.label = Gtk.Label(data)
        if align == 'LEFT':
            self.label.set_justify(Gtk.Justification.LEFT)
        else:
            self.label.set_justify(Gtk.Justification.RIGHT)
        self.add(self.label)

# Main Window Class
class MyWindow(Gtk.Window):

    def __init__(self):

        # Window Configurations
        Gtk.Window.__init__(self, title="Jarvis")
        self.set_border_width(8)
        self.set_default_size(400, 500)
        self.set_icon_from_file("./assets/mic.png")
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = "Jarvis"
        self.set_titlebar(header)

        # Main Container
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.set_homogeneous(False)
        self.add(self.box)

        # Main List
        listcontainer = Gtk.ScrolledWindow()
        self.box.pack_start(listcontainer, True, True, 0)
        self.list = Gtk.ListBox()
        self.list.set_selection_mode(Gtk.SelectionMode.NONE)
        listcontainer.add(self.list)

        # Trigger
        self.button = Gtk.Button(label="Start")
        self.button.connect("clicked", self.on_button_clicked)
        Gtk.StyleContext.add_class(self.button.get_style_context(), "suggested-action")
        Gtk.StyleContext.add_class(self.button.get_style_context(), "circular")
        self.box.pack_start(self.button, False, False, 8)
       
    def on_button_clicked(self, widget):
        assistant._on_button_pressed()
        self.list.show_all()

    def printTranscript(self, text, align):
        exchange = Exchange(text, align)
        self.list.add(exchange)
        self.list.show_all()

    def showProgress(self):
        self.progressbar = Gtk.ProgressBar()
        self.box.pack_start(self.progressbar, True, True, 0)

    def do_delete_event(self, event):
        self.printTranscript('GoodBye', 'LEFT')
        sleep(2)
        return False


css = b"""
window.background {
    background: white;
}
headerbar, headerbar button { 
    background: white;
    color: black;
}
list {
    background: white;
    color: #333;
}
row {
    background: #eee;
    border-radius: 15px;
    padding: 6px;
    margin-bottom: 6px;
}

.button, .circular, .suggested-action {
    background: #546e7a;
}
"""

style_provider = Gtk.CssProvider()
style_provider.load_from_data(css)
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER
)

window = MyWindow()
window.show_all()
window.connect("destroy", Gtk.main_quit)
assistant = MyAssistant(window)
assistant.start()
Gtk.main()
