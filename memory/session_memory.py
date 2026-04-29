import json
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path

# --- Configuration Constants ---
# Base directory for all memory files. Created if it doesn't exist.
BASE_DIR = Path("memory")
# Path for the structured session log.
SESSION_LOG_PATH = BASE_DIR / "session_log.json"
# Path for critical facts migrated from the session log.
LONG_TERM_MEMORY_PATH = BASE_DIR / "long_term_memory.json"
# Path for the current actively managed session data (e.g., variables, user state).
CURRENT_SESSION_STATE_PATH = BASE_DIR / "current_session_state.json"

# Log entries older than this duration will be cleaned up.
SESSION_LOG_EXPIRATION_DAYS = 3
# Interval for the background thread to automatically save the session state.
AUTO_SAVE_INTERVAL_MINUTES = 20

class SessionManager:
    """
    Manages session memory, logging, automatic saving, and long-term memory migration.

    This class provides a comprehensive system for:
    - Storing and retrieving dynamic session-specific data.
    - Logging structured events with timestamps.
    - Automatically saving the session state and logs at regular intervals.
    - Cleaning up expired log entries.
    - Migrating "critical facts" from expired log entries to a separate long-term memory store.
    - Handling file I/O with JSON serialization and pathlib.
    - Ensuring thread safety for shared data access.
    """

    def __init__(self, auto_save_interval_minutes: int = AUTO_SAVE_INTERVAL_MINUTES):
        """
        Initializes the SessionManager, loads existing data, and starts the auto-save thread.

        Args:
            auto_save_interval_minutes: The interval in minutes for automatic saving.
        """
        # Ensure the base directory for memory files exists.
        self._ensure_directory()

        # Initialize internal data structures to hold session state and logs.
        self.session_data: dict = {}      # Dictionary for current, active session data.
        self.session_log: list = []       # List of structured log entries.
        self.long_term_memory: list = []  # List of critical facts migrated from logs.

        # Threading components for concurrency control and background tasks.
        self._lock = threading.Lock()           # Lock to protect shared resources.
        self._stop_event = threading.Event()    # Event to signal the auto-save thread to stop.
        self._auto_save_thread = None           # Reference to the auto-save background thread.
        self._auto_save_interval_minutes = auto_save_interval_minutes

        # Load existing data from files when the manager starts.
        self._load_all_data()

        # Start the background thread responsible for automatic saving.
        self._start_auto_save_thread()

    def _ensure_directory(self):
        """Creates the base directory for memory files if it doesn't already exist."""
        try:
            BASE_DIR.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            # Handle potential OS errors during directory creation (e.g., permissions).
            print(f"Error creating memory directory '{BASE_DIR}': {e}")
            # In a production system, this might warrant raising a critical error or logging.

    def _load_json_file(self, path: Path) -> list | dict:
        """
        Helper method to load JSON data from a given file path.

        Args:
            path: The pathlib.Path object pointing to the JSON file.

        Returns:
            The loaded data (list or dict) or an empty list/dict if the file
            does not exist, is empty, or is corrupted.
        """
        # Return appropriate empty structure if file doesn't exist.
        if not path.exists():
            return [] if path == SESSION_LOG_PATH or path == LONG_TERM_MEMORY_PATH else {}

        try:
            with path.open("r", encoding="utf-8") as f:
                # Handle empty file case gracefully.
                content = f.read()
                if not content.strip():
                    return [] if path == SESSION_LOG_PATH or path == LONG_TERM_MEMORY_PATH else {}
                f.seek(0) # Reset file pointer if read above
                return json.load(f)
        except json.JSONDecodeError as e:
            # Log a warning if the JSON file is malformed.
            print(f"Warning: JSON decode error in '{path}'. File might be corrupted. {e}")
            # Return an empty structure to prevent application crash.
            return [] if path == SESSION_LOG_PATH or path == LONG_TERM_MEMORY_PATH else {}
        except IOError as e:
            # Log other file I/O errors.
            print(f"Error reading file '{path}': {e}")
            return [] if path == SESSION_LOG_PATH or path == LONG_TERM_MEMORY_PATH else {}

    def _save_json_file(self, path: Path, data: list | dict):
        """
        Helper method to save data to a JSON file path.

        Args:
            path: The pathlib.Path object pointing to the JSON file.
            data: The list or dictionary to be serialized and saved.
        """
        try:
            with path.open("w", encoding="utf-8") as f:
                # Use indent for readability and ensure non-ASCII characters are handled.
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            # Log file writing errors.
            print(f"Error writing to file '{path}': {e}")
            # Consider more robust error handling like a retry mechanism or critical log in a real system.

    def _load_all_data(self):
        """Loads all memory components (session data, log, long-term memory) from disk."""
        with self._lock:  # Acquire lock to ensure data consistency during initial load.
            self.session_log = self._load_json_file(SESSION_LOG_PATH)
            self.long_term_memory = self._load_json_file(LONG_TERM_MEMORY_PATH)
            self.session_data = self._load_json_file(CURRENT_SESSION_STATE_PATH)
            print(f"[{datetime.now().isoformat()}] Loaded {len(self.session_log)} session log entries.")
            print(f"[{datetime.now().isoformat()}] Loaded {len(self.long_term_memory)} long-term memory entries.")
            print(f"[{datetime.now().isoformat()}] Loaded {len(self.session_data)} session data entries.")

    def _start_auto_save_thread(self):
        """Initiates the background thread responsible for periodic auto-saving."""
        # Prevent starting multiple auto-save threads.
        if self._auto_save_thread is None or not self._auto_save_thread.is_alive():
            # Create a daemon thread so it doesn't prevent program exit.
            self._auto_save_thread = threading.Thread(target=self._auto_save_worker, daemon=True)
            self._auto_save_thread.start()
            print(f"[{datetime.now().isoformat()}] Auto-save thread started, saving every {self._auto_save_interval_minutes} minutes.")

    def _auto_save_worker(self):
        """The target function executed by the background auto-save thread."""
        while not self._stop_event.is_set():
            # Wait for the specified interval or until the stop event is triggered.
            # `wait()` returns True if event is set, False if timeout.
            self._stop_event.wait(self._auto_save_interval_minutes * 60)
            if not self._stop_event.is_set(): # Only proceed if the stop event was not set during wait.
                print(f"[{datetime.now().isoformat()}] Auto-saving session state and running cleanup...")
                self.save_current_state() # Save active session data and log.
                self.cleanup_and_migrate() # Also run cleanup and migration on auto-save cycles.

    def save_current_state(self):
        """
        Manually saves the current session data and session log to their respective files.
        This method is thread-safe.
        """
        with self._lock:  # Acquire lock to prevent race conditions during file write.
            self._save_json_file(CURRENT_SESSION_STATE_PATH, self.session_data)
            self._save_json_file(SESSION_LOG_PATH, self.session_log)
            # Long-term memory is primarily saved after cleanup/migration,
            # but can be explicitly saved here too if its state changes independently.
            # self._save_json_file(LONG_TERM_MEMORY_PATH, self.long_term_memory)
            print(f"[{datetime.now().isoformat()}] Session state and log saved successfully.")

    def add_session_data(self, key: str, value: any):
        """
        Adds or updates a piece of data within the current session state.
        A log event is also recorded for this update. This method is thread-safe.
        """
        with self._lock:
            self.session_data[key] = value
            # Log the change in session data for traceability.
            self.log_event("SESSION_DATA_UPDATE", f"Key '{key}' updated.", data={key: value})

    def get_session_data(self, key: str, default: any = None) -> any:
        """
        Retrieves a piece of data from the current session state.
        This method is thread-safe.

        Args:
            key: The key of the data to retrieve.
            default: The value to return if the key is not found.

        Returns:
            The value associated with the key, or the default value if not found.
        """
        with self._lock:
            return self.session_data.get(key, default)

    def log_event(self, event_type: str, message: str, is_critical: bool = False, **kwargs):
        """
        Logs a structured event to the session log.

        Args:
            event_type: A string identifying the type of event (e.g., "USER_ACTION", "ERROR").
            message: A human-readable description of the event.
            is_critical: If True, this log entry is marked as a critical fact for potential
                         migration to long-term memory upon cleanup.
            **kwargs: Additional arbitrary key-value pairs to include in the log entry.
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),  # ISO 8601 format for easy parsing.
            "event_type": event_type,
            "message": message,
            "is_critical_fact": is_critical,  # Flag to indicate if this entry should be migrated.
            **kwargs  # Embed any extra context provided.
        }
        with self._lock:
            self.session_log.append(log_entry)
            print(f"[{datetime.now().isoformat()}] Logged event: [{event_type}] {message}")
            # For high-frequency logging, relying on auto-save is better than immediate save.
            # If immediate persistence of logs is critical, uncomment the line below.
            # self._save_json_file(SESSION_LOG_PATH, self.session_log)

    def cleanup_and_migrate(self):
        """
        Cleans up expired log entries from `session_log.json` and migrates
        critical facts (marked with `is_critical_fact=True`) to `long_term_memory.json`.
        This method is thread-safe.
        """
        with self._lock:
            now = datetime.now()
            # Calculate the cutoff timestamp for log expiration.
            expiration_cutoff = now - timedelta(days=SESSION_LOG_EXPIRATION_DAYS)

            new_session_log = []
            migrated_count = 0
            cleaned_up_count = 0

            for entry in self.session_log:
                try:
                    entry_timestamp_str = entry.get("timestamp")
                    if not entry_timestamp_str:
                        # If a log entry lacks a timestamp, it's malformed. Keep it for inspection.
                        new_session_log.append(entry)
                        print(f"Warning: Log entry without timestamp found and retained: {entry}")
                        continue

                    # Parse the timestamp from the log entry string.
                    entry_timestamp = datetime.fromisoformat(entry_timestamp_str)

                    if entry_timestamp < expiration_cutoff:
                        # This log entry has expired.
                        if entry.get("is_critical_fact", False):
                            # If marked as critical, move it to long-term memory.
                            self.long_term_memory.append(entry)
                            migrated_count += 1
                        cleaned_up_count += 1
                    else:
                        # Keep non-expired entries in the session log.
                        new_session_log.append(entry)
                except ValueError as e:
                    # Handle cases where timestamp string is malformed and cannot be parsed.
                    print(f"Warning: Could not parse timestamp in log entry: {entry}. Error: {e}")
                    new_session_log.append(entry) # Retain malformed entries to prevent data loss.

            self.session_log = new_session_log  # Update the session log with non-expired entries.

            # Save both long-term memory and the cleaned-up session log to disk.
            self._save_json_file(LONG_TERM_MEMORY_PATH, self.long_term_memory)
            self._save_json_file(SESSION_LOG_PATH, self.session_log)

            if cleaned_up_count > 0 or migrated_count > 0:
                print(f"[{now.isoformat()}] Cleanup complete: {cleaned_up_count} entries removed from session log, {migrated_count} critical facts migrated to long-term memory.")
            else:
                print(f"[{now.isoformat()}] Cleanup performed: No expired or critical facts found for migration.")
            
    def stop_auto_save(self):
        """
        Stops the background auto-save thread gracefully.
        Signals the thread to stop and waits for it to finish its current cycle.
        """
        if self._auto_save_thread and self._auto_save_thread.is_alive():
            self._stop_event.set()  # Signal the thread to terminate.
            self._auto_save_thread.join()  # Wait for the thread to complete its execution.
            print(f"[{datetime.now().isoformat()}] Auto-save thread stopped.")

    def __enter__(self):
        """Enables the SessionManager to be used as a context manager (`with` statement)."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensures resources are cleaned up (auto-save thread stopped) and a final state
        is saved when exiting the context manager block.
        """
        print(f"[{datetime.now().isoformat()}] Exiting SessionManager context. Performing final save and cleanup.")
        self.save_current_state()      # Perform a final save of the session state.
        self.cleanup_and_migrate()     # Run one last cleanup and migration.
        self.stop_auto_save()          # Stop the auto-save background thread.
        print(f"[{datetime.now().isoformat()}] SessionManager gracefully shut down.")

# --- Public API Functions for loading (as per description request) ---

def load_session_log() -> list:
    """
    Loads and returns the raw session log entries from 'memory/session_log.json'.
    This function is intended for manual loading at session start or for inspection.
    """
    # Create a temporary SessionManager instance to leverage its file loading helpers.
    # Set a very small auto_save_interval to ensure its thread starts and can be stopped quickly,
    # though ideally, these functions would interact with an already running SessionManager instance.
    temp_manager = SessionManager(auto_save_interval_minutes=0.01)
    try:
        log_data = temp_manager._load_json_file(SESSION_LOG_PATH)
        print(f"[{datetime.now().isoformat()}] Manually loaded {len(log_data)} session log entries from {SESSION_LOG_PATH}.")
        return log_data
    finally:
        # Ensure the temporary manager's thread is stopped to prevent resource leaks.
        temp_manager.stop_auto_save()

def load_long_term_memory() -> list:
    """
    Loads and returns the raw long-term memory entries from 'memory/long_term_memory.json'.
    This function is intended for manual loading at session start or for inspection.
    """
    # Create a temporary SessionManager instance to leverage its file loading helpers.
    temp_manager = SessionManager(auto_save_interval_minutes=0.01)
    try:
        ltm_data = temp_manager._load_json_file(LONG_TERM_MEMORY_PATH)
        print(f"[{datetime.now().isoformat()}] Manually loaded {len(ltm_data)} long-term memory entries from {LONG_TERM_MEMORY_PATH}.")
        return ltm_data
    finally:
        # Ensure the temporary manager's thread is stopped to prevent resource leaks.
        temp_manager.stop_auto_save()