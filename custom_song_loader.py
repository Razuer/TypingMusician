import os
import tkinter
from tkinter import filedialog
import librosa
import numpy as np

def extract_rhythm(file_path):
    # Wczytaj plik muzyczny
      # Podaj ścieżkę do swojego pliku dźwiękowego
    y, sr = librosa.load(file_path)
    
    # Wyodrębnij główną melodię przy użyciu transformacji częstotliwościowej
    onset_times = librosa.onset.onset_detect(y=y, sr=sr, backtrack=False)

    # Convert onset times to milliseconds
    onset_times_ms = librosa.frames_to_time(onset_times, sr=sr) * 1000

    # Print onset times of each note in melody line
    onset_times_ms = [round(onset) for onset in onset_times_ms]

    output_file = f"{os.path.splitext(file_path)[0]}.txt"

    np.savetxt(output_file, onset_times_ms, fmt='%d', delimiter='\n')
    print(f"Pomyślnie przetworzono plik i zapisano wyniki w {output_file}")

if __name__ == "__main__":
    root = tkinter.Tk()

    root.withdraw()

    song_path = filedialog.askopenfilename(initialdir="songs", filetypes=[("MP3 and WAV files", "*.mp3;*.wav"),("MP3 files", "*.mp3"), ("WAV files", "*.wav")])

    if song_path:
        extract_rhythm(song_path)
    else:
        print("File was not selected")