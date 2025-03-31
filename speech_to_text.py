import whisper

def speech_to_text(audio_file):
    """
    Convert speech to text using Whisper.
    """
    # Load the Whisper model
    model = whisper.load_model("base")
    
    # Transcribe the audio file
    result = model.transcribe(audio_file)
    
    # Return the transcribed text
    return result["text"]

if __name__ == "__main__":
    audio_file = "data/speech.wav"
    text = speech_to_text(audio_file)
    print("Transcribed Text:", text)