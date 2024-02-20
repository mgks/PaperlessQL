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
        os.makedirs(notes_directory, exist_ok=True)  # Create directories if they don't exist
        os.makedirs(logs_directory, exist_ok=True)

    def _validate_filename(self, name):
        valid_chars = set("abcdefghijklmnopqrstuvwxyz0123456789_-.")
        if not all(char in valid_chars for char in name):
            raise ValueError(f"Invalid characters in note name: {name}")

    def create_note(self, content, name=None):
        if name:
            self._validate_filename(name)
        try:
            if not name:
                name = str(uuid.uuid4())  # Generate unique name if not provided
            note_file = os.path.join(self.notes_directory, f"{name}.json")
            with open(note_file, "w") as f:
                json.dump({"content": content}, f)
            return name  # Return the note name for reference
        except Exception as e:
            self._log_error(f"Error creating note: {e}")
            raise

    def read_note(self, name):
        note_file = os.path.join(self.notes_directory, f"{name}.json")
        try:
            with open(note_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Note '{name}' not found")

    def update_note(self, name, content):
        note_file = os.path.join(self.notes_directory, f"{name}.json")
        with open(note_file, "w") as f:
            json.dump({"content": content}, f)

    def delete_note(self, name):
        note_file = os.path.join(self.notes_directory, f"{name}.json")
        os.remove(note_file)

    def list_notes(self):
        note_files = os.listdir(self.notes_directory)
        return [os.path.splitext(f)[0] for f in note_files if f.endswith(".json")]

    def search_notes(self, query):
        results = []
        for note_name in self.list_notes():
            note = self.read_note(note_name)
            if query.lower() in note["content"].lower():
                results.append(note)
        return results

    def _log_error(self, message):
        """Logs an error message to a date-stamped file."""
        error_file = os.path.join(self.logs_directory, f"errors_{datetime.date.today()}.log")
        with open(error_file, "a") as f:  # Append to the log file
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

