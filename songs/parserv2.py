import librosa
import numpy as np
import os 

def extract_rhythm(file_path, threshold=0.2):
    # Wczytanie pliku dźwiękowego
    y, sr = librosa.load(file_path)

    # Obliczenie siły zaakcentowania dźwięków
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # Wyodrębnienie momentów rytmicznych na podstawie siły zaakcentowania
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    # Konwersja ramki do czasu w milisekundach
    beat_times = librosa.frames_to_time(beat_frames, sr=sr) * 1000

    # Filtracja momentów rytmicznych na podstawie progu głośności
    beat_times_filtered = [beat_time for beat_time, strength in zip(beat_times, onset_env[beat_frames]) if strength >= threshold]

    # Zapisanie wyników do pliku tekstowego
    output_file = f"{os.path.splitext(file_path)[0]}.txt"
    np.savetxt(output_file, beat_times_filtered, fmt='%d', delimiter='\n')

    print(f"Pomyślnie przetworzono plik i zapisano wyniki w {output_file}")

# Przykładowe użycie
file_path = 'songs/wav/fashion_beats.wav'
extract_rhythm(file_path, threshold=9)
