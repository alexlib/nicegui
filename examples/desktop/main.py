#!/usr/bin/env python3
import multiprocessing
import os
import signal
import tempfile
import webview  # pip install webview
from nicegui import ui

ui.button('button', on_click=lambda: ui.notify('Nice!'))


def open_window(event):
    window = webview.create_window('NiceGUI', url='http://localhost:8080')
    window.events.closing += event.set  # signal that the program should be closed to the main process
    webview.start(storage_path=tempfile.mkdtemp())

# create shutdown event for inter process communication
shutdown = multiprocessing.Event()
#  repeatedly check if the program should be terminated
ui.timer(0.1, lambda: os.kill(os.getpgid(os.getpid()), signal.SIGTERM) if shutdown.is_set() else None)
# start webview in a subprocess once when the program starts (not when uvicorn parses the file again with __name__ == '__mp_main__')
if __name__ == "__main__":
    multiprocessing.Process(target=open_window, args=(shutdown,), daemon=False).start()

ui.run(show=False)