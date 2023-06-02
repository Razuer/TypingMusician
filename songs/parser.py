import librosa
import numpy as np
import os 

def extract_rhythm(file_path):
    # Wczytanie pliku dźwiękowego
    y, sr = librosa.load(file_path)

    # Ekstrakcja tempa i akcentów rytmicznych
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # Konwersja ramki do czasu w milisekundach
    beat_times = librosa.frames_to_time(beat_frames, sr=sr) * 1000

    # Zapisanie wyników do pliku tekstowego
    output_file = f"{os.path.basename(file_path).split('.')[0]}.txt"
    np.savetxt(output_file, beat_times, fmt='%d', delimiter='\n')

    print(f"Pomyślnie przetworzono plik i zapisano wyniki w {output_file}")

# Przykładowe użycie
file_path = 'songs/wav/fashion_beats.wav'
extract_rhythm(file_path)
