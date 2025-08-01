from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import subprocess

WATCH_DIR = r"C:\Users\ASUS\pythonProject\python"

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_commit_time = 0

    def on_modified(self, event):
        if event.is_directory:
            return

        # Ignore changes in .git directory and temp/backup files
        if ".git" in event.src_path or event.src_path.endswith("~"):
            return

        print(f"[INFO] Detected change in: {event.src_path}")

        # Only attempt to commit once every 5 seconds max
        if time.time() - self.last_commit_time < 5:
            return

        os.chdir(WATCH_DIR)
        try:
            subprocess.run(["git", "add", "."], check=True)

            # Check if there are staged changes before committing
            status_output = subprocess.check_output(["git", "status", "--porcelain"]).decode()
            if not status_output.strip():
                print("[INFO] No changes to commit.")
                return

            subprocess.run(["git", "commit", "-m", f"Auto update at {time.ctime()}"], check=True)
            subprocess.run(["git", "pull", "--rebase"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)

            print("[SUCCESS] Changes pushed to GitHub.")
            self.last_commit_time = time.time()

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Git command failed: {e}")

if __name__ == "__main__":
    print(f"[INFO] Watching for changes in: {WATCH_DIR}")
    observer = Observer()
    observer.schedule(ChangeHandler(), path=WATCH_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
