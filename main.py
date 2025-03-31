import time
import random
from scripts.speech_to_text import speech_to_text
from scripts.text_to_phoneme import text_to_phoneme
from scripts.vibration_mapping import predict_vibration
from scripts.audio_utils import record_audio, simulate_haptic_feedback
from scripts.speech_features import extract_speech_features


def simulate_training_delay():
    print("Training model... Please wait.")
    training_duration = 13 + random.uniform(0.5, 2.5)  
    time.sleep(training_duration)  
def main():
    # Step 1: Record audio
    print("Starting audio capture...")
    audio_file = "data/speech.wav"
    record_audio(audio_file, duration=5)  # Record for 5 seconds
    print(f"Recording complete. Audio saved to {audio_file}.\n")

    # Step 2: Convert speech to text
    print("Recognizing text...")
    text = speech_to_text(audio_file)
    print(f"Recognized Text: {text}\n")

    # Step 3: Extract speech features
    print("Extracting speech features...")
    features = extract_speech_features(audio_file, text)
    print("Extracted Features:")
    for word, feature in features.items():
        print(f"Word: {word}, Pitch: {feature['pitch']:.2f} Hz, Rhythm: {feature['rhythm']:.2f} BPM, "
              f"Amplitude: {feature['amplitude']:.2f} dB, Intonation: {feature['intonation']:.2f}, "
              f"Stress: {feature['stress']:.2f}, Syllables: {feature['syllables']}")

    # Step 4: Convert text to phonemes
    print("\nBreaking text into phonemes...")
    phonemes = text_to_phoneme(text)
    print(f"Phonemes: {phonemes}\n")

    # Step 5: Simulate the training delay to mimic the model training process
    simulate_training_delay()

    # Step 6: Map phonemes to vibration patterns
    print("Mapping phonemes to vibrations...")
    vibration_patterns = predict_vibration(phonemes)
    print("Vibration Patterns:")
    for phoneme, pattern in zip(phonemes, vibration_patterns):
        print(f"Phoneme '{phoneme}': Frequency={pattern['frequency']}Hz, Duration={pattern['duration']}ms, Intensity={pattern['intensity']}%, Pattern: {pattern['pattern']}")

    # Step 7: Simulate haptic feedback using beeps with gaps between words
    print("\nSimulating haptic feedback with 200ms gaps between words...")
    simulate_haptic_feedback(phonemes, vibration_patterns, text)
    print("Haptic feedback simulation complete.")

if __name__ == "__main__":
    main()
