import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartServerHandler(FileSystemEventHandler):
    def __init__(self, server_process):
        self.server_process = server_process

    def on_modified(self, event):
        if event.src_path.endswith((".html", ".css", ".js")):  # Watch specific file types
            print(f"Detected change in {event.src_path}. Restarting server...")
            self.server_process.terminate()  # Stop the server
            time.sleep(1)  # Give it a moment to release the port
            self.server_process = subprocess.Popen([sys.executable, "-m", "http.server"])
            print("Server restarted.")

if __name__ == "__main__":
    server_process = subprocess.Popen([sys.executable, "-m", "http.server"])
    event_handler = RestartServerHandler(server_process)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    print("Watching for file changes. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        server_process.terminate()

    observer.join()
