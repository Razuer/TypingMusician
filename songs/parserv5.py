import os
import librosa
import numpy as np
import soundfile as sf
from spleeter.separator import Separator

def extract_rhythm(file_path):
    # Wczytaj plik muzyczny
      # Podaj ścieżkę do swojego pliku dźwiękowego
    y, sr = librosa.load(file_path)

    temp_file = 'temp.wav'
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(temp_file, 'output/')
    sf.write(temp_file, y, sr)
    # Load the separated vocal track into memory
    vocal_file = 'output/temp/vocals.wav'
    y_vocal, sr_vocal = librosa.load(vocal_file)
    vocal_file_trimmed = 'vocals_trimmed.mp3'
    sf.write(vocal_file_trimmed, y_vocal, sr_vocal)

    os.remove(temp_file)
    os.rmdir('output/temp')

    # Wyodrębnij główną melodię przy użyciu transformacji częstotliwościowej
    onset_times = librosa.onset.onset_detect(y=y_vocal, sr=sr_vocal)

    # Convert onset times to milliseconds
    onset_times_ms = librosa.frames_to_time(onset_times, sr=sr_vocal) * 1000

    # Print onset times of each note in melody line
    onset_times_ms = [round(onset) for onset in onset_times_ms]
    
    output_file = f"{os.path.splitext(file_path)[0]}.txt"

    np.savetxt(output_file, onset_times_ms, fmt='%d', delimiter='\n')
    print(f"Pomyślnie przetworzono plik i zapisano wyniki w {output_file}")

audio_path = 'songs/wav/shooting-stars.wav'
extract_rhythm(audio_path)