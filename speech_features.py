import librosa
import numpy as np

def extract_speech_features(audio_file, text):
    """
    Extract speech features (pitch, rhythm, amplitude, etc.) for each word in the text.
    """
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)
    
    # Split the text into words
    words = text.split()
    
    # Initialize a dictionary to store features for each word
    features = {}
    
    # Calculate the duration of each word in the audio
    word_durations = len(y) / len(words)  # Approximate duration of each word
    
    for i, word in enumerate(words):
        # Extract a segment of the audio corresponding to the word
        start = int(i * word_durations)
        end = int((i + 1) * word_durations)
        y_word = y[start:end]
        
        # Extract features for the word
        pitch = librosa.yin(y_word, fmin=50, fmax=500)  # Extract pitch (fundamental frequency)
        tempo, _ = librosa.beat.beat_track(y=y_word, sr=sr)  # Extract rhythm (tempo)
        amplitude = librosa.amplitude_to_db(np.abs(librosa.stft(y_word)))  # Extract amplitude
        intonation = np.std(pitch)  # Intonation as pitch variability
        stress = np.mean(amplitude)  # Stress as average amplitude
        syllables = len(librosa.effects.split(y_word, top_db=30))  # Approximate syllable count
        
        # Ensure all feature values are scalar (single values)
        pitch_mean = float(np.mean(pitch))
        tempo_mean = float(tempo)
        amplitude_mean = float(np.mean(amplitude))
        intonation_mean = float(intonation)
        stress_mean = float(stress)
        syllables_mean = int(syllables)
        
        # Store features for the word
        features[word] = {
            "pitch": pitch_mean,
            "rhythm": tempo_mean,
            "amplitude": amplitude_mean,
            "intonation": intonation_mean,
            "stress": stress_mean,
            "syllables": syllables_mean
        }
    
    return features

if __name__ == "__main__":
    audio_file = "data/speech.wav"
    text = "hello my name is Manu"
    features = extract_speech_features(audio_file, text)
    print(features)