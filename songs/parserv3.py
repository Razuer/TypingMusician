import os
import librosa
import numpy as np

def extract_rhythm(file_path, threshold=0.2, freq_range=(200, 6000)):
    if not (os.path.splitext(file_path)[1] == '.wav'):
        return False
    else:
        # Wczytanie pliku dźwiękowego
        y, sr = librosa.load(file_path)

        # Obliczenie siły zaakcentowania dźwięków
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)

        # Analiza częstotliwościowa
        stft = librosa.stft(y)
        mag = np.abs(stft)
        freqs = librosa.fft_frequencies(sr=sr)
        freq_idx = np.where((freqs >= freq_range[0]) & (freqs <= freq_range[1]))[0]
        freq_mag_sum = np.sum(mag[freq_idx, :], axis=0)

        # Wyodrębnienie momentów rytmicznych na podstawie siły zaakcentowania i analizy częstotliwościowej
        combined_strength = onset_env * freq_mag_sum
        tempo, beat_frames = librosa.beat.beat_track(onset_envelope=combined_strength, sr=sr)

        # Konwersja ramki do czasu w milisekundach
        beat_times = librosa.frames_to_time(beat_frames, sr=sr) * 1000

        # Filtracja momentów rytmicznych na podstawie progu głośności
        beat_times_filtered = [beat_time for beat_time, strength in zip(beat_times, combined_strength[beat_frames]) if strength >= threshold]

        # Zapisanie wyników do pliku tekstowego
        output_file = f"{os.path.splitext(file_path)[0]}.txt"
        np.savetxt(output_file, beat_times_filtered, fmt='%d', delimiter='\n')

        print(f"Pomyślnie przetworzono plik i zapisano wyniki w {output_file}")
        return True
# Przykładowe użycie
file_path = 'songs/wav/shooting-stars.wav'
extract_rhythm(file_path, threshold=0.2, freq_range=(200, 6000))

