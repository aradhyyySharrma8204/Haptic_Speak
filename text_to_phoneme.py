from g2p_en import G2p

def text_to_phoneme(text):
    """
    Convert text to phonemes using G2P.
    """
    # Initialize the G2P converter
    g2p = G2p()
    
    # Convert text to phonemes
    phonemes = g2p(text)
    
    # Return the phonemes
    return phonemes

if __name__ == "__main__":
    text = "This is a test sentence."
    phonemes = text_to_phoneme(text)
    print("Phonemes:", phonemes)