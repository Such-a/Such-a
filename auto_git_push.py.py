from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import subprocess

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"[INFO] Detected change in: {event.src_path}")
            os.chdir(r"C:\Users\ASUS\pythonProject\python")
            try:
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", f"Auto update at {time.ctime()}"], check=True)
                subprocess.run(["git", "pull", "--rebase"], check=True)
                subprocess.run(["git", "push", "origin", "main"], check=True)
                print("[SUCCESS] Changes pushed to GitHub.")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Git command failed: {e}")

if __name__ == "__main__":
    watch_path = r"C:\Users\ASUS\pythonProject\python"
    print(f"[INFO] Watching for changes in: {watch_path}")
    observer = Observer()
    observer.schedule(ChangeHandler(), path=watch_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
