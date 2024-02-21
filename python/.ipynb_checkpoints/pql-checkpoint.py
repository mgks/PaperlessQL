import json
import os
import uuid
import datetime
from functions import img_to_blob

class PQLDatabase:
    """Represents the database for storing and managing notes."""

    def __init__(self, notes_directory, logs_directory="logs"):
        """Initializes the database with directories for notes and logs."""
        self.notes_directory = notes_directory
        self.logs_directory = logs_directory
        os.makedirs(notes_directory, exist_ok=True)
        os.makedirs(logs_directory, exist_ok=True)

    # ... (Implementation of other database methods)

    def _log_error(self, message):
        """Logs an error message to a date-stamped file."""
        error_file = os.path.join(self.logs_directory, f"errors_{datetime.date.today()}.log")
        with open(error_file, "a") as f:
            f.write(f"{datetime.datetime.now()}: {message}\n")

class PQL:
    """Encapsulates the database and provides high-level methods."""

    def __init__(self, notes_directory, logs_directory="logs"):
        """Initializes the PQL object with the database."""
        self.db = PQLDatabase(notes_directory, logs_directory)

    def push_image(self, image_path, name=None):
        """Stores an image as a note."""
        try:
            blob = img_to_blob(image_path)
            note_name = self.db.create_note(blob, name)
            print(f"Image stored as note: {note_name}")
        except Exception as e:
            print(f"Error storing image: {e}")
