import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.optimizers import Adam
import matplotlib.pyplot as plt

# Load the dataset
def load_dataset():
    return pd.read_excel("data/phoneme_mapped_corrected.xlsx")

# Encode phonemes to numeric format
def encode_phonemes(phonemes):
    phoneme_encoder = LabelEncoder()
    phoneme_encoder.fit(phonemes)
    return phoneme_encoder

# Prepare data for training
def prepare_data(df, phoneme_encoder):
    phoneme_sequences = df['Phoneme'].values
    encoded_phonemes = phoneme_encoder.transform(phoneme_sequences)
    X = encoded_phonemes.reshape(-1, 1)  # Features (phonemes)
    y = df[['Frequency (Hz)', 'Duration (ms)', 'Intensity (%)']].values  # Labels
    return X, y

# Build LSTM model
def build_model(input_dim, output_dim):
    model = Sequential()
    model.add(Embedding(input_dim=input_dim, output_dim=128, input_length=1))
    model.add(LSTM(128, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(output_dim))
    model.compile(optimizer=Adam(), loss='mean_squared_error', metrics=['mae'])
    return model

# Load and prepare data
df = load_dataset()
phoneme_encoder = encode_phonemes(df['Phoneme'].values)
X, y = prepare_data(df, phoneme_encoder)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build and compile the model
model = build_model(input_dim=len(phoneme_encoder.classes_), output_dim=3)
model.summary()

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Plot training and validation loss
# plt.plot(history.history['loss'], label='Train Loss')
# plt.plot(history.history['val_loss'], label='Validation Loss')
# plt.legend()
# plt.title('Model Training Loss')
# plt.xlabel('Epochs')
# plt.ylabel('Loss')
# plt.show()

# Evaluate the model
# test_loss, test_mae = model.evaluate(X_test, y_test)
# print(f"Test Loss: {test_loss}, Test MAE: {test_mae}")

# Make predictions
predictions = model.predict(X_test)
for i, phoneme in enumerate(X_test[:5]):
    print(f"Phoneme: {phoneme_encoder.inverse_transform([phoneme])[0]}, Mapping phonemes to vibrations... : {predictions[i]}")