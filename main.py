# main.py
# The main entry point for The Eye of Babel application.

import file_watcher

if __name__ == "__main__":
    try:
        file_watcher.setup_folders()
        file_watcher.watch_folder()
    except KeyboardInterrupt:
        print("\nScript stopped by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
