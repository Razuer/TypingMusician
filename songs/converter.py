import py_midicsv as pm
import tkinter as tk
from tkinter import filedialog
import os

# Define the function to convert MIDI files to CSV
def convert_to_csv(midi_path):
    # Load the MIDI file and parse it into CSV format
    csv_string = pm.midi_to_csv(midi_path)

    # Set the output file name and path
    csv_file = f"songs/csv/{os.path.basename(midi_path).split('.')[0]}.csv"

    # Write the CSV string to the output file
    with open(csv_file, "w") as f:
        f.write(csv_string)

# Create the main Tkinter window
root = tk.Tk()

# Hide the main window since we don't need it
root.withdraw()

# Get the current working directory
current_directory = os.getcwd()

# Display a file dialog for selecting MIDI files in the current directory
midi_path = filedialog.askopenfilename(initialdir=current_directory, filetypes=[("MIDI files", "*.mid")])

if midi_path:
    # Convert the selected MIDI file to CSV
    convert_to_csv(midi_path)
