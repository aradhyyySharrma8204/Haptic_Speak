import time
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

def record_audio(filename, duration=5, sample_rate=16000):
    """
    Record audio from the microphone and save it as a .wav file.
    
    Args:
        filename (str): Path to save the recorded audio.
        duration (int): Duration of the recording in seconds.
        sample_rate (int): Sampling rate of the audio.
    """
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    wav.write(filename, sample_rate, audio)  # Save the recording as a .wav file
    print(f"Audio saved to {filename}")

def generate_pattern_sound(pattern, frequency, duration, intensity):
    """
    Generate a sound based on the pattern description using sounddevice.
    
    Args:
        pattern (str): The pattern description (e.g., "1 short pulse", "2 sharp pulses", "wavy vibration").
        frequency (int): The frequency of the sound in Hz.
        duration (int): The duration of the sound in milliseconds.
        intensity (int): The intensity of the sound as a percentage.
    
    Returns:
        np.array: The generated sound waveform.
    """
    sample_rate = 44100  # Standard sample rate
    t = np.linspace(0, duration / 1000, int(sample_rate * duration / 1000), endpoint=False)
    
    if pattern == "1 short pulse":
        # Single short beep
        waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    elif pattern == "2 short pulses":
        # Two short beeps with a gap in between
        beep_duration = duration // 3
        gap_duration = duration // 3
        t1 = np.linspace(0, beep_duration / 1000, int(sample_rate * beep_duration / 1000), endpoint=False)
        t2 = np.linspace(0, beep_duration / 1000, int(sample_rate * beep_duration / 1000), endpoint=False)
        beep1 = 0.5 * np.sin(2 * np.pi * frequency * t1)
        gap = np.zeros(int(sample_rate * gap_duration / 1000))
        beep2 = 0.5 * np.sin(2 * np.pi * frequency * t2)
        waveform = np.concatenate((beep1, gap, beep2))
    
    elif pattern == "Wavy vibration":
        # Wavy vibration (modulated intensity)
        waveform = 0.5 * np.sin(2 * np.pi * frequency * t) * np.sin(2 * np.pi * 5 * t)
    
    elif pattern == "Rolling vibration":
        # Rolling vibration (modulated frequency)
        waveform = 0.5 * np.sin(2 * np.pi * frequency * t * np.sin(2 * np.pi * 5 * t))
    
    else:
        # Default to a simple beep
        waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    # Adjust intensity
    waveform = waveform * (intensity / 100)
    return waveform

def simulate_haptic_feedback(phonemes, vibration_patterns, text):
    """
    Simulate haptic feedback using sounddevice with a 200ms gap between words.
    
    Args:
        phonemes (list): List of phonemes.
        vibration_patterns (list): List of dictionaries containing 'frequency', 'duration', 'intensity', and 'pattern'.
        text (str): The original text to group phonemes by words.
    """
    # Split the text into words
    words = text.split()
    
    # Group phonemes and vibration patterns by words
    phoneme_groups = []
    vibration_groups = []
    start = 0
    for word in words:
        # Count the number of phonemes in the current word
        word_phonemes = []
        while start < len(phonemes):
            phoneme = phonemes[start]
            if phoneme.strip():  # Skip empty phonemes (e.g., spaces)
                word_phonemes.append(phoneme)
                start += 1
            else:
                start += 1  # Skip space
                break  # Stop at space (word boundary)
        
        # Append phonemes and vibration patterns for the current word
        phoneme_groups.append(word_phonemes)
        vibration_groups.append(vibration_patterns[start - len(word_phonemes):start])
    
    # Simulate haptic feedback for each word with a 200ms gap
    for word_phonemes, word_vibrations in zip(phoneme_groups, vibration_groups):
        for phoneme, pattern in zip(word_phonemes, word_vibrations):
            frequency = pattern['frequency']
            duration = pattern['duration']
            intensity = pattern['intensity']
            pattern_desc = pattern['pattern']
            print(f"Playing beep for Phoneme '{phoneme}': {frequency} Hz, {intensity}% intensity, {duration} ms duration, Pattern: {pattern_desc}")
            
            # Generate the sound based on the pattern
            waveform = generate_pattern_sound(pattern_desc, frequency, duration, intensity)
            
            # Play the sound
            sd.play(waveform, samplerate=44100)
            sd.wait()  # Wait until the sound is finished
        
        # Add a 200ms gap after each word
        print("Adding 200ms gap between words...")
        time.sleep(0.2)