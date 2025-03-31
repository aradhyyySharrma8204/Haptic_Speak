import pandas as pd

def load_dataset():
    """
    Load the phoneme-to-vibration mapping dataset.
    """
    return pd.read_excel("data/phoneme_mapped_corrected.xlsx")

def predict_vibration(phonemes):
    """
    Predict vibration patterns for given phonemes using the dataset.
    """
    # Load the dataset
    df = load_dataset()
    
    # Initialize a list to store vibration patterns
    vibration_patterns = []
    
    for phoneme in phonemes:
        # Find the phoneme in the dataset
        match = df[df['Phoneme'] == phoneme]
        if not match.empty:
            # Extract the vibration pattern
            pattern = {
                'frequency': match['Frequency (Hz)'].values[0],
                'duration': match['Duration (ms)'].values[0],
                'intensity': match['Intensity (%)'].values[0],
                'pattern': match['Pattern'].values[0]
            }
            vibration_patterns.append(pattern)
        else:
            # Use a default pattern if the phoneme is not found
            vibration_patterns.append({
                'frequency': 500,
                'duration': 100,
                'intensity': 50,
                'pattern': 'Default vibration'
            })
    
    return vibration_patterns

if __name__ == "__main__":
    # Test the function
    phonemes = ['/p/', '/t/', '/k/', '/m/', '/iː/']
    vibration_patterns = predict_vibration(phonemes)
    print("Vibration Patterns:")
    for phoneme, pattern in zip(phonemes, vibration_patterns):
        print(f"Phoneme '{phoneme}': {pattern}")