import os
import librosa
import numpy as np

def extract(file_path):
    # Wczytanie pliku dźwiękowego
    y, sr = librosa.load(file_path)

    # Wyszukanie charakterystycznego fragmentu dźwięku
    # Dostosuj te wartości do swoich potrzeb
    characteristic_instrument = "fortepian"
    characteristic_duration = 0.5  # w sekundach

    # Konwersja czasu na milisekundy
    characteristic_duration_ms = int(characteristic_duration * 1000)

    # Przeliczenie próbek na czas w milisekundach
    frame_ms = 1000 / sr
    characteristic_duration_frames = int(characteristic_duration_ms / frame_ms)

    # Wyszukanie indeksu początkowego fragmentu dźwięku
    # przy użyciu podobieństwa widma
    y_stft = librosa.stft(y)
    characteristic_index = np.argmax(np.mean(np.abs(y_stft), axis=0))

    # Obliczenie czasu pojawienia się dźwięków w milisekundach
    timestamps = []
    for i in range(len(y)):
        if i % characteristic_index == 0:
            timestamps.append(int(i * frame_ms))

    # Zapisanie wyników do pliku txt
    output_file = f"{os.path.splitext(file_path)[0]}.txt"
    with open(output_file, "w") as f:
        for timestamp in timestamps:
            f.write(str(timestamp) + "\n")

    print("Przetwarzanie zakończone. Wyniki zapisane w pliku:", output_file)

file_path = 'songs/wav/fashion_beats.wav'
extract(file_path)