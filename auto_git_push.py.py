from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import subprocess

# === Configuration ===
WATCHED_DIR = r"C:\Users\ASUS\pythonProject\python\main1.py"  # ✅ Folder to watch
GIT_BRANCH = "main"
GIT_REMOTE = "origin"  # Usually 'origin'


class AutoGitHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"[INFO] File modified: {event.src_path}")
            try:
                os.chdir(WATCHED_DIR)

                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", f"Auto update at {time.ctime()}"], check=True)
                subprocess.run(["git", "push", GIT_REMOTE, GIT_BRANCH], check=True)

                print(f"[SUCCESS] Changes pushed to {GIT_REMOTE}/{GIT_BRANCH}")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Git command failed:\n{e}")
            except Exception as ex:
                print(f"[ERROR] Unexpected error:\n{ex}")


# === Start Watching ===
if __name__ == "__main__":
    observer = Observer()
    observer.schedule(AutoGitHandler(), path=WATCHED_DIR, recursive=True)
    observer.start()
    print(f"[INFO] Watching: {WATCHED_DIR} ... Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
